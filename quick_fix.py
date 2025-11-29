#!/usr/bin/env python3
"""
Quick fix for JSON parsing issues
"""

import sqlite3
import json

def quick_fix():
    """Quick fix for testimonials JSON"""
    print("=== Quick Fix ===")
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    # Get the problematic testimonials
    cursor.execute('SELECT id, testimonials FROM configurations')
    configs = cursor.fetchall()
    
    for config_id, testimonials in configs:
        if testimonials:
            try:
                # Try to parse and re-save to ensure clean JSON
                parsed = json.loads(testimonials)
                clean_json = json.dumps(parsed)
                
                cursor.execute('''
                    UPDATE configurations 
                    SET testimonials = ? 
                    WHERE id = ?
                ''', (clean_json, config_id))
                
                print(f"Fixed config {config_id}")
                
            except Exception as e:
                print(f"Error with config {config_id}: {e}")
                # Set to empty array if parsing fails
                cursor.execute('''
                    UPDATE configurations 
                    SET testimonials = ? 
                    WHERE id = ?
                ''', ('[]', config_id))
    
    conn.commit()
    conn.close()
    print("Fix completed!")

if __name__ == '__main__':
    quick_fix()