from mcp.server import MCPServer
from pathlib import Path

mcp = MCPServer("code-explorer")
root = Path("/Users/antoannguyen/devflow-ai")

@mcp.tool()
def list_files():
    """Lists files relative to the project folder, excluding the .git folder"""
    files = []
    for p in root.rglob("*"):
        if p.is_file():
            if ".git" in p.parts:
                continue
            files.append(str(p.relative_to(root)))
    return files
        