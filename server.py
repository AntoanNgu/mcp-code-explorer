from mcp.server import MCPServer
from pathlib import Path
from mcp.server.mcpserver.exceptions import ToolError

import os

mcp = MCPServer("code-explorer")


blocked_names = {".env", ".envrc", "id_rsa", "credentials.json"}
blocked_suffixes = {".pem", ".key"}
blocked_directories = {".git", ".venv", "node_modules"}


def is_blocked(rel_path):
    if rel_path.name in blocked_names:
        return True
    if rel_path.suffix in blocked_suffixes:
        return True
    for part in rel_path.parts:
        if part in blocked_directories:
            return True
    return False


def get_root():
    value = os.environ.get("CODE_EXPLORER_ROOT")
    if value is None:
        raise RuntimeError(
            "CODE_EXPLORER_ROOT isn't set, Set it to a project folder you want to explore"
        )
    path = Path(value)

    if not path.is_dir():
        raise RuntimeError(f"Folder path is incorrect: {path} ")

    return path.resolve()


@mcp.tool()
def list_files() -> list[str]:
    """Lists files relative to the project folder. Hides secrets (like .env and key files) and dependency or version-control folders (.git, .venv, node_modules)."""
    root = get_root()

    files = [
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and not is_blocked(p.relative_to(root))
    ]
    return files


@mcp.tool()
def read_file(path: str) -> str:
    """Read a file and return its content, protected files and binary files are refused"""
    root = get_root()
    full_path = (root / path).resolve()

    if not full_path.is_relative_to(root):
        raise ToolError(f"Access denied: {path} is outside the project")

    if is_blocked(full_path.relative_to(root)):
        raise ToolError(f"Access denied: {path} is a protected file")

    if not full_path.is_file():
        raise ToolError(f"This file path does not exist: {path}")

    try:
        return full_path.read_text()
    except UnicodeDecodeError:
        raise ToolError("Can not show binary files")


if __name__ == "__main__":
    get_root()
    mcp.run()
