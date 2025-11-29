#!/usr/bin/env python3
"""
Demo setup script - Creates a sample institute for testing
"""

import sqlite3
from werkzeug.security import generate_password_hash
import json
import os

def create_demo_institute():
    """Create a demo institute for testing"""
    print("=== Creating Demo Institute ===")
    
    # Initialize database
    from coach_saas_app import init_db
    init_db()
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Check if demo institute already exists
    cursor.execute('SELECT id FROM institutes WHERE username = ?', ('demo',))
    if cursor.fetchone():
        print("Demo institute already exists!")
        print("Login details:")
        print("  URL: http://localhost:5000/institute/demo")
        print("  Admin: http://localhost:5000/admin/login")
        print("  Username: demo")
        print("  Password: demo123")
        conn.close()
        return
    
    # Create demo institute
    cursor.execute('''
        INSERT INTO institutes (username, password_hash, institute_name, offer_text, upi_id, email)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'demo',
        generate_password_hash('demo123'),
        'Excellence Coaching Institute',
        'Great opportunity to crack SSC exam for 2025 - 50% off!',
        'demo@paytm',
        'admin@excellence.com'
    ))
    
    institute_id = cursor.lastrowid
    
    # Create configuration
    why_choose_us = "Expert Faculty with 10+ years experience\nProven Track Record - 95% success rate\nPersonalized Attention - Small batch sizes\nComprehensive Study Material\nRegular Mock Tests"
    
    testimonials = json.dumps([
        {
            "name": "Rahul Sharma",
            "text": "Excellent coaching! I cleared SSC CGL in first attempt. The faculty is very supportive and the study material is comprehensive.",
            "image": ""
        },
        {
            "name": "Priya Singh", 
            "text": "Best institute for government exam preparation. The mock tests really helped me improve my speed and accuracy.",
            "image": ""
        }
    ])
    
    cursor.execute('''
        INSERT INTO configurations (institute_id, why_choose_us, pdf_title, testimonials)
        VALUES (?, ?, ?, ?)
    ''', (institute_id, why_choose_us, "Download Previous Year Papers", testimonials))
    
    conn.commit()
    conn.close()
    
    # Create uploads directory
    os.makedirs('uploads', exist_ok=True)
    
    print("[SUCCESS] Demo institute created successfully!")
    print("\nAccess Details:")
    print("  Institute Page: http://localhost:5000/institute/demo")
    print("  Admin Panel: http://localhost:5000/admin/login")
    print("  Username: demo")
    print("  Password: demo123")
    print("\nYou can now:")
    print("  1. View the institute landing page")
    print("  2. Test student registration")
    print("  3. Access admin panel to configure settings")
    print("  4. Upload PDFs and manage testimonials")

if __name__ == '__main__':
    create_demo_institute()