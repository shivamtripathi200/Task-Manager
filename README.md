# 📋 Task Manager CLI

A simple *command-line based Task Manager* built with [Typer](https://typer.tiangolo.com/).  
This app allows you to *add, update, list, complete, delete, and export tasks* directly from the terminal.

---

## 🚀 Project Overview

This project is a *lightweight task management tool* designed for developers who prefer working in the terminal.  
It stores tasks in a local JSON file (tasks.json) and supports:

- ✅ Add new tasks with priority and due date  
- ✏ Update task details  
- ✔ Mark tasks as completed  
- 📜 List tasks (with filters for priority and status)  
- 🗑 Delete tasks  
- 📤 Export tasks to CSV  

---

## 🛠 Technologies Used

- *Python 3.8+*  
- **[Typer](https://typer.tiangolo.com/)** → for building CLI commands  
- *JSON* → for local storage  
- *CSV* → for exporting tasks  

---

## ⚙ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/task_manager.git
cd task_manager
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install typer[all]
```

### 4. Run the App
```bash
python taskmanager.py --help
```

---

## 📌 Available Commands

### ➕ Add a Task
```bash
python taskmanager.py add "Finish project" --priority high --due 20-08-2025
```

### 📝 Update a Task
```bash
python taskmanager.py update 1 --title "Finish ML project" --priority medium
```

### ✔ Mark Task as Completed
```bash
python taskmanager.py completed 1
```

### 📋 List Tasks
```bash
python taskmanager.py list                # List all tasks
python taskmanager.py list --priority high
python taskmanager.py list --status completed

```
### 🗑 Delete a Task
```bash
python taskmanager.py delete 2

```
### 📤 Export to CSV
```bash
python taskmanager.py exportcsv tasks.csv

```
---

## 📂 Project Structure

```
task_manager/
├── taskmanager.py   # Main CLI app
├── tasks.json       # Task database (auto-generated)
├── README.md        # Project documentation


```


## 📊 Sample Data Format

### tasks.json structure:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "priority": "high",
      "due": "25-08-2025",
      "status": "pending",
      "created_at": "17-08-2025 14:30:00"
    },
    {
      "id": 2,
      "title": "Review code changes",
      "priority": "medium",
      "due": "22-08-2025",
      "status": "completed",
      "created_at": "17-08-2025 15:45:00"
    }
  ]
}

```

---

## 🎯 Features

- *Priority Levels*: low, medium, high
- *Status Tracking*: pending, completed
- *Date Support*: Due dates in DD-MM-YYYY format
- *Filtering*: List tasks by priority or status
- *Export*: Export all tasks to CSV format
- *Auto-numbering*: Tasks get unique IDs automatically

---

## 📝 Usage Examples

### Quick Start
```bash
# Add a high-priority task
python taskmanager.py add "Deploy website" --priority high --due 30-08-2025

# List all pending tasks
python taskmanager.py list --status pending

# Mark task as completed
python taskmanager.py completed 1

# Export all tasks to CSV
python taskmanager.py exportcsv my_tasks.csv

```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



---

## 🐛 Issues & Support

If you encounter any issues or have suggestions, please [open an issue](https://github.com/your-username/task_manager/issues) on GitHub.

---

## 🔮 Future Enhancements

- [ ] Task categories/tags
- [ ] Recurring tasks
- [ ] Task search functionality
- [ ] Integration with calendar apps
- [ ] Task notifications/reminders
- [ ] Multi-user support

---

*Made with ❤ by [Shivam Tripathi](https://github.com/your-username)*
