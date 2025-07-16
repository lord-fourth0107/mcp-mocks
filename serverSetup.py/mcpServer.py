from fastmcp import FastMCP
class RoutePlanningMCPServer(FastMCP):
    def __init__(self,name :str):
        super().__init__(name)
    def handleInput(self, input):
        planner = self.getTool("planner_tool")
        plan = planner(input)
        for step in plan:
            print(step)
        return plan
