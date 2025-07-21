from serverSetup.mcpServer import mcp
from fastmcp.prompts.prompt import PromptMessage, Prompt,TextContent
import json

@mcp.prompt
async def planner_prompt(
    userInput : str,
    tools_schema
    ) -> PromptMessage:
    """Prompt which provides plan for a given natural language input."""
    # This now uses the input from your client, so you can see it working.

    content = (
        "You are a tool planner assistant. Read the user's request and the available tools, "
        "then come up with a plan of which tools to call in sequence. "
        f"The user's request is: '{userInput}'.\n"
        f"The available tools are: {tools_schema}\n"
        "Your response must be a single JSON object with two keys: 'tool_names' (a list of tool function names to call in order) "
        "and 'tool_args' (a list of dictionaries for each tool's arguments)."
    )    
    return PromptMessage(role = "user", content = TextContent(type = "text", text = content))

@mcp.prompt
def response_prompt(response):
    """ Prompt which is responsible to find the missing details from the user input and check chat with LLM and user """
    content = (
        " You are an expert schema checker and a helpful chat bot for the user designed to chaet with user for missing details in his/her request,"
        " till all the required input field is not completed by the user. You will receive the api response from a tool as '{response}' , you will need to check for the missing fields and chat with the user to give more details or missing mandatory fields " \
        "Your response must be a single JSON object with two keys: 'user_message' (a human readable message of missing fields and how to provide them) and the userId  "
    )
    return PromptMessage(
        role = "user", content = TextContent(type = "text", text = content)
    )

@mcp.prompt
async def user_input_checks():
    """Prompt for prompting the LLM for checking the inputs required by the api's"""
    content = " You are an helpful assistant which takes user's input and map them to json schema and check  for all necessary fields for any particular tool input. If you receive a natural language input for generation of floor plan or program sheet, you will need to check if the user input has enough details to build a floor plan" 
    return PromptMessage(
        role = "user", content = TextContent(type = "text", text = content)
    )
    
