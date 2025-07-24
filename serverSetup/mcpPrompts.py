from serverSetup.mcpServer import mcp
from fastmcp.prompts.prompt import PromptMessage, Prompt,TextContent
import json
from fastmcp import Context


@mcp.prompt
async def high_level_planner_prompt(
    userInput: str,
    tools_schema: str,
    userContext: dict,
    ctx: Context
) -> PromptMessage:
    """
    Generates a high-level plan consisting only of a sequence of tool names.
    """
    content = (
        "You are a high-level planner. Your task is to determine the sequence of tools needed to accomplish the user's goal. "
        "Do not determine the arguments for the tools yet.\n\n"
        "--- TASK ---\n"
        f"User's Goal: {userInput}\n\n"
        f"--- AVAILABLE TOOLS ---\n"
        f"{tools_schema}\n\n"
        "--- YOUR RESPONSE ---\n"
        "Your response MUST be a single JSON object with one key, 'plan', which is a list of tool names in the correct order of execution. "
        "Example: {\"plan\": [\"tool_name_1\", \"tool_name_2\"]}"
    )    
    return PromptMessage(role="user", content=TextContent(type="text", text=content))
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

@mcp.prompt 
async def get_tool_args_prompt(
    tool_name: str,
    tool_args: dict,
    userContext: dict,
    history: dict,
    response: dict,
    ctx: Context
) -> PromptMessage:
    content = (
         "You are an expert at preparing API requests. Your task is to create the precise JSON input for the upcoming tool call.\n"
        "Analyze the original user goal, the user's context data, and the history of previous tool outputs to find the values for all required parameters in the tool's schema.\n\n"
        "--- CURRENT TOOL ---\n"
         f"{tool_name} \n" 
        "--- CURRENT TOOL ARGUMENTS ---\n"
        f" {tool_args}.\n\n"
        "--- USER CONTEXT ---\n"
        f"{userContext}\n\n"
        "--- HISTORY OF PREVIOUS STEPS (Use this to find inputs for the current step) ---\n"
        f"{history}\n\n"
        "--- RESPONSE FROM PREVIOUS STEPS (Use this to find inputs for the current step) ---\n"
        f"{response}\n\n"
        "--- YOUR RESPONSE ---\n"
        "Your response MUST be a single, valid JSON object that exactly matches the tool's input schema."
    )
    return PromptMessage(
        role="user", content=TextContent(type="text", text=content)
    )
# @mcp.prompt(name = "react_prompt")
# async def react_prompt(
#     userInput : str,
#     tools_schema,
#     userContext : dict,
#     ctx : Context
#     ) -> PromptMessage:
#     """Prompt which provides plan for a given natural language input."""
#     # This now uses the input from your client, so you can see it working.

#     content = (
#         "You are a tool planner assistant. Read the user's request and the available tools, "
#         "then come up with a plan of which tools to call in sequence. "
#         f"The user's request is: '{userInput}'.\n"
#         f"The available tools are: {tools_schema}\n"
#         "Your response must be a single JSON object with two keys: 'tool_names' (a list of tool function names to call in order) "
#         "and 'tool_args' (a list of dictionaries for each tool's arguments)."
#         f" The tool arguments needs to be filled using the details in context {userContext}\n"
#     )    
#     return PromptMessage(role = "user", content = TextContent(type = "text", text = content))

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
        "You are an expert AI project planner for an architectural design firm. "
        "Your goal is to analyze the user's request and the provided context to decide on one of two actions: ELICIT_INPUT or EXECUTE_PLAN.\n\n"
        "### INSTRUCTIONS & LOGIC ###\n"
        "1. **Analyze**: Carefully review the User Request, the User Context, and the schemas in Available Tools.\n"
        "2. **Decide**: \n"
        "   - If the request is vague or lacks details required by a tool's parameters (e.g., asking for a 'program sheet' without a CSV file), you MUST choose the ELICIT_INPUT action.\n"
        "   - If the request and context provide enough information to fill all required arguments for at least the first tool in a logical sequence, you MUST choose the EXECUTE_PLAN action.\n\n"
        "### OUTPUT FORMAT ###\n"
        "Your response MUST be a single, valid JSON object. Choose ONLY ONE of the following two formats:\n\n"
        "1. For asking the user a question:\n"
        '{\n'
        '  "action": "elicit_input",\n'
        '  "user_message": "Your clear, friendly question to the user to get the missing information."\n'
        '}\n\n'
        "2. For creating a plan:\n"
        '{\n'
        '  "action": "execute_plan",\n'
        '  "plan": {\n'
        '    "steps": [\n'
        '      {\n'
        '        "tool_name": "name_of_the_first_tool",\n'
        '        "tool_args": {\n'
        '          "argument_name": "value_from_user_request_or_context"\n'
        '        }\n'
        '      }\n'
        '    ]\n'
        '  }\n'
        '}\n\n'
        "--- PROVIDED DATA ---\n"
        f"User Request: {userInput}\n"
        f"User Context: {userContext}\n"
        f"Available Tools: {tools_schema}\n\n"
        "--- YOUR JSON RESPONSE ---"
    )
    return PromptMessage(
        role = "user", content = TextContent(type = "text", text = content)
    )
    
