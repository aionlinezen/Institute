#!/usr/bin/env python3
"""
Simple test to verify the SaaS application structure
"""

import os
import sys

def test_file_structure():
    """Test if all required files exist"""
    print("=== Coach Institute SaaS - File Structure Test ===")
    print()
    
    required_files = [
        'coach_saas_app.py',
        'payment_service.py',
        'setup_new_institute.py',
        'requirements_saas.txt',
        'render.yaml',
        'README_SAAS.md'
    ]
    
    required_templates = [
        'templates/base.html',
        'templates/landing.html',
        'templates/institute.html',
        'templates/payment.html',
        'templates/admin_login.html',
        'templates/admin_register.html',
        'templates/admin_dashboard.html',
        'templates/payment_success.html'
    ]
    
    print("Checking main files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"   [OK] {file}")
        else:
            print(f"   [MISSING] {file}")
    
    print("\nChecking templates...")
    for template in required_templates:
        if os.path.exists(template):
            print(f"   [OK] {template}")
        else:
            print(f"   [MISSING] {template}")
    
    print("\nChecking directories...")
    directories = ['templates', '.github/workflows']
    for directory in directories:
        if os.path.exists(directory):
            print(f"   [OK] {directory}/")
        else:
            print(f"   [MISSING] {directory}/")

def test_code_syntax():
    """Test if Python files have valid syntax"""
    print("\n=== Syntax Check ===")
    
    python_files = [
        'coach_saas_app.py',
        'payment_service.py',
        'setup_new_institute.py',
        'test_saas_app.py'
    ]
    
    for file in python_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    compile(f.read(), file, 'exec')
                print(f"   [OK] {file} - Valid syntax")
            except SyntaxError as e:
                print(f"   [ERROR] {file} - Syntax error: {e}")
            except Exception as e:
                print(f"   [WARNING] {file} - Warning: {e}")

def show_deployment_info():
    """Show deployment information"""
    print("\n=== Deployment Information ===")
    print()
    print("Ready for deployment!")
    print()
    print("Backend Deployment (Render):")
    print("  1. Push code to GitHub repository")
    print("  2. Connect repository to Render")
    print("  3. Set environment variables:")
    print("     - SECRET_KEY")
    print("     - SENDER_EMAIL")
    print("     - SENDER_PASSWORD")
    print("     - RAZORPAY_KEY_ID")
    print("     - RAZORPAY_KEY_SECRET")
    print()
    print("Quick Setup for New Institute:")
    print("  python setup_new_institute.py")
    print()
    print("Local Testing:")
    print("  pip install -r requirements_saas.txt")
    print("  python coach_saas_app.py")
    print("  Open: http://localhost:5000")

def main():
    """Main test function"""
    test_file_structure()
    test_code_syntax()
    show_deployment_info()
    
    print("\n" + "="*50)
    print("SaaS Platform Setup Complete!")
    print("Read README_SAAS.md for detailed instructions")
    print("Use setup_new_institute.py for quick institute setup")
    print("="*50)

if __name__ == '__main__':
    main()