import typer
from typing import Optional
from datetime import datetime
import json
from pathlib import Path

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
            "created at": self.created_at
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


@app.command(help="Update an existing task.")
def update(
    update_id : int = typer.Argument(),
    title: str = typer.Argument(None),
    priority: str = typer.Option(None),
    due:Optional[str] = typer.Option(None)
):
    if priority.lower() not in ["low", "medium", "high"]:
        print("Error: Priority must be 'low', 'medium', or 'high'.")
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


@app.command(help = "update status for completed tasks")
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


@app.command(help="List all tasks.")
def list(
    priority: str = typer.Option(None, help="Priority of the task (low, medium, high)."),
    status: str = typer.Option(None, help="status of the task")
):
    if  priority == ["low", "medium","high"] :
        data = load_data()
        tasks = data["tasks"]
        for task in tasks:
            if task["priority"]== priority:
                print(json.dumps(task,indent = 4))
        

    

@app.command(help="Add a new task")
def add(
    title: str = typer.Argument(..., help="The title of the task."),
    priority: str = typer.Option("medium", help="Priority of the task (low, medium, high)."),
    due:Optional[str] = typer.Option(None, help="Due date in DD-MM-YYYY(optional) format.")
):
    if priority.lower() not in ["low", "medium", "high"]:
        print("Error: Priority must be 'low', 'medium', or 'high'.")
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
    


    

if __name__ == "__main__":
    app()
