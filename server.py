from mcp.server import MCPServer
from pathlib import Path
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("code-explorer")
root = Path("/Users/antoannguyen/devflow-ai")

@mcp.tool()
def list_files() -> list[str]:  
    """Lists files relative to the project folder, excluding the .git folder"""
    files = []
    for p in root.rglob("*"):
        if p.is_file():
            if ".git" in p.parts:
                continue
            files.append(str(p.relative_to(root)))
    return files

@mcp.tool()
def read_file(path: str) -> str:
    """Read a file and return its content"""
    full_path = root / path 

    if not full_path.is_file():
        raise ToolError(f"This file path does not exist: {path}")
    return full_path.read_text()