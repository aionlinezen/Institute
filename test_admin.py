#!/usr/bin/env python3
"""
Test admin dashboard functionality
"""

from coach_saas_app import app
import sqlite3

def test_admin_dashboard():
    """Test admin dashboard data loading"""
    print("=== Testing Admin Dashboard ===")
    
    try:
        with app.test_client() as client:
            # Test if we can load institute data without JSON errors
            conn = sqlite3.connect('coach_saas.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT i.id, i.username, i.password_hash, i.institute_name, i.offer_text, i.upi_id, i.email, i.created_at,
                       c.why_choose_us, c.pdf_title, c.pdf_filename, c.testimonials
                FROM institutes i
                LEFT JOIN configurations c ON i.id = c.institute_id
                WHERE i.username = ?
            ''', ('demo',))
            
            institute_data = cursor.fetchone()
            conn.close()
            
            if institute_data:
                # Test JSON parsing
                import json
                try:
                    testimonials = json.loads(institute_data[11]) if institute_data[11] else []
                    print(f"[SUCCESS] JSON parsing works - {len(testimonials)} testimonials found")
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"[ERROR] JSON parsing failed: {e}")
                    print(f"Raw data: {repr(institute_data[11])}")
                    return False
                
                print(f"[SUCCESS] Institute data loaded: {institute_data[3]}")
                return True
            else:
                print("[ERROR] No demo institute found")
                return False
                
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_admin_dashboard()
    if success:
        print("\n[SUCCESS] Admin dashboard is ready!")
        print("You can now run: python start_app.py")
    else:
        print("\n[ERROR] Please run: python demo_setup.py first")