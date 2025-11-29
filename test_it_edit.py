#!/usr/bin/env python3
"""
Test IT admin edit functionality
"""

from coach_saas_app import app
import sqlite3

def test_it_edit():
    """Test IT admin edit functionality"""
    print("=== Testing IT Admin Edit Functionality ===")
    
    with app.test_client() as client:
        # Login as IT admin
        login_response = client.post('/it/authenticate', data={
            'username': 'itadmin',
            'password': 'itadmin123'
        })
        
        if login_response.status_code == 302:  # Redirect means success
            print("[OK] IT admin login successful")
            
            # Test edit institute
            edit_response = client.post('/it/edit_institute/1', data={
                'institute_name': 'Test Institute Updated',
                'email': 'test@updated.com',
                'upi_id': 'test@upi',
                'amount': '2000'
            })
            
            if edit_response.status_code == 200:
                data = edit_response.get_json()
                if data and data.get('success'):
                    print("[OK] Institute edit successful")
                    
                    # Verify changes in database
                    conn = sqlite3.connect('coach_saas.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT institute_name, email, upi_id, amount FROM institutes WHERE id = 1')
                    result = cursor.fetchone()
                    conn.close()
                    
                    if result:
                        print(f"[OK] Updated data: {result}")
                    else:
                        print("[ERROR] No data found")
                else:
                    print(f"[ERROR] Edit failed: {data}")
            else:
                print(f"[ERROR] Edit request failed with status: {edit_response.status_code}")
        else:
            print("[ERROR] IT admin login failed")

if __name__ == '__main__':
    test_it_edit()