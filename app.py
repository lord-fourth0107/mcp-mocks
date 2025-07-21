from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn
from loguru import logger
from serverSetup import mcp
import serverSetup.mcpTool as mcpTool
from llmApi.llmapi import LLMClient
import json
from pydantic import BaseModel
from dotenv import load_dotenv
import serverSetup.mcpTool as mcpTool
import serverSetup.mcpPrompts as mcpPrompts
from dataModels.apiInputs import UserInput
load_dotenv()
mcp_app = mcp.http_app(path="/mcp")
# 1. Create the main FastAPI application
app = FastAPI(title="Architectural Assistant Server",lifespan = mcp_app.lifespan)
remote_llm_host = LLMClient()

async def get_tools(toolList):
    tool_schemas =[]
    for tool in toolList:
        tool_object = await mcp.get_tool(tool)
        clean_schema = {
            "name": tool_object.name,
            "description": tool_object.description,
            "parameters": tool_object.parameters,
        }
        tool_schemas.append(clean_schema)
    tools_schema  = json.dumps(tool_schemas)
    return tools_schema
async def coordinator_agent(inputNaturalLanguage: str):
    try:
        prompt_func = await mcp.get_prompt("planner_prompt")
        available_tools = await mcp.get_tools()
        tool_schema = await get_tools(available_tools)
        prompt = await prompt_func.render({"userInput" :inputNaturalLanguage , "tools_schema" : tool_schema})
        print(f"Prompt is:",prompt[0].content.text)
        response = remote_llm_host.chat_with_LLM(prompt[0].content.text)
        tool_call = json.loads(response['message']['content'])
        return response
    except Exception as e:
        print(e)
@app.get("/")
async def root(request : UserInput):
    userInput = UserInput( userId = request.userId,
                          userInput = request.userInput, 
                          projectId = request.projectId, 
                          requestId = request.requestId, 
                          studyId = request.studyId
                          )
    response = await coordinator_agent(userInput.userInput) 
    print(response)

app.mount("/mcp-server", mcp_app)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Server started")
