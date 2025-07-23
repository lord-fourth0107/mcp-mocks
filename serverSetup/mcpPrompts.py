from serverSetup.mcpServer import mcp
from fastmcp.prompts.prompt import PromptMessage, Prompt,TextContent
import json
from fastmcp import Context

@mcp.prompt
async def master_planner_prompt(
    userInput: str,
    tools_schema: str,
    userContext: dict,
    ctx: Context  # The context is still defined here
) -> PromptMessage:
    """
    A master prompt that first validates user input and then creates a plan.
    If input is insufficient, it elicits more information.
    """
    content = (
        "You are an expert AI assistant for architectural design.\n"
        "Your task is to analyze a user's request and the available tools. You have two possible actions:\n"
        "1. **ELICIT_INPUT**: If the user's request is vague or missing critical details required by the tools (like number of rooms for a floor plan), you must ask a friendly, clarifying question. Your entire response must be a JSON object like this: {\"action\": \"elicit_input\", \"user_message\": \"Your question to the user.\"}\n"
        "2. **EXECUTE_PLAN**: If the user's request is clear and has enough information to proceed, you must create a multi-step plan. Your entire response must be a JSON object like this: {\"action\": \"execute_plan\", \"plan\": {\"steps\": [{\"tool_name\": \"...\", \"tool_args\": {...}}]}}\n\n"
        "--- CONTEXT ---\n"
        f"User Request: {userInput}\n"
        f"User Context: {userContext}\n"
        f"Available Tools: {tools_schema}\n\n"
        "--- YOUR ANALYSIS AND RESPONSE ---"
    )    
    return PromptMessage(role="user", content=TextContent(type="text", text=content))
@mcp.prompt(name = "react_prompt")
async def react_prompt(
    userInput : str,
    tools_schema,
    userContext : dict,
    ctx : Context
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
        f" The tool arguments needs to be filled using the details in context {userContext}\n"
    )    
    return PromptMessage(role = "user", content = TextContent(type = "text", text = content))

@mcp.prompt
def response_prompt(userInput : str,
                    userContext : dict,
                    ctx: Context
                    ) -> PromptMessage:
    """ Prompt which is responsible to find the missing details from the user input and check chat with LLM and user """
    print(f"the mcp context is {ctx}")
    content = (
        " You are an expert schema checker and a helpful chat bot for the user designed to chaet with user for missing details in his/her request,"
        " till all the required input field is not completed by the user. You will receive the api response from a tool as '{response}' , you will need to check for the missing fields and chat with the user to give more details or missing mandatory fields " \
        "Your response must be a single JSON object with two keys: 'user_message' (a human readable message of missing fields and how to provide them) and the userId  "
    )
    return PromptMessage(
        role = "user", content = TextContent(type = "text", text = content)
    )

@mcp.prompt(name = "readiness_and_planner_prompt")
async def input_readiness_prompt(userInput:str,
                                 userContext : dict,
                                 tools_schema : str,
                                 ctx: Context  ) -> PromptMessage:
    """Prompt for prompting the LLM for checking the inputs required by the api's"""
    content = (
        "You are an expert AI assistant for architectural design.\n"
        "Your task is to analyze a user's request and the available tools. You have two possible actions:\n"
        "1. **ELICIT_INPUT**: If the user's request is vague or missing critical details required by the tools (like number of rooms for a floor plan), you must ask a friendly, clarifying question. Your entire response must be a JSON object like this: {\"action\": \"elicit_input\", \"user_message\": \"Your question to the user.\"}\n"
        "2. **EXECUTE_PLAN**: If the user's request is clear and has enough information to proceed, you must create a multi-step plan. Your entire response must be a JSON object like this: {\"action\": \"execute_plan\", \"plan\": {\"steps\": [{\"tool_name\": \"...\", \"tool_args\": {...}}]}}\n\n"
        "The response cannot be empty and must be a valid JSON object and action should have one of the following values: 'elicit_input', 'execute_plan'.\n\n"
        "In case of 'elicit_input', you must return a JSON object like this: {\"action\": \"elicit_input\", \"user_message\": \"Your question to the user.\"}\n\n"
        "You must return a JSON object like this: {\"action\": \"...\", \"user_message\": \"...\", \"plan\": {\"steps\": [{\"tool_name\": \"...\", \"tool_args\": {...}}]}}\n\n"
        "--- CONTEXT ---\n"
        f"User Request: {userInput}\n"
        f"User Context: {userContext}\n"
        f"Available Tools: {tools_schema}\n\n"
        "Here is the details of api's which are available as tools, The room_list_and_graph_adjacency_and_program_sheet_generation_tool tools calls an api which takes the user input of description and generates the rooma list and graph adjacency from it. If a csv files is provided as input then it generates the program sheet," \
        "The floor_plan_generation_tool ues the room list and graph adjacency from the output of previous step and or uses the user input to construct the url for s3 to get the room list and adjacency to generate the floor plan and puts that into s3 ,"
        "The bubble diagram generation tool uses the user input to check if the floor plan exists in the s3 and prepapres a bubble diagram for the floor plan, and also returns the url of the s3 where bubble diagram is stored.\n\n,"
        "Given this context, now come up with a plan of tools to call in sequence.You cannot give an empty response\n\n"
        "--- YOUR ANALYSIS AND RESPONSE ---"
    )    
    return PromptMessage(
        role = "user", content = TextContent(type = "text", text = content)
    )
    
