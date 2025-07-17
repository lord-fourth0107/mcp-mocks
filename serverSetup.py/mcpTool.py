from fastmcp import FastMCP
from mcpServer import mcp
# from mcpServer import RoutePlanningMCPServer as mcp
# 3. Define the tool to correctly accept and USE the argument
@mcp.tool
def planner_tool(inputNaturalLanguage: str) -> str:
    """Tool which provides plan for a given natural language input."""
    # This now uses the input from your client, so you can see it working.
    return f"A detailed plan has been generated for: {inputNaturalLanguage}"

@mcp.tool
def program_sheet_generation_tool():
    pass

@mcp.tool
def floor_plan_generation_tool():
    pass

@mcp.tool
def bubble_diagram_generation_tool():
    pass