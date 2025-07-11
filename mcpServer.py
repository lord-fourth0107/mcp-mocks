from mcp.server.fastmcp import FastMCP
from mcp.types import (Completion,
                       ResourceTemplateReference,
                       PromptReference, 
                       CompletionContext,
                       CompletionArgument)
from pydantic import BaseModel, Field


mcpServer = FastMCP(
    name = "Input Completion Server"
)
class InputAdjacencySchema(BaseModel):
    nodes: list[str] = Field(default_factory=list)
    graph_edges : list[tuple[int,int,int]] = Field(default_factory=list)

@mcp.tool
def inputCompletionTool():
    ''' Tool for Input Completion '''

    

@mcp.