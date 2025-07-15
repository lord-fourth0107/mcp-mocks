from fastmcp.host import FastMCPHost
from mcpTool import *


class PlannerHost(FastMCPHost):
    def __init__(self):
        super().__init__()
    def addTool(self, tool_name):
        self.add_tool(tool_name)
if __name__ == "__main__":
    mcpHost = PlannerHost()
    mcpHost.addTool(floor_plan_generation_tool)
    mcpHost.addTool(program_sheet_gereration_tool)
    mcpHost.addTool(planner_tool)
    mcpHost.addTool(bubble_diagram_generation_tool)