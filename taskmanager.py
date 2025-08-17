import typer
from typing import Optional
from datetime import datetime
import json
from pathlib import Path
import csv

app = typer.Typer(help="A simple command-line based task manager. ✅")

DB_FILE = Path("tasks.json")

class Task:
    def __init__(self,id : int, title: str, priority: str = "medium",due: Optional[str] = None):
        self.id = id
        self.title = title
        self.priority = priority
        self.due = due
        self.status = "pending"
        self.created_at = datetime.now().isoformat().split(".")
    def to_dict(self):
        return{
            "id": self.id,
            "title":self.title,
            "priority":self.priority,
            "due": self.due,
            "status": self.status,
            "created_at": self.created_at
        }
    
def save_data(data:dict):
    with open(DB_FILE,"w") as f:
        json.dump(data, f, indent = 4)

def load_data():

    if  not DB_FILE.exists() or DB_FILE.stat().st_size == 0:
        initialdata = {"tasks":[],"next_id":1}
        save_data(initialdata)
        return initialdata
    with open(DB_FILE,"r") as f:
        return json.load(f)


@app.command(help="update [id] title")
def update(
    update_id : int = typer.Argument(),
    title: Optional[str] = None,
    priority: Optional[str] =None,
    due:Optional[str] = None
):
    if priority not in ["low", "medium", "high"]:
        typer.echo("Error: Priority must be 'low', 'medium', or 'high'.")
        raise typer.Exit(code=1)
    data = load_data()
    tasks = data["tasks"]
    for t in tasks:
        if t["id"] == update_id:
            temp_task = t
            break
    
    if title:
        temp_task["title"] = title
    if priority:
        temp_task["priority"] = priority
    if due:
        temp_task["due"] = due
    
    save_data(data)


@app.command(help = "completed [id]")
def completed(
    id: int = typer.Argument(),
):
    data = load_data()
    tasks = data["tasks"]
    temp = None
    for task in tasks:
        if task["id"] == id :
            temp = task
            print("task updated")
            break
    temp["status"] = "completed"
    save_data(data)


@app.command(help="list --priority [option] --status [option]")
def list(
    priority: str = typer.Option(None, help="Priority of the task (low, medium, high)."),
    status: str = typer.Option(None, help="status of the task")
):
    data = load_data()
    tasks = data["tasks"]
    if  priority in ["low", "medium","high"] :
        for task in tasks:
            if task["priority"]== priority:
                typer.echo(json.dumps(task,indent = 4))
    
    if status:
        for task in tasks:
            if task["status"] == status:
                typer.echo(json.dumps(task,indent=4))

    if not priority and not status:
        typer.echo(json.dumps(tasks,indent=4))
    
        

    

@app.command(help="add [argument] --priority [argument] --due [argument]")
def add(
    title: str = typer.Argument(..., help="The title of the task."),
    priority: str = typer.Option("medium", help="Priority of the task (low, medium, high)."),
    due:Optional[str] = typer.Option(None, help="Due date in DD-MM-YYYY(optional) format.")
):
    if priority not in ["low", "medium", "high"]:
        typer.echo("Error: Priority must be 'low', 'medium', or 'high'.")
        raise typer.Exit(code=1)
    data = load_data()
    data_base_task = data["tasks"]
    next_id = data.get("next_id")
    temp = Task(id = next_id , title= title,priority=priority,due=due)
    next_id +=1
    data["next_id"] = next_id
    data_base_task.append(temp.to_dict())
    save_data(data)


@app.command(help="Delete a task.")
def delete(delete_id: int):
    data = load_data()
    tasks = data["tasks"]
    task_to_delete = None
    for t in tasks:
        if t["id"] == delete_id:
            task_to_delete = t
            break
    
    if task_to_delete:
        tasks.remove(task_to_delete)
        save_data(data)
        typer.echo(f"Task with id{delete_id} deleted.")
    else:
        typer.echo(f"No task found with id{delete_id}.")
    

@app.command()
def exportcsv(filename: str = typer.Argument("tasks.csv", help="CSV filename to export all tasks")):
    data = load_data()
    tasks = data.get("tasks", [])

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "priority", "due", "status", "created_at"])
        writer.writeheader()
        writer.writerows(tasks)

    typer.echo(f"Exported all {len(tasks)} tasks to {filename}")
    

if __name__ == "__main__":
    app()
