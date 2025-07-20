from serverSetup.mcpServer import mcp
from fastmcp.prompts.prompt import PromptMessage, Prompt,TextContent
import json

@mcp.prompt
async def planner_prompt(
    userInput : str
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
    
    return PromptMessage(role = "user", content = TextContent(type="text",content = content))

# @mcp.prompt
# def coordinator_prompt()