# Task Manager Web App - Complete Documentation

## Overview
A Flask-based task management application with both CLI and web interfaces. Tasks are stored persistently in JSON format with priority-based sorting.

## Architecture

### Core Components

#### 1. Task Class
```python
class Task:
    def __init__(self, name, priority, task_id=None)
```
- **Purpose**: Represents individual tasks
- **Attributes**:
  - `name`: Task description (string)
  - `priority`: Task priority (integer, lower = higher priority)
  - `id`: Unique identifier (web version only)

#### 2. TaskManager Class
```python
class TaskManager:
    def __init__(self, filename='tasks.json')
```
- **Purpose**: Manages task collection and persistence
- **Key Methods**:
  - `add_task(name, priority)`: Adds and sorts tasks
  - `remove_task(index/task_id)`: Removes tasks
  - `load_tasks()`: Loads from JSON file
  - `save_tasks()`: Saves to JSON file

## File Structure

```
code/
├── app.py                 # Flask web application
├── task_tracker.py        # CLI version
├── templates/
│   └── index.html        # Web interface template
├── test_task_tracker.py  # CLI tests
├── test_web_app.py       # Web app tests
├── requirements.txt      # Dependencies
├── tasks.json           # Data storage (auto-created)
└── README.md            # Basic setup guide
```

## API Documentation

### Web Routes

#### GET /
- **Purpose**: Display main task interface
- **Returns**: HTML page with task list and add form
- **Template**: `templates/index.html`

#### POST /add
- **Purpose**: Add new task
- **Parameters**:
  - `name` (required): Task description
  - `priority` (required): Integer priority value
- **Validation**: Strips whitespace, validates priority as integer
- **Response**: Redirects to main page

#### GET /remove/<task_id>
- **Purpose**: Remove specific task
- **Parameters**: `task_id` (URL parameter)
- **Response**: Redirects to main page

## Data Storage

### JSON Structure
```json
{
  "tasks": [
    {
      "id": 1,
      "name": "Task description",
      "priority": 3
    }
  ],
  "next_id": 2
}
```

### Priority System
- **Lower numbers = Higher priority**
- Tasks automatically sorted by priority (ascending)
- Example: Priority 1 appears before Priority 5

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Installation Steps
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run CLI version
python task_tracker.py

# 3. Run web version
python app.py
# Access at http://localhost:5000
```

### Dependencies
- **Flask 2.3.3**: Web framework
- **gunicorn 21.2.0**: WSGI server (production)

## Usage Examples

### CLI Interface
```bash
$ python task_tracker.py

Task Manager
1. Add Task
2. List Tasks
3. Remove Task
4. Exit
Choose an option: 1
Enter task name: Complete documentation
Enter task priority: 2
Task added.
```

### Web Interface
1. Navigate to `http://localhost:5000`
2. Fill task name and priority in form
3. Click "Add Task"
4. View sorted task list
5. Click "Remove" to delete tasks

## Testing

### Test Coverage

#### CLI Tests (`test_task_tracker.py`)
- Task creation validation
- Priority sorting
- Task removal
- Error handling

#### Web Tests (`test_web_app.py`)
- HTTP route responses
- Form submission
- Data persistence
- File operations

### Running Tests
```bash
# CLI tests
python -m unittest test_task_tracker.py

# Web app tests
python -m unittest test_web_app.py

# All tests
python -m unittest discover
```

## Error Handling

### Input Validation
- **Empty task names**: Ignored in web interface
- **Invalid priorities**: Caught with try/catch blocks
- **File corruption**: Graceful fallback to empty task list
- **Missing files**: Auto-creation on first save

### Exception Types
- `ValueError`: Invalid priority conversion
- `IndexError`: Invalid task index (CLI)
- `JSONDecodeError`: Corrupted data file
- `KeyError`: Missing JSON structure

## Performance Considerations

### Efficiency
- **O(n log n)** sorting on task addition
- **O(n)** task removal by ID
- **File I/O**: Only on add/remove operations
- **Memory**: All tasks loaded in memory

### Scalability Limits
- Suitable for personal use (< 1000 tasks)
- File-based storage limits concurrent access
- No pagination in web interface

## Security Notes

### Current Implementation
- No authentication/authorization
- Local file access only
- No input sanitization beyond basic validation
- Debug mode disabled in production

### Recommendations for Production
- Add user authentication
- Implement input sanitization
- Use database instead of JSON files
- Add CSRF protection
- Enable HTTPS

## Deployment

### Local Development
```bash
python app.py
# Runs on http://localhost:5000
```

### Production (Heroku-ready)
- `Procfile`: Configured for gunicorn
- `runtime.txt`: Python version specification
- Environment variable support for PORT

## Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
pip install -r requirements.txt
```

#### Port already in use
```bash
# Change port in app.py or set environment variable
export PORT=8000
python app.py
```

#### Tasks not persisting
- Check file permissions in project directory
- Verify `tasks.json` is created and writable

#### Priority sorting incorrect
- Ensure priority values are integers
- Lower numbers = higher priority (1 before 5)

## Future Enhancements

### Potential Features
- Task categories/tags
- Due dates and reminders
- Task completion status
- User accounts and sharing
- REST API endpoints
- Database backend
- Mobile-responsive design
- Task search and filtering

### Code Improvements
- Add type hints
- Implement logging
- Add configuration management
- Create proper error pages
- Add API documentation
- Implement caching