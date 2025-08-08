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
from dataModels.baseInput import UserInput
from serverSetup.coordinator import Coordinator_Agent
load_dotenv()
mcp_app = mcp.http_app(path="/mcp")
# 1. Create the main FastAPI application

app = FastAPI(title="Architectural Assistant Server",lifespan = mcp_app.lifespan)
remote_llm_host = LLMClient()

app.mount("/mcp-server", mcp_app)


@app.get("/")
async def root(request : UserInput):
    userInput = UserInput( userId = request.userId,
                          userQuery = request.userQuery, 
                          projectId = request.projectId, 
                          requestId = request.requestId, 
                          )
   
    coordinator_agent =  Coordinator_Agent(request = userInput, remote_llm_host = remote_llm_host)
    response = await coordinator_agent.coordinate()
    return response


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Server started")
