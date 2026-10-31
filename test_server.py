from server import read_file
from mcp.server.mcpserver.exceptions import ToolError
import pytest

def test_valid_read(monkeypatch, tmp_path):
    (tmp_path / "hello.txt").write_text("hi")
    monkeypatch.setenv("CODE_EXPLORER_ROOT", str(tmp_path))
    read = read_file("hello.txt")
    assert read == "hi"

def test_traversal_blocked(monkeypatch, tmp_path):
    monkeypatch.setenv("CODE_EXPLORER_ROOT", str(tmp_path))
    path = "../secret.txt"
    with pytest.raises(ToolError, match="outside the project"):
        read_file(path)

def test_env_blocked(monkeypatch, tmp_path):
    monkeypatch.setenv("CODE_EXPLORER_ROOT", str(tmp_path))
    file = ".env"
    with pytest.raises(ToolError, match="protected file"):
        read_file(file)

def test_file_existence(monkeypatch, tmp_path):
    monkeypatch.setenv("CODE_EXPLORER_ROOT", str(tmp_path))
    file = "notes.txt"
    with pytest.raises(ToolError, match="This file path does not exist"):
        read_file(file)

def test_binary(monkeypatch, tmp_path):
    (tmp_path / "hello.txt").write_bytes(b"\xff\xfe\x00")
    monkeypatch.setenv("CODE_EXPLORER_ROOT", str(tmp_path))
    file = "hello.txt"
    with pytest.raises(ToolError, match="Can not show binary files"):
        read_file(file)






