#!/usr/bin/env python3
"""
Database repair script - Fixes JSON parsing issues
"""

import sqlite3
import json

def fix_database():
    """Fix corrupted JSON data in database"""
    print("=== Database Repair Tool ===")
    
    try:
        conn = sqlite3.connect('coach_saas.db')
        cursor = conn.cursor()
        
        # Check configurations table
        cursor.execute('SELECT id, testimonials FROM configurations')
        configs = cursor.fetchall()
        
        fixed_count = 0
        for config_id, testimonials in configs:
            if testimonials:
                try:
                    # Try to parse existing JSON
                    json.loads(testimonials)
                    print(f"Config {config_id}: JSON is valid")
                except json.JSONDecodeError:
                    # Fix corrupted JSON
                    print(f"Config {config_id}: Fixing corrupted JSON")
                    cursor.execute('''
                        UPDATE configurations 
                        SET testimonials = ? 
                        WHERE id = ?
                    ''', ('[]', config_id))
                    fixed_count += 1
            else:
                # Set empty JSON array for NULL values
                print(f"Config {config_id}: Setting default empty array")
                cursor.execute('''
                    UPDATE configurations 
                    SET testimonials = ? 
                    WHERE id = ?
                ''', ('[]', config_id))
                fixed_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"\n[SUCCESS] Fixed {fixed_count} records")
        print("Database is now ready to use!")
        
    except Exception as e:
        print(f"[ERROR] Database repair failed: {e}")

if __name__ == '__main__':
    fix_database()