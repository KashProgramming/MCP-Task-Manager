# MCP Task Manager

This Task Management MCP Server helps manage personal tasks and to-dos through a simple set of MCP-compatible tools and a JSON-powered backend. It's built for real-world practicality and integrates seamlessly with any MCP-compatible client — like Claude Desktop or a custom LLM client using Groq.

## Features
A toolbox of essential task management capabilities:
- **Add Tasks** — Add new tasks with a title, description, and priority
- **List Tasks** — View all tasks or filter by status (pending or completed)
- **Complete Tasks** — Mark a task as completed
- **Delete Tasks** — Remove a task from the list
- **Get Stats** — See task statistics (e.g. total, completed, pending)
All data is stored persistently in a `tasks.json` file, so tasks survive restarts.

## How It Works
Each tool is implemented as an MCP-compatible function:
- `add_task` — Adds a task with required fields
- `list_tasks` — Lists tasks, supports filtering by status
- `complete_task` — Marks a task as completed
- `delete_task` — Deletes a task from storage
- `get_stats` — Returns a summary of current task counts

These tools can be triggered via:
- An MCP client like **Claude Desktop**
- A custom client (e.g. `client.py`) using the **Groq API**

## Using the Client (ChatGroq)
The `client.py` file acts as an LLM-powered interface. Just ask it to:
- “Add a high priority task to fix bugs in the app”
- “List my pending tasks”
- “Mark task 3 as completed”
- “Delete task 4”
- “Show task stats”
The client will handle the rest by invoking matching tools using structured MCP calls.

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/mcp-task-manager.git
cd mcp-task-manager
````

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MCP server for Claude Desktop
Claude Desktop uses a JSON config file to discover MCP servers.
Add an entry for this server inside your Claude MCP config.

**Linux/Mac**
```bash
mkdir -p ~/.config/Claude/mcp
nano ~/.config/Claude/mcp/tasks_config.json
```

**Windows (PowerShell)**
```powershell
mkdir $env:APPDATA\Claude\mcp -Force
notepad $env:APPDATA\Claude\mcp\tasks_config.json
```

Paste this into `tasks_config.json`:
```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/mcp-task-manager"
    }
  }
}
```
*(Replace `/absolute/path/to/mcp-task-manager` with the actual repo path.)*

### 5. Start the MCP server
From inside the repo:
```bash
python server.py
```
Claude Desktop will automatically connect to it the next time it starts.

### 6. (Optional) Test with client.py
You can run the provided client interface directly:
```bash
python client.py
```
