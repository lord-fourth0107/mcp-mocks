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
        tools_list = []
        for tool in toolList:
            tool_object = await mcp.get_tool(tool)
            clean_schema = {
                "name": tool_object.name,
                "description": tool_object.description,
                "parameters": tool_object.parameters,
            }
            tool_list = {
                "name": tool_object.name,
                "description": tool_object.description,
            }
            tools_list.append(tool_list)
            tool_schemas.append(clean_schema)
        tools_schemas  = json.dumps(tool_schemas)
        tools_list =json.dumps(tools_list)
        return tools_list,tools_schemas
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
                available_tools = await mcp.get_tools()
                tool_list, tool_schema = await self.get_tools(available_tools)
                #inputReadinessPromptFunc = await client.get_prompt("input_readiness_prompt")
                high_level_plan_prompt = await client.get_prompt("high_level_planner_prompt",{"userInput" : self.userInput, "userContext" : self.userContext, "tools_schema" : tool_list})
                checkResponse = self.remote_llm_host.chat_with_LLM(high_level_plan_prompt.messages[0].content.text)
                print(checkResponse)
                high_level_plan_json = json.loads(checkResponse['message']['content'])
                high_level_plan = high_level_plan_json["plan"]
                high_level_plan.append("endpoint")
                print(high_level_plan)
                i= 0
                for tool in high_level_plan:
                  if(tool!="endpoint"):
                    tool_schema = json.loads(tool_schema)
                    response = await client.call_tool(tool, tool_schema[tool]['TABSInput'])
                    i+=1
                    tool_args_prompt = await client.get_prompt("get_tool_args_prompt",{"tool_name" : tool, "tool_args": tool_schema[tool]['parameter'], "userContext" : self.userContext,"history":self.work_history,"response":self.response_history[0]})
                    llm_response = self.remote_llm_host.chat_with_LLM(tool_args_prompt.messages[0].content.text)
                    print(llm_response)
                    #response = await client.call_tool(tool, )
                    self.work_history.append(response.json())
                    self.response_history.append(response.json())
                    if(response.json()["status"] == "200"):
                            continue
                    else:
                        return response.json()
                else:
                    return response.json()
            except Exception as e:
                print(e)
