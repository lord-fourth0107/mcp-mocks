import ollama 
import os
def chatWithLLM():
    response = ollama.chat(
        model = os.env.get("MODEL_ID"),
        messages = [],
    )


