from typing import Any, Optional
import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(
    name="task-manager",
    host="localhost",
    port=8001
)

# Constants
TASKS_FILE = "tasks.json"

def load_tasks() -> list[dict]:
    """Load tasks from JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks: list[dict]) -> None:
    """Save tasks to JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2, default=str)

def get_next_id(tasks: list[dict]) -> int:
    """Get the next available task ID."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

@mcp.tool()
async def add_task(title: str, description: str = "", priority: str = "medium") -> str:
    """Add a new task.
    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: Task priority - low, medium, high (default: medium)
    """
    if priority not in ["low", "medium", "high"]:
        return "Error: Priority must be 'low', 'medium', or 'high'"
    
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return f"Task added successfully!"

@mcp.tool()
async def list_tasks(status: str = "all") -> str:
    """List tasks filtered by status.
    Args:
        status: Filter by status - 'all', 'pending', 'completed' (default: all)
    """
    if status not in ["all", "pending", "completed"]:
        return "Error: Status must be 'all', 'pending', or 'completed'"
    tasks = load_tasks()
    if status != "all":
        tasks = [task for task in tasks if task["status"] == status]
    if not tasks:
        return f"No {status} tasks found."
    # Sort by priority (high -> medium -> low) and then by creation date
    priority_order = {"high": 3, "medium": 2, "low": 1}
    tasks.sort(key=lambda x: (priority_order.get(x["priority"], 0), x["created_at"]), reverse=True)
    result = f"\n=== {status.upper()} TASKS ===\n"
    for task in tasks:
        status_icon = "✅" if task["status"] == "completed" else "⏳"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
        result += f"\n{status_icon} ID: {task['id']} | {priority_icon} {task['priority'].upper()}\n"
        result += f"  {task['title']}\n"
        if task['description']:
            result += f"  {task['description']}\n"
        result += f"  Created: {task['created_at'][:10]}\n"
        if task['completed_at']:
            result += f"  Completed: {task['completed_at'][:10]}\n"
        result += "  " + "-" * 40 + "\n"
    return result

@mcp.tool()
async def complete_task(task_id: int) -> str:
    """Mark a task as completed.
    Args:
        task_id: ID of the task to complete
    """
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "completed":
                return f"Task {task_id} is already completed!"
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            return f"Task {task_id} '{task['title']}' marked as completed! 🎉"
    return f"Task with ID {task_id} not found."

@mcp.tool()
async def delete_task(task_id: int) -> str:
    """Delete a task permanently.
    Args:
        task_id: ID of the task to delete
    """
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks(tasks)
            return f"Task {task_id} '{deleted_task['title']}' deleted successfully!"
    return f"Task with ID {task_id} not found."

@mcp.tool()
async def get_stats() -> str:
    """Get task statistics and summary."""
    tasks = load_tasks()
    if not tasks:
        return "No tasks found. Add some tasks to see statistics!"
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "completed"])
    pending_tasks = total_tasks - completed_tasks
    
    # Priority breakdown
    priority_counts = {"high": 0, "medium": 0, "low": 0}
    for task in tasks:
        if task["status"] == "pending":
            priority_counts[task["priority"]] += 1
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    result = f"""
        📊 TASK STATISTICS
        ==================
        📋 Total Tasks: {total_tasks}
        ✅ Completed: {completed_tasks}
        ⏳ Pending: {pending_tasks}
        📈 Completion Rate: {completion_rate:.1f}%

        🎯 PENDING TASKS BY PRIORITY:
        🔴 High Priority: {priority_counts['high']}
        🟡 Medium Priority: {priority_counts['medium']}
        🟢 Low Priority: {priority_counts['low']}
    """
    
    return result

@mcp.resource("config://tasks")
def get_task_config() -> str:
    """Get task management configuration."""
    return json.dumps({
        "task_file": TASKS_FILE,
        "supported_priorities": ["low", "medium", "high"],
        "supported_statuses": ["pending", "completed"]
    }, indent=2)

if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running Task Manager server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running Task Manager server with SSE transport on http://localhost:8001")
        print("Available endpoints:")
        print("  - SSE: http://localhost:8001/sse")
        print("  - Health: http://localhost:8001/health")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")