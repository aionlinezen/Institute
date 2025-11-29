#!/usr/bin/env python3
"""
Simple startup script for Coach Institute SaaS
"""

from coach_saas_app import app, init_db
import os

def main():
    print("=== Coach Institute SaaS Platform ===")
    print("Initializing database...")
    
    try:
        init_db()
        print("✓ Database initialized successfully!")
        
        print("\nStarting Flask application...")
        print("Open your browser to: http://localhost:5000")
        print("Admin panel: http://localhost:5000/admin/login")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 40)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Flask is installed: pip install flask")
        print("2. Check if port 5000 is available")
        print("3. Run: python coach_saas_app.py directly")

if __name__ == '__main__':
    main()