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

## Why This Matters
- A real-world example of how MCP tools can be designed and used
- Enables LLMs to take action through structured, usable commands
- Keeps task data local, lightweight, and privacy-friendly
- Can be easily extended with new tools
- Ideal for experimenting with agent workflows and tool integration
