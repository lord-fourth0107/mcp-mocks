from dataModels.apiInputs import UserInput
from llmApi.llmapi import LLMClient
from serverSetup.mcpServer import mcp
import json 
from fastmcp import Client as MCPClient
class Coordinator_Agent():
    def __init__(self, request: UserInput,
                remote_llm_host: LLMClient, 
                ):
        self.userInput = request
        self.remote_llm_host = remote_llm_host
    async def get_tools(self,toolList):
        tool_schemas =[]
        for tool in toolList:
            tool_object = await mcp.get_tool(tool)
            clean_schema = {
                "name": tool_object.name,
                "description": tool_object.description,
                "parameters": tool_object.parameters,
            }
            tool_schemas.append(clean_schema)
        tools_schema  = json.dumps(tool_schemas)
        return tools_schema
    async def coordinate(self):
        self.work_history = []
        self.response_history = []
        self.userContext = {
            "userId" : self.userInput.userId,
            "requestId" : self.userInput.requestId,
            "projectId" : self.userInput.projectId,
            "studyId" : self.userInput.studyId,
        }
        async  with MCPClient("http://127.0.0.1:8000/mcp-server/mcp") as client:
            try:
                prompt_func = await mcp.get_prompt("planner_prompt")
                available_tools = await mcp.get_tools()
                tool_schema = await self.get_tools(available_tools)
                prompt = await prompt_func.render({"userInput" :self.userInput , "tools_schema" : tool_schema, "userContext" : self.userContext})
                print(f"Prompt is:",prompt[0].content.text)
                response =self.remote_llm_host.chat_with_LLM(prompt[0].content.text)
                print(response)
                plan = json.loads(response['message']['content'])
                print(plan)
                toolList = plan["tool_names"]
                tool_args = plan["tool_args"]
                print(toolList)
                print(tool_args)
                for tool in toolList:
                  response = await client.call_tool(tool, tool_args[toolList.index(tool)])
                  self.work_history.append(response.json())
                  self.response_history.append(response.json())
                  if(response.json()["status"] == "200"):
                            continue
                  else:
                            pass
            except Exception as e:
                print(e)

            
                
                
                

                ## Complete this into a working coordinator agent and add status check for each response




    