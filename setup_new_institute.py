#!/usr/bin/env python3
"""
Quick setup script for new coaching institutes
This script helps quickly replicate the setup for new institutions
"""

import os
import shutil
import sqlite3
from werkzeug.security import generate_password_hash
import json

def setup_new_institute():
    """Interactive setup for new institute"""
    print("=== Coach Institute SaaS - New Institute Setup ===")
    print()
    
    # Get institute details
    institute_name = input("Enter Institute Name: ")
    username = input("Enter Username (for URL): ").lower().replace(" ", "")
    admin_email = input("Enter Admin Email: ")
    password = input("Enter Admin Password: ")
    upi_id = input("Enter UPI ID (optional): ")
    
    # Database setup
    db_name = f"coach_saas_{username}.db"
    
    if os.path.exists(db_name):
        overwrite = input(f"Database {db_name} exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Initialize database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            institute_name TEXT NOT NULL,
            offer_text TEXT,
            upi_id TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institute_id INTEGER,
            why_choose_us TEXT,
            pdf_title TEXT,
            pdf_filename TEXT,
            testimonials TEXT,
            FOREIGN KEY (institute_id) REFERENCES institutes (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institute_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            payment_status TEXT DEFAULT 'pending',
            payment_id TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (institute_id) REFERENCES institutes (id)
        )
    ''')
    
    # Insert institute data
    cursor.execute('''
        INSERT INTO institutes (username, password_hash, institute_name, email, upi_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, generate_password_hash(password), institute_name, admin_email, upi_id))
    
    institute_id = cursor.lastrowid
    
    # Default configuration
    default_why_choose_us = "Quality Education\nExperienced Faculty\nProven Track Record\nPersonalized Attention"
    default_testimonials = json.dumps([
        {
            "name": "Sample Student",
            "text": "Great coaching institute with excellent faculty and results!",
            "image": ""
        }
    ])
    
    cursor.execute('''
        INSERT INTO configurations (institute_id, why_choose_us, pdf_title, testimonials)
        VALUES (?, ?, ?, ?)
    ''', (institute_id, default_why_choose_us, "Download Sample Papers", default_testimonials))
    
    conn.commit()
    conn.close()
    
    # Create uploads directory
    uploads_dir = f"uploads_{username}"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Generate environment file
    env_content = f"""# Environment variables for {institute_name}
SECRET_KEY=your-secret-key-{username}
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
DATABASE_NAME={db_name}
UPLOADS_FOLDER={uploads_dir}
INSTITUTE_USERNAME={username}
"""
    
    with open(f".env_{username}", "w") as f:
        f.write(env_content)
    
    # Generate custom app file
    app_content = f"""# Custom app for {institute_name}
from coach_saas_app import *
import os

# Override configurations
app.config['DATABASE_NAME'] = '{db_name}'
app.config['UPLOAD_FOLDER'] = '{uploads_dir}'
app.config['INSTITUTE_USERNAME'] = '{username}'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
"""
    
    with open(f"app_{username}.py", "w") as f:
        f.write(app_content)
    
    print(f"\n=== Setup Complete! ===")
    print(f"Institute: {institute_name}")
    print(f"Username: {username}")
    print(f"Database: {db_name}")
    print(f"Uploads: {uploads_dir}")
    print(f"Environment: .env_{username}")
    print(f"App file: app_{username}.py")
    print(f"\nInstitute URL: /institute/{username}")
    print(f"Admin Login: /admin/login")
    print(f"\nTo run: python app_{username}.py")
    print()
    
    # Generate deployment instructions
    deployment_instructions = f"""# Deployment Instructions for {institute_name}

## Render Deployment
1. Create new web service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements_saas.txt`
4. Set start command: `python app_{username}.py`
5. Add environment variables from .env_{username}

## Environment Variables
- SECRET_KEY: Generate a secure random key
- SENDER_EMAIL: Your Gmail address for notifications
- SENDER_PASSWORD: Gmail app password
- DATABASE_NAME: {db_name}
- UPLOADS_FOLDER: {uploads_dir}
- INSTITUTE_USERNAME: {username}

## GitHub Setup
1. Create new repository: {username}-coaching-institute
2. Upload all files including:
   - coach_saas_app.py
   - app_{username}.py
   - templates/
   - requirements_saas.txt
   - {db_name}
   - {uploads_dir}/

## Custom Domain (Optional)
1. Purchase domain: {username}coaching.com
2. Configure DNS to point to Render app
3. Add custom domain in Render dashboard

## Admin Access
- URL: https://your-app.onrender.com/admin/login
- Username: {username}
- Password: [as set during setup]
"""
    
    with open(f"DEPLOYMENT_{username}.md", "w") as f:
        f.write(deployment_instructions)
    
    print(f"Deployment instructions saved to: DEPLOYMENT_{username}.md")

def create_institute_package():
    """Create a complete package for new institute"""
    username = input("Enter institute username: ")
    
    # Create directory structure
    package_dir = f"institute_{username}_package"
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy necessary files
    files_to_copy = [
        "coach_saas_app.py",
        "payment_service.py",
        "requirements_saas.txt",
        "render.yaml",
        "Procfile_saas"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
    
    # Copy templates directory
    if os.path.exists("templates"):
        shutil.copytree("templates", os.path.join(package_dir, "templates"), dirs_exist_ok=True)
    
    print(f"\nPackage created in: {package_dir}")
    print("This package contains all files needed for deployment.")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Setup new institute")
    print("2. Create deployment package")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        setup_new_institute()
    elif choice == "2":
        create_institute_package()
    else:
        print("Invalid choice")