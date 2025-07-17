from mcpServer import mcp
from fastmcp.prompts.promt import PromptMessage, Prompt,TextContent

@mcp.prompt
def planner_prompt(inputNaturalLanguage: str) -> str:
    """Prompt which provides plan for a given natural language input."""
    # This now uses the input from your client, so you can see it working.
    content = " You are a tool planner assistant, which read the customer's request from the user's input  and plans the next tool or a sequence of tools to be called." \
    "Using the user's input as stated in : {inputNaturalLanguage}, can you come up with a plan of tools or sequence of tools to complete the task?"  \
    
    return PromptMessage(role = "user", content = TextContent(type="text",content = content))