from mcp.server.fastmcp import FastMCP
from mcp.types import (Completion,
                       ResourceTemplateReference,
                       PromptReference, 
                       CompletionContext,
                       CompletionArgument)
from pydantic import BaseModel, Field



@mcp.tool
def planner_tool(inputNaturalLanguage:str):
    """ Tool which provides plan for a given natural language input"""


@mcp.tool
def program_sheet_gereration_tool():
    """ Tool which provides program sheet for a given natural language input"""

@mcp.tool 
def floor_plan_generation_tool():
    """ Tool which provides floor plan for a given natural language input"""

@mcp.tool
def bubble_diagram_generation_tool():
    """ Tool which provides bubble diagram for a given natural language input"""
