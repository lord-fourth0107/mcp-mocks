import ollama
import os
from ollama import Client




class LLMClient:

    def __init__(self):
        print("LLM API URL is:",os.getenv("LLM_API_URL"))
        self.remote_llm_client = Client(host=os.getenv("LLM_API_URL"))
    def chat_with_LLM(self,prompt : str, toolList : list[str] = []) -> str:
        print(prompt)
        response = self.remote_llm_client.chat(
            model = "llama3:latest",
            messages = [
                {
                    "role": "user",
                    "content":prompt,
                }
            ],
             format ="json"
        )
        return response


