# mcp-code-explorer

MCP server in Python that lets AI clients list and read files within a sandboxed folder

## What it is 

* Model Context Protocol is a way to give a model context it doesn't have. It is also the standard for how an AI client and server talk. The servers, such as GitHub or Notion offer tools to the client side to find and call, which allows for any MCP client to use any MCP server eliminating the need for custom integration.
* This is an MCP server written in python that allows AI clients to list and read files within a sandboxed folder

## Tools

* Two main functions in this server: list_files and read_file
* In list_files, this collects a list of files that are within the scope of the project and returns relative paths, excluding the .git folder
* In read_file, takes in a single path that is requested from the client and returns the contents of the file as a string, restricting file paths that are not within the scope of the project

## Security Design

* Paths are resolved and must stay inside the project folder, paths outside the project such as /etc/passwd and ../../.ssh/id_rsa are restricted
* The access check runs before the existence check to prevent attackers from learning which files exist outside the project
* Paths relative to the project are returned so AI never sees username or folder layout
* Errors go through a `ToolError` so only intended messages reach the client
* When testing, Claude itself refused the SSH path, but the server enforces the boundary regardless of what the client decides.
* Symlinks pointing outside the project are blocked, because paths are resolved before the check.

## Setup

1. Clone the repo

   1. `git clone https://github.com/AntoanNgu/mcp-code-explorer.git`
   2. Run `cd mcp-code-explorer`to be in the correcr folder
2. Create and activate a virtual environment

   1. `python3 -m venv .venv`
   2. `source .venv/bin/activate`
3. Install the SDK

   1. `pip install -r requirements.txt`
   2. `python -c "import mcp; print('ok')"` to check that it worked
4. Edit `root`in server.py to point at your own project folder
5. Test with `mcp dev server.py`
6. To run in Claude Desktop

   1. Open Claude Desktop
   2. Settings -> Developer -> Edit Config
   3. Open the file titled `claude_desktop_config.json`
   4. App needs two things, the exact python and the full path to server.py

      1. run these two in terminal `which python` and `pwd`
      2. Take the path and paste into .json
      3. If the config file already has content, add the `mcpServers`section alongside it rather than replacing the file, then fully quit and reopen Claude Desktop.

      ```json
      {
        "mcpServers": {
          "code-explorer": {
            "command": "/path/to/mcp-code-explorer/.venv/bin/python",
            "args": ["/path/to/mcp-code-explorer/server.py"]
          }
        }
      }
      ```



## Demo

Claude lists project files using `list_files`:

![Claude lists project files](Screenshots/list-files.PNG)

Claude reads a files using `read_file` :

![Claude reads evals.md](Screenshots/read-file.PNG)

The server blocks a path outside the project:

![Access denied](Screenshots/access-denied.PNG)

## Limitations

* Root is hardcoded to my own path, so anyone cloning must edit root to their own path
* `list_files`returns every file except `.git`, folders like `node_modules/`or `.venv/` would flood claude with thousands of irrelevant paths
* Works for any text files, but binary files aren't supported: `.read_text()`fails on images.
* Very large files get read with no limitation
* No subfolder option, so Claude can't narrow its veiw to one part of a large project
* No search tool
