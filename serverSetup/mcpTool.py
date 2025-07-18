from fastmcp import FastMCP
from serverSetup.mcpServer import mcp
import os 
import httpx
@mcp.tool
def planner_tool(inputNaturalLanguage: str) -> str:
    """Tool which provides plan for a given natural language input."""
    # This now uses the input from your client, so you can see it working.
    return f"A detailed plan has been generated for: {inputNaturalLanguage}"

@mcp.tool
async def program_sheet_generation_tool():
    API_URL = os.getenv("TABS_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL)
        return response.json()

@mcp.tool
async def floor_plan_generation_tool():
    pass

@mcp.tool
async def bubble_diagram_generation_tool():
    pass