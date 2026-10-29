from mcp.server import MCPServer
from pathlib import Path
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("code-explorer")
root = Path("/Users/antoannguyen/devflow-ai").resolve()

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
    full_path = (root / path).resolve()

    if not full_path.resolve().is_relative_to(root):
        raise ToolError(f"Access denied: {path} is outside the project")

    if not full_path.resolve().is_file():
            raise ToolError(f"This file path does not exist: {path}")

    return full_path.read_text()

if __name__ == "__main__":
     mcp.run()