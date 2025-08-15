import typer
from typing import Optional
from datetime import datetime
import jason
from pathlib import Path

app = typer.Typer()

class Task:
    def __init__(self,id : int, title: str, priority: str = "medium",due: optional[str] = None):
        self.id = id
        self.title = title
        self.priority = priority.lower()
        self.due = due
        self.status = "pending"
        self.created_at = datetime.now().isoformat().split(".")


@app.command()
def add( title: str = typer.argument()