from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

class Task:
    def __init__(self, name, priority, task_id=None):
        self.name = name
        self.priority = int(priority)
        self.id = task_id
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'priority': self.priority}

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task(t['name'], t['priority'], t['id']) for t in data['tasks']]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
                self.next_id = 1
    
    def save_tasks(self):
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'next_id': self.next_id
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)
    
    def add_task(self, name, priority):
        task = Task(name, priority, self.next_id)
        self.next_id += 1
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x.priority)
        self.save_tasks()
    
    def get_tasks(self):
        return self.tasks
    
    def remove_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

manager = TaskManager()

@app.route('/')
def index():
    return render_template('index.html', tasks=manager.get_tasks())

@app.route('/add', methods=['POST'])
def add_task():
    name = request.form.get('name', '').strip()
    priority = request.form.get('priority', '')
    
    if not name:
        return redirect(url_for('index'))
    
    try:
        manager.add_task(name, priority)
    except ValueError:
        pass
    
    return redirect(url_for('index'))

@app.route('/remove/<int:task_id>')
def remove_task(task_id):
    manager.remove_task(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)