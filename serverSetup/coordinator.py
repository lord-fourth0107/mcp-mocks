import httpx
from dataModels.apiInputs import UserInput
from llmApi.llmapi import LLMClient
class Coordinator_Agent(UserInput):
    def __init__(self, request: UserInput, remote_llm_client: LLMClient):
        self.projectId = request.projectId
        self.userId = request.userId
        self.requestId = request.requestId
        self.userInput = request.userInput
        self.remote_llm_client = remote_llm_client

    async def coordinate(toolList):
        work_history = []
        response_history = []
        for tool in toolList:
            async with httpx.AsyncClient() as client:
                response = await client.post(tool, json = {"work_history" : work_history, "response_history" : response_history})
                work_history.append(response.json())
                response_history.append(response.json())
                if(response.json()["status"] == "200"):
                    continue
                else:
                    pass
                
                
                

                ## Complete this into a working coordinator agent and add status check for each response




    