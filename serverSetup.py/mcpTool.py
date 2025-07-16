from fastmcp import FastMCP
# from mcpServer import RoutePlanningMCPServer as mcp
@mcp.tool
def planner_tool(inputNaturalLanguage:str):
    """ Tool which provides plan for a given natural language input"""
    if(inputNaturalLanguage.__contains__("program sheet")):
        return {
            "tool":"program_sheet_gereration_tool",
             "input" : inputNaturalLanguage
        }
    elif(inputNaturalLanguage.__contains__("floor plan")):
        return "Floor Plan for " + inputNaturalLanguage
    elif(inputNaturalLanguage.__contains__("bubble diagram")):
        return "Bubble Diagram for " + inputNaturalLanguage
    else:   
        return "Plan for " + inputNaturalLanguage


@mcp.tool
def program_sheet_gereration_tool():
    """ Tool which provides program sheet for a given natural language input"""

@mcp.tool 
def floor_plan_generation_tool():
    """ Tool which provides floor plan for a given natural language input"""

@mcp.tool
def bubble_diagram_generation_tool():
    """ Tool which provides bubble diagram for a given natural language input"""
