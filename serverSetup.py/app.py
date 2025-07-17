from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn
from loguru import logger
from mcpServer import mcp
import mcpTool
mcp_app = mcp.http_app(path="/mcp")
# 1. Create the main FastAPI application
app = FastAPI(title="Architectural Assistant Server",lifespan = mcp_app.lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}# ... add your other tools here, making sure they accept arguments if needed ...

print(f"MCP object is :", mcp.http_app())
# 4. Mount the MCP app at "/mcp" to match your client's URL
app.mount("/mcp-server", mcp_app)

# 5. Run the server
if __name__ == "__main__":
    # This command will now work correctly because the file is named "app.py"
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True,debug=True,logger_level="info")
    logger.info("Server started")
