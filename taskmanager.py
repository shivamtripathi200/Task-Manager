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
    
def save_data(data:dict):
    with open(DB_FILE,"w") as f:
        json.dump(data, f, indent = 4)

def load_data():
    if not DB_FILE.exists():
        initialdata = {"tasks":[],"next_id":1}
        save_data(initialdata)
        return initialdata
    with open(DB_FILE,"r") as f:
        return json.load(f)


@app.command(help="function to insert a task")
def edit(
    title: str = typer.Argument(),
    priority: str = typer.Option("medium"),
    due:Optional[str] = typer.Option(None)
):
    T = Task(id = 1, title = title, priority = priority, due = due)
    save_data(T.to_dict())
    print(f"task added successfully {title}")

@app.command()
def list():
    print(json.dumps(load_data(), indent=4))

@app.command()
def add(
    title: str = typer.Argument(),
    priority: str = typer.Option("medium"),
    due:Optional[str] = typer.Option(None)
):
    data = load_data()
    data_base_task = data["tasks"]
    next_id = data.get("next_id",1)
    next_id +=1
    temp = Task(id = next_id , title= title,priority=priority,due=due)
    data_base_task.append(temp.to_dict())
    save_data(data)



    

if __name__ == "__main__":
    app()
