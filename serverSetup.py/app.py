from fastmcp.server import FastMCPServer
import uvicorn
from mcpHost import mcpHost



class RoutePlanningMCPServer(FastMCPServer):
    def __init__(self, mcpHost):
        super().__init__(mcpHost)
    def handleInput(self, input):
        planner = self.mcpHost.getTool("planner_tool")
        plan = planner(input)
        for step in plan:
            print(step)
        return plan

if __name__ == "__main__":
    mcpHost = mcpHost
    server = RoutePlanningMCPServer(mcpHost)
    uvicorn.run(server, host="0.0.0.0", port=8001)