from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn
from loguru import logger
from serverSetup import mcp
import serverSetup.mcpTool as mcpTool
from llmApi.llmapi import LLMClient
import json
from pydantic import BaseModel
mcp_app = mcp.http_app(path="/mcp")
# 1. Create the main FastAPI application
app = FastAPI(title="Architectural Assistant Server",lifespan = mcp_app.lifespan)
class InputData(BaseModel):
    natural_language_input : str
remote_llm_host = LLMClient()
async def coordinator_agent(inputNaturalLanguage: str):
    prompt_func = await mcp.get_prompt("planner_prompt")
    prompt = await prompt_func(inputNaturalLanguage)

    print(f"Prompt is:",prompt.content.content)
    response = remote_llm_host.chat_with_LLM(prompt.content.content)
    tool_call = json.loads(response['message']['content'])
    tool_names = tool_call['tool_names']
    tool_args = tool_call['tool_args']
    print(tool_names)
    return tool_names, tool_args
@app.get("/")
async def root(data : InputData):
    natural_language_input = data.natural_language_input
    
    response = coordinator_agent(natural_language_input) 
    print(response)

print(f"MCP object is :", mcp.http_app())
# 4. Mount the MCP app at "/mcp" to match your client's URL
app.mount("/mcp-server", mcp_app)

# 5. Run the server
if __name__ == "__main__":
    # This command will now work correctly because the file is named "app.py"
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Server started")
