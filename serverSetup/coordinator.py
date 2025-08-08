from dataModels.apiInputs import TABSInput,BubbleInput,FLANEInput,CSVFile,MetaData,Options
from dataModels.baseInput import UserInput
from llmApi.llmapi import LLMClient
from serverSetup.mcpServer import mcp
import json 
import re 
import concurrent.futures
import time 
import os 
from brooklyn_api_gcp_commons import CloudStorageOperations, ServiceType 

from fastmcp import Client as MCPClient
class Coordinator_Agent():
    def __init__(self, request: UserInput,
                remote_llm_host: LLMClient, 
                ):
        self.userInput = request
        self.remote_llm_host = remote_llm_host
        self.storage = None
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
                def_name = prop['$ref'].split('/')[-1]
                template[key] = self._create_json_template(schema['$defs'][def_name])
            elif 'properties' in prop:
                 template[key] = self._create_json_template(prop)
            else:
                template[key] = None 
        return template
    def upload_converstaions(self,fileName):
         storage = CloudStorageOperations(
             bucket_name = os.getenv("GCP_BUCKET_NAME")
         )
         keys =["userId","projectId","userQuery","llm_response"]
         values =[self.userInput.userId,self.userInput.projectId,self.userInputList,self.llm_responses]
         data = dict(zip(keys,values))
         json_data = json.dumps(data,indent =4)
         #print(json_data)
         with open(json_data, "rb") as f:
             result = storage.upload(
                 ServiceType.USER,
                 user_id = self.userInput.userId,
                 project_id = self.userInput.projectId,
                 filestream = f,
                 filename = fileName ,
                 content_type = "application/json",
             )
         return result
         
    async def call_task_list(self,high_level_plan,client):
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
                                requestId = self.userInput.requestId,
                                options = Options(language = "en"),
                                metaData = MetaData()
                            )
                else:
                                apiInput = BubbleInput(
                                userId = self.userInput.userId,
                                projectId = self.userInput.projectId,
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
    async def coordinate(self):
        self.userInputList = []
        self.llm_responses = []
        self.work_history = []
        self.response_history = []
        self.userContext = {
            "userId" : self.userInput.userId,
            "requestId" : self.userInput.requestId,
            "projectId" : self.userInput.projectId,
        }
        async  with MCPClient("http://127.0.0.1:8000/mcp-server/mcp") as client:
            try:
                available_tools = await mcp.get_tools()
                tool_list, tool_schema = await self.get_tools(available_tools)            
                high_level_plan_prompt = await client.get_prompt("high_level_planner_prompt",{"userInput" : self.userInput, "userContext" : self.userContext, "tools_schema" : tool_list})
                checkResponse = self.remote_llm_host.chat_with_LLM(high_level_plan_prompt.messages[0].content.text)
                high_level_plan_text = checkResponse.text
                try:
                    json_str_match = re.search(r'\{.*\}', high_level_plan_text, re.DOTALL)
                
                    if not json_str_match:
                        print("Error: No JSON object found in the response string.")
                        return []
                    json_str = json_str_match.group(0)
                    data = json.loads(json_str)
                    tool_list = data.get('plan', [])
                except json.JSONDecodeError:
                    print("Error: Failed to decode the extracted JSON string.")
                except AttributeError:
                    print("Error: Could not find a match for the JSON pattern.")
                high_level_plan = tool_list
                high_level_plan.append("endpoint")
                self.userInputList.append(self.userInput.userQuery )
                self.llm_responses.append(high_level_plan)
                with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
                     future_response_1 =  executor.submit(self.upload_converstaions("user_conversation_history.json"))
                     future_response_2 = executor.submit(await self.call_task_list(high_level_plan,client))
                     if(future_response_1.status == 200 and  future_response_2.status == 200):
                          return
                     else:
                          print("stupid stuff")
                    #        return APIOutput(
                    #            requestId = self.userInput.requestId,
                    #            userId = self.userInput.userId,
                    #            status = "200",
                    #            response = "Success",
                    #        )
                    #  else:
                    #       return APIOutput(
                               
                    #       )

            except Exception as e:
                print(e)
