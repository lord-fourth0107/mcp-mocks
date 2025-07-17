import asyncio
from fastmcp import Client

async def main():
    # Connect to the running server
    async with Client("http://127.0.0.1:8000/mcp-server/mcp") as client:
        # Call the 'add' tool and print the result
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("planner_tool", {"inputNaturalLanguage" : "bubble diagram"})
        print(f"The result is: {result}")

if __name__ == "__main__":
    asyncio.run(main())