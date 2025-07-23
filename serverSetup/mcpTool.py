from serverSetup.mcpServer import mcp
from fastmcp import Context
import os 
import httpx
from dataModels.apiInputs import TABSInput, FLANEInput, BubbleInput

@mcp.tool
async def room_list_and_graph_adjacency_and_program_sheet_generation_tool(api_input:TABSInput,
                                        ctx : Context
                                        ) -> dict:
    API_URL = os.getenv("TABS_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, params = api_input.model_dump())
        return response.json()

@mcp.tool
async def floor_plan_generation_tool(api_input:FLANEInput,
                                     ctx : Context
                                     ) -> dict:
    """ Tool which uses the graph adjacencies and toom list from program sheet output and genertates a floor plan"""
    API_URL = os.getenv("FLANE_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, params = api_input.model_dump())
        return response.json()
    

@mcp.tool
async def bubble_diagram_generation_tool(api_input:BubbleInput,
                                         ctx : Context) -> dict:
    """ Tool which uses the file location of coordinates to generate the bubble diagram """
    await ctx.info(f"Received request for user_id: {api_input.userId}")
    API_URL = os.getenv("BUBBLE_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, params = api_input.model_dump())
        return response.json()

# @mcp.tool
# async def status_code_checker(api_input) -> dict:
#     pass ## change the argument to apiOutput and create a data model for api output
