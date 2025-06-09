# MCP Task Manager

This Task Management MCP Server project helps you manage personal tasks and to-dos — through a simple set of commands and a JSON-powered backend. Built for real-world practicality and seamless integration with any MCP-compatible client (like Claude Desktop or your custom LLM like ChatGroq client).

## Features
This server provides a toolbox of essential task management capabilities:
	•	Add Tasks — Add new tasks with a title, description, and priority
	• List Tasks — View all tasks or filter by status (pending or completed)
	• Complete Tasks — Mark a task as completed
	• Delete Tasks — Remove a task from the list
	• Get Stats — See task statistics (e.g. total, completed, pending)
Data is stored persistently in a tasks.json file, so to-dos survive restarts.

## How It Works
Each tool is implemented as an MCP-compatible function:
	•	add_task: Adds a task with required fields
	•	list_tasks: Lists tasks, supports filtering
	•	complete_task: Marks a task as completed
	•	delete_task: Deletes a task from storage
	•	get_stats: Returns a summary of current task counts
You can call these via:
	•	An MCP client like Claude Desktop, or
	•	A custom client (like client.py) using your Groq API Key

## Using the Client (ChatGroq)
The client.py file connects to the MCP server using a language model via Groq’s API. Just ask it to:
	•	“Add a high priority task to fix bugs in the app”
	•	“List my pending tasks”
	•	“Mark task 3 as completed”
	•	“Delete task 4”
	•	“Show task stats”
It’ll do the rest, using the tools defined in the MCP server.

## Why This Matters
	•	A real-world example of how MCP tools can be designed and used.
	• Enables LLMs to take action through structured, usable commands.
	• Keeps task data local, lightweight, and privacy-friendly.
	• Can be easily extended with new tools.
	• Ideal for experimenting with agent workflows and tool integration.
