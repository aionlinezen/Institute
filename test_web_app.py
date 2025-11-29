import unittest
import os
import json
from app import app, TaskManager

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.test_file = 'test_tasks.json'
        self.manager = TaskManager(self.test_file)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Manager', response.data)
    
    def test_add_task(self):
        response = self.app.post('/add', data={'name': 'Test Task', 'priority': '3'})
        self.assertEqual(response.status_code, 302)
        
        tasks = self.manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'Test Task')
    
    def test_file_persistence(self):
        self.manager.add_task('Persistent Task', 2)
        
        new_manager = TaskManager(self.test_file)
        tasks = new_manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'Persistent Task')

if __name__ == '__main__':
    unittest.main()