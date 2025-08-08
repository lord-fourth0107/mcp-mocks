import ollama
import os
# from ollama import Client
from google import genai
from google.genai.types import HttpOptions

# import google.generativeai as genai
import json
class LLMClient:

    def __init__(self):
        print(os.getenv("LLM_PROJECT_ID"))
        try :
            self.remote_llm_client = genai.Client(
                vertexai = True,
                project = os.getenv("LLM_PROJECT_ID"),
                location = os.getenv("LLM_REGION"),
                http_options = HttpOptions(api_version = "v1" )

            )
            # vertexai.init(project = os.getenv("LLM_PROJECT_ID"), location = os.getenv("LLM_REGION"))
            # self.remote_llm_client = GenerativeModel(os.getenv("LLM_MODEL"))
        except Exception as e:
            print(e)
        
    def chat_with_LLM(self,prompt : str, toolList : list[str] = []) -> str:
        #print(prompt)
        response = self.remote_llm_client.models.generate_content(
            model = os.getenv("LLM_MODEL"),
            contents = prompt
            )
        # response = self.remote_llm_client.generate_content(prompt)
        # response = json.loads(response)
        return response


