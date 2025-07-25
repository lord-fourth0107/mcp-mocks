from serverSetup.mcpServer import mcp
from fastmcp import Context
import os 
import httpx
from dataModels.apiInputs import TABSInput, FLANEInput, BubbleInput, UserInput

@mcp.tool
async def room_list_and_graph_adjacency_and_program_sheet_generation_tool(apiInput:TABSInput,
                                        ctx : Context
                                        ) -> dict:
    """Tool which takes user inputs and generates room list and graph adjacencies and program sheet"""
    API_URL = os.getenv("TABS_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, params = apiInput.model_dump())
        return response.json()

@mcp.tool
async def floor_plan_generation_tool(apiInput:FLANEInput,
                                     ctx : Context
                                     ) -> dict:
    """ Tool which uses room list and  the graph adjacencies and toom list from program sheet output and genertates a floor plan"""
    API_URL = os.getenv("FLANE_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, params = apiInput.model_dump())
        return response.json()
    

@mcp.tool
async def bubble_diagram_generation_tool(apiInput:BubbleInput,
                                         ctx : Context) -> dict:
    """ Tool which uses the file location of coordinates to generate the bubble diagram """
    await ctx.info(f"Received request for user_id: {apiInput.userId}")
    API_URL = os.getenv("BUBBLE_API_URL")
    ## Put here the json request of tabs
    async with httpx.AsyncClient() as client: 
        response  = await client.get(API_URL, params = apiInput.model_dump())
        return response.json()

# @mcp.tool
# async def status_code_checker(api_input) -> dict:
#     pass ## change the argument to apiOutput and create a data model for api output
