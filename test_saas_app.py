#!/usr/bin/env python3
"""
Test script for Coach Institute SaaS Platform
"""

import unittest
import json
import os
import tempfile
from coach_saas_app import app, init_db

class CoachSaaSTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            init_db()
    
    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_landing_page(self):
        """Test landing page loads"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Coach Institute SaaS Platform', rv.data)
    
    def test_admin_register(self):
        """Test admin registration"""
        rv = self.app.post('/admin/create', data={
            'username': 'testinstitute',
            'password': 'testpass123',
            'institute_name': 'Test Institute',
            'email': 'test@example.com'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
    
    def test_admin_login(self):
        """Test admin login"""
        # First create an institute
        self.app.post('/admin/create', data={
            'username': 'testinstitute',
            'password': 'testpass123',
            'institute_name': 'Test Institute',
            'email': 'test@example.com'
        })
        
        # Then try to login
        rv = self.app.post('/admin/authenticate', data={
            'username': 'testinstitute',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
    
    def test_institute_page(self):
        """Test institute public page"""
        # Create institute first
        self.app.post('/admin/create', data={
            'username': 'testinstitute',
            'password': 'testpass123',
            'institute_name': 'Test Institute',
            'email': 'test@example.com'
        })
        
        # Access institute page
        rv = self.app.get('/institute/testinstitute')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Test Institute', rv.data)
    
    def test_student_registration(self):
        """Test student registration"""
        # Create institute first
        self.app.post('/admin/create', data={
            'username': 'testinstitute',
            'password': 'testpass123',
            'institute_name': 'Test Institute',
            'email': 'test@example.com'
        })
        
        # Register student
        rv = self.app.post('/register/testinstitute', data={
            'name': 'Test Student',
            'email': 'student@example.com',
            'phone': '1234567890'
        })
        self.assertEqual(rv.status_code, 200)
        
        # Check response
        data = json.loads(rv.data)
        self.assertTrue(data['success'])
        self.assertIn('registration_id', data)

def run_manual_tests():
    """Run manual tests for demonstration"""
    print("=== Coach Institute SaaS - Manual Tests ===")
    print()
    
    # Test 1: Database initialization
    print("1. Testing database initialization...")
    try:
        init_db()
        print("   ✓ Database initialized successfully")
    except Exception as e:
        print(f"   ✗ Database initialization failed: {e}")
    
    # Test 2: App startup
    print("2. Testing app startup...")
    try:
        with app.test_client() as client:
            rv = client.get('/')
            if rv.status_code == 200:
                print("   ✓ App starts successfully")
            else:
                print(f"   ✗ App startup failed with status {rv.status_code}")
    except Exception as e:
        print(f"   ✗ App startup failed: {e}")
    
    # Test 3: Template rendering
    print("3. Testing template rendering...")
    try:
        with app.test_client() as client:
            rv = client.get('/admin/login')
            if rv.status_code == 200 and b'Admin Login' in rv.data:
                print("   ✓ Templates render correctly")
            else:
                print("   ✗ Template rendering failed")
    except Exception as e:
        print(f"   ✗ Template rendering failed: {e}")
    
    print()
    print("Manual tests completed!")
    print()
    print("To run full tests: python -m unittest test_saas_app.py")
    print("To start app: python coach_saas_app.py")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'manual':
        run_manual_tests()
    else:
        unittest.main()