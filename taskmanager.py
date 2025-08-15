import typer
from typing import Optional
from datetime import datetime
import json
from pathlib import Path

app = typer.Typer()

DB_FILE = Path("tasks.json")

class Task:
    def __init__(self,id : int, title: str, priority: str = "medium",due: Optional[str] = None):
        self.id = id
        self.title = title
        self.priority = priority.lower()
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
    
def load_data():
    with open(DB_FILE,"r") as f:
        return json.load(f)
def save_data(data:dict):
    with open(DB_FILE,"w") as f:
        json.dump(data, f, indent = 4)

@app.command(help="function to insert a task")
def add(
    title: str = typer.Argument(),
    priority: str = typer.Option(),
    due:Optional[str] = typer.Option()
):
    T = Task(id = 1, title = title, priority = priority, due = due)
    save_data(T.to_dict())
    print(f"task added successfully {title}")

@app.command()
def list():
    print(json.dumps(load_data(), indent=4))


@app.command()
def edit(title: Optional[str], priority: Optional[str], status: Optional[str],due: Optional[str]):
    

if __name__ == "__main__":
    app()
