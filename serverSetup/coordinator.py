from dataModels.apiInputs import TABSInput,BubbleInput,FLANEInput,CSVFile,MetaData,Options
from dataModels.baseInput import UserInput
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
    async def _create_json_template(self, schema: dict) -> dict:
        """
        Recursively creates a JSON template with null values from a Pydantic schema.
        """
        template = {}
        properties = schema.get('properties', {})
        for key, prop in properties.items():
            if '$ref' in prop:
                # Find the definition in $defs and recurse
                def_name = prop['$ref'].split('/')[-1]
                template[key] = self._create_json_template(schema['$defs'][def_name])
            elif 'properties' in prop:
                 template[key] = self._create_json_template(prop)
            else:
                template[key] = None # Set the value to null
        return template
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
                high_level_plan_json = json.loads(checkResponse['message']['content'])
                high_level_plan = high_level_plan_json["plan"]
                high_level_plan.append("endpoint")
                print(high_level_plan)
                i= 0
                for tool in high_level_plan:
                  if(tool!="endpoint"):
                    if(tool == "room_list_and_graph_adjacency_and_program_sheet_generation_tool"):
                        if(self.userInput.userQuery.__contains__("generate")):
                                action = "create"
                        else:
                            action = "update"
                            
                        apiInput = TABSInput(
                            userId = self.userInput.userId,
                            projectId = self.userInput.projectId,
                            studyId = self.userInput.studyId,
                            requestId = self.userInput.requestId,
                            action = action,
                            prompt = self.userInput.userQuery,
                            csvFile = None,
                            options = Options(language = "en"),
                            metadata = MetaData()
                        )
                    elif(tool == "floor_plan_generation_tool"):
                                apiInput = FLANEInput(
                                userId = self.userInput.userId,
                                projectId = self.userInput.projectId,
                                studyId = self.userInput.studyId,
                                requestId = self.userInput.requestId,
                                options = Options(language = "en"),
                                metaData = MetaData()
                            )
                    else:
                                apiInput = BubbleInput(
                                userId = self.userInput.userId,
                                projectId = self.userInput.projectId,
                                studyId = self.userInput.studyId,
                                requestId = self.userInput.requestId,
                                options = Options(language = "en"),
                                metaData = MetaData()
                            )
                    response = await client.call_tool(tool, {"apiInput" : apiInput})
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
