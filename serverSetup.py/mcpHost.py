from fastmcp.host import FastMCPHost
from mcpTool import *


mcpHost = FastMCPHost()
mcpHost.addTool(floor_plan_generation_tool)
mcpHost.addTool(program_sheet_gereration_tool)
mcpHost.addTool(planner_tool)
mcpHost.addTool(bubble_diagram_generation_tool)
