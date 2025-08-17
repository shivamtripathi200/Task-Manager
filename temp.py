# task_manager_simple.py

import typer
import json
from datetime import datetime
from pathlib import Path
from typing import  Optional

# --- Configuration & State ---

# Initialize Typer app
app = typer.Typer(help="A simple command-line based task manager. ✅")

# Path to the JSON database file
DB_FILE = Path("tasks.json")


# --- Helper Functions for Data Storage ---

def load_data() -> dict:
    """Loads tasks from the JSON file. Creates the file if it doesn't exist."""
    if not DB_FILE.exists():
        # Create a default structure if the file is new
        initial_data = {"tasks": [], "next_id": 1}
        save_data(initial_data)
        return initial_data
    # No error handling for corrupted file
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data: dict):
    """Saves the current state of tasks to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- CLI Commands ---

@app.command(name="add", help="Add a new task.")
def add_task(
    title: str = typer.Argument(..., help="The title of the task."),
    priority: str = typer.Option("medium", "--priority", "-p", help="Priority of the task (low, medium, high)."),
    due: Optional[str] = typer.Option(None, "--due", "-d", help="Due date in YYYY-MM-DD format."),
):
    """Adds a new task to the list."""
    if priority.lower() not in ["low", "medium", "high"]:
        print("Error: Priority must be 'low', 'medium', or 'high'.")
        raise typer.Exit(code=1)

    data = load_data()
    tasks = data.get("tasks", [])
    next_id = data.get("next_id", 1)

    new_task = {
        "id": next_id,
        "title": title,
        "priority": priority.lower(),
        "due_date": due,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    data["next_id"] += 1
    save_data(data)
    
    print(f"🚀 Task #{next_id} added successfully: '{title}'")

@app.command(name="list", help="List all tasks.")
def list_tasks(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (pending, completed)."),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority (low, medium, high)."),
):
    """Displays a list of tasks, with optional filters."""
    data = load_data()
    tasks = data.get("tasks", [])

    if not tasks:
        print("No tasks found. Add one with 'task add'!")
        return

    # Apply filters
    filtered_tasks = tasks
    if status:
        filtered_tasks = [t for t in filtered_tasks if t['status'] == status.lower()]
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t['priority'] == priority.lower()]

    if not filtered_tasks:
        print("No tasks match the specified filters.")
        return

    # Create and display a simple text table
    print("\n--- Your To-Do List ---")
    print(f"{'ID':<4} | {'Title':<30} | {'Status':<12} | {'Priority':<10} | {'Due Date':<12}")
    print("-" * 80)

    for task in filtered_tasks:
        due_date_str = task['due_date'] if task['due_date'] else "N/A"
        
        # Add a checkmark for completed tasks
        title = task['title']
        if task['status'] == 'completed':
            title += " (✓)"

        # Truncate long titles to fit the column
        title_short = (title[:27] + '...') if len(title) > 30 else title
        
        print(
            f"{task['id']:<4} | {title_short:<30} | {task['status']:<12} | "
            f"{task['priority']:<10} | {due_date_str:<12}"
        )

@app.command(name="update", help="Update an existing task.")
def update_task(
    task_id: int = typer.Argument(..., help="The ID of the task to update."),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="The new title."),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="The new priority."),
    due: Optional[str] = typer.Option(None, "--due", "-d", help="The new due date."),
):
    """Finds a task by its ID and updates its properties."""
    data = load_data()
    tasks = data.get("tasks", [])
    task_to_update = next((t for t in tasks if t['id'] == task_id), None)

    if not task_to_update:
        print(f"Error: Task with ID #{task_id} not found.")
        raise typer.Exit(code=1)

    updated = False
    if title:
        task_to_update['title'] = title
        updated = True
    if priority:
        if priority.lower() not in ["low", "medium", "high"]:
            print("Error: Priority must be 'low', 'medium', or 'high'.")
            raise typer.Exit(code=1)
        task_to_update['priority'] = priority.lower()
        updated = True
    if due:
        task_to_update['due_date'] = due
        updated = True

    if updated:
        save_data(data)
        print(f"✅ Task #{task_id} updated successfully.")
    else:
        print("No changes provided. Nothing to update.")

@app.command(name="complete", help="Mark a task as complete.")
def complete_task(task_id: int = typer.Argument(..., help="The ID of the task to complete.")):
    """Marks a task's status as 'completed'."""
    data = load_data()
    tasks = data.get("tasks", [])
    task_to_complete = next((t for t in tasks if t['id'] == task_id), None)

    if not task_to_complete:
        print(f"Error: Task with ID #{task_id} not found.")
        raise typer.Exit(code=1)

    if task_to_complete['status'] == 'completed':
        print(f"Task #{task_id} is already marked as complete.")
    else:
        task_to_complete['status'] = 'completed'
        save_data(data)
        print(f"🎉 Task #{task_id} marked as complete!")


@app.command(name="delete", help="Delete a task.")
def delete_task(task_id: int = typer.Argument(..., help="The ID of the task to delete.")):
    """Removes a task from the list permanently."""
    data = load_data()
    tasks = data.get("tasks", [])
    
    initial_len = len(tasks)
    data['tasks'] = [t for t in tasks if t['id'] != task_id]
    
    if len(data['tasks']) == initial_len:
        print(f"Error: Task with ID #{task_id} not found.")
        raise typer.Exit(code=1)
        
    save_data(data)
    print(f"🗑 Task #{task_id} has been deleted.")

if _name_ == "_main_":
    app()
    
    
    
    
    
    
    
    
    
def update(update_id: int, title: Optional[str] = None, priority: Optional[str] = None, due: Optional[str] = None):
    if priority.lower() not in ["high", "medium", "low"]:
        typer.echo("Priority must be high, medium or low")
        raise typer.Exit(code=1)
    
    data = load_data()
    tasks=data["tasks"] 
    task_to_update = None
    for task in tasks:
        if task["id"] == update_id:
            task_to_update = task
            break   
     
    if title:
        task_to_update["title"] = title
    if priority:
        task_to_update["priority"] = priority.lower()
    if due:
        task_to_update["due"] = due
        
    save_data(data) 
    typer.echo(f"Task with id {update_id} updated.")