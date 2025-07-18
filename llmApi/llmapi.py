import ollama
import os
from ollama import Client




class LLMClient:

    def __init__(self):
        self.remote_llm_client = ollama.Client(os.getenv("LLM_API_URL"))
    def chat_with_LLM(self,prompt : str, toolList : list[str] = []) -> str:
        print(prompt)
        response = self.remote_llm_client.chat(
            model = "llama-3b",
            messages = [
                {
                    "role": "user",
                    "content":prompt,
                }
            ],
             format ="json"
        )
        return response


