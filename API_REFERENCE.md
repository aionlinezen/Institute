# Task Manager API Reference

## Core Classes

### Task Class

#### Constructor
```python
Task(name: str, priority: int, task_id: int = None)
```

**Parameters:**
- `name`: Task description
- `priority`: Priority level (lower = higher priority)
- `task_id`: Unique identifier (optional, web version only)

**Raises:**
- `ValueError`: If priority cannot be converted to integer

#### Methods

##### `to_dict() -> dict`
Converts task to dictionary format for JSON serialization.

**Returns:**
```python
{
    'id': int,
    'name': str, 
    'priority': int
}
```

##### `__str__() -> str`
String representation of task.

**Returns:** `"[priority {priority}] {name}"`

### TaskManager Class

#### Constructor
```python
TaskManager(filename: str = 'tasks.json')
```

**Parameters:**
- `filename`: JSON file path for persistence

#### Methods

##### `add_task(name: str, priority: int) -> None`
Adds task and maintains priority sorting.

**Parameters:**
- `name`: Task description
- `priority`: Priority level

**Side Effects:**
- Appends task to internal list
- Sorts tasks by priority (ascending)
- Saves to file (web version)
- Increments next_id counter (web version)

##### `remove_task(index: int) -> None` (CLI version)
Removes task by list index.

**Parameters:**
- `index`: Zero-based list position

**Raises:**
- `IndexError`: If index out of range

##### `remove_task(task_id: int) -> None` (Web version)
Removes task by unique ID.

**Parameters:**
- `task_id`: Task identifier

**Side Effects:**
- Filters task from list
- Saves updated list to file

##### `list_tasks() -> None` (CLI version)
Prints formatted task list to console.

**Output Format:**
```
1. [priority 1] High priority task
2. [priority 3] Medium priority task
```

##### `get_tasks() -> List[Task]` (Web version)
Returns current task list.

**Returns:** List of Task objects sorted by priority

##### `load_tasks() -> None` (Web version)
Loads tasks from JSON file.

**Side Effects:**
- Populates tasks list from file
- Sets next_id counter
- Creates empty list if file missing/corrupted

##### `save_tasks() -> None` (Web version)
Persists tasks to JSON file.

**File Format:**
```json
{
    "tasks": [{"id": 1, "name": "Task", "priority": 2}],
    "next_id": 2
}
```

## Flask Routes

### GET /
**Purpose:** Main application page

**Response:** HTML template with task list

**Template Variables:**
- `tasks`: List of Task objects

### POST /add
**Purpose:** Add new task

**Form Parameters:**
- `name` (required): Task description
- `priority` (required): Integer priority

**Validation:**
- Strips whitespace from name
- Rejects empty names
- Converts priority to integer

**Response:** Redirect to main page

**Error Handling:**
- Invalid priority: Silently ignored
- Empty name: Silently ignored

### GET /remove/<int:task_id>
**Purpose:** Remove specific task

**URL Parameters:**
- `task_id`: Integer task identifier

**Response:** Redirect to main page

## Data Structures

### Task Storage Format
```python
# In-memory representation
Task(name="Example", priority=2, task_id=1)

# JSON file format
{
    "id": 1,
    "name": "Example", 
    "priority": 2
}
```

### File Structure
```json
{
    "tasks": [
        {"id": 1, "name": "Task 1", "priority": 1},
        {"id": 2, "name": "Task 2", "priority": 3}
    ],
    "next_id": 3
}
```

## Error Codes & Exceptions

### ValueError
**Cause:** Invalid priority conversion
```python
Task("test", "invalid_priority")  # Raises ValueError
```

### IndexError  
**Cause:** Invalid task index (CLI version)
```python
manager.remove_task(999)  # Raises IndexError if index doesn't exist
```

### JSONDecodeError
**Cause:** Corrupted JSON file
**Handling:** Falls back to empty task list

### KeyError
**Cause:** Missing JSON structure keys
**Handling:** Falls back to empty task list

## Usage Examples

### Basic Task Operations
```python
# Create manager
manager = TaskManager()

# Add tasks
manager.add_task("High priority", 1)
manager.add_task("Low priority", 5)

# Tasks automatically sorted: [priority 1] then [priority 5]

# Remove task (CLI)
manager.remove_task(0)  # Removes first task

# Remove task (Web)
manager.remove_task(task_id=1)  # Removes task with ID 1
```

### Web Application Usage
```python
from flask import Flask
from app import app, manager

# Start server
app.run(host='0.0.0.0', port=5000)

# Add task via POST request
# POST /add with form data: name="Test", priority="2"

# Remove task via GET request  
# GET /remove/1 (removes task with ID 1)
```

### File Persistence
```python
# Tasks automatically saved on add/remove (web version)
manager.add_task("Persistent task", 3)
# Creates/updates tasks.json

# Load existing tasks
new_manager = TaskManager("existing_tasks.json")
# Automatically loads tasks from file
```