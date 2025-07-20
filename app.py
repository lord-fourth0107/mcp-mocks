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
load_dotenv()
mcp_app = mcp.http_app(path="/mcp")
# 1. Create the main FastAPI application
app = FastAPI(title="Architectural Assistant Server",lifespan = mcp_app.lifespan)
class InputData(BaseModel):
    natural_language_input : str
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
async def root(data : InputData):
    natural_language_input = data.natural_language_input
    
    response = await coordinator_agent(natural_language_input) 
    print(response)

print(f"MCP object is :", mcp.http_app())
# 4. Mount the MCP app at "/mcp" to match your client's URL
app.mount("/mcp-server", mcp_app)

# 5. Run the server
if __name__ == "__main__":
    # This command will now work correctly because the file is named "app.py"
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Server started")
