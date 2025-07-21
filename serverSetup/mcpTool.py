from serverSetup.mcpServer import mcp
import os 
import httpx
from dataModels.apiInputs import TABSInput, FLANEInput, BubbleInput

@mcp.tool
async def program_sheet_generation_tool(api_input:TABSInput) -> dict:
    API_URL = os.getenv("TABS_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, json = api_input.model_dump())
        return response.json()

@mcp.tool
async def floor_plan_generation_tool(api_input:FLANEInput) -> dict:
    """ Tool which uses the graph adjacencies and toom list from program sheet output and genertates a floor plan"""
    API_URL = os.getenv("FLANE_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, json = api_input.model_dump())
        return response.json()
    

@mcp.tool
async def bubble_diagram_generation_tool(api_input:BubbleInput) -> dict:
    """ Tool which uses the file location of coordinates to generate the bubble diagram """
    API_URL = os.getenv("BUBBLE_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, json = api_input.model_dump())
        return response.json()
    

@mcp.tool
async def status_code_checker(api_input) -> dict:
    pass ## change the argument to apiOutput and create a data model for api output
