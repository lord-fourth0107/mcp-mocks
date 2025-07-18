import ollama, Client
import os




class LLMClient:

    def __init__(self):
        self.remotellmClient = ollama.Client(os.getenv("LLM_API_URL"))
    def chat_with_LLM(self,prompt : str, toolList : list[str] = []) -> str:
        response = self.remote_llm_client.chat(
            [
                {
                    "role": "user",
                    "content":prompt,
                    "format":'json'

                }
            ]
        )
        return response


