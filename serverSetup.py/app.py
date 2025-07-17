from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn
from loguru import logger

mcp = FastMCP()
mcp_app = mcp.http_app(path="/mcp")
# 1. Create the main FastAPI application
app = FastAPI(title="Architectural Assistant Server",lifespan = mcp_app.lifespan)

# 2. Create the MCP application

@app.get("/")
async def root():
    return {"message": "Hello World"}
# 3. Define the tool to correctly accept and USE the argument
@mcp.tool
def planner_tool(inputNaturalLanguage: str) -> str:
    """Tool which provides plan for a given natural language input."""
    # This now uses the input from your client, so you can see it working.
    return f"A detailed plan has been generated for: {inputNaturalLanguage}"

# ... add your other tools here, making sure they accept arguments if needed ...

print(f"MCP object is :", mcp.http_app())
# 4. Mount the MCP app at "/mcp" to match your client's URL
app.mount("/mcp-server", mcp_app)

# 5. Run the server
if __name__ == "__main__":
    # This command will now work correctly because the file is named "app.py"
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True,debug=True,logger_level="info")
    logger.info("Server started")
