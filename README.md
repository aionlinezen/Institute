# Task Manager Web App

A Flask-based task management application that saves tasks to a local JSON file.

## Features
- Add tasks with priority levels
- View tasks sorted by priority (ascending)
- Remove tasks
- Persistent storage in local file
- Web-based interface

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open browser to `http://localhost:5000`

## Testing
- Run CLI tests: `python -m unittest test_task_tracker.py`
- Run web app tests: `python -m unittest test_web_app.py`

## Files
- `app.py` - Flask web application
- `task_tracker.py` - Original CLI version
- `templates/index.html` - Web interface
- `tasks.json` - Task storage file (auto-created)