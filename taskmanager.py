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


@app.command(help="function to insert a task")
def edit(
    update_id : int = typer.Argument(),
    title: str = typer.Argument(None),
    priority: str = typer.Option(None),
    due:Optional[str] = typer.Option(None)
):
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
    next_id = data.get("next_id")
    temp = Task(id = next_id , title= title,priority=priority,due=due)
    next_id +=1
    data["next_id"] = next_id
    data_base_task.append(temp.to_dict())
    save_data(data)



    

if __name__ == "__main__":
    app()
