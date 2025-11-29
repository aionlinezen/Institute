#!/usr/bin/env python3
"""
Database migration script for new features
"""

import sqlite3
from werkzeug.security import generate_password_hash

def migrate_database():
    """Migrate existing database to support new features"""
    print("=== Database Migration ===")
    
    conn = sqlite3.connect('coach_saas.db')
    cursor = conn.cursor()
    
    try:
        # Add amount column to institutes table if not exists
        cursor.execute("PRAGMA table_info(institutes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'amount' not in columns:
            print("Adding amount column to institutes table...")
            cursor.execute('ALTER TABLE institutes ADD COLUMN amount DECIMAL(10,2) DEFAULT 1000')
        
        if 'is_active' not in columns:
            print("Adding is_active column to institutes table...")
            cursor.execute('ALTER TABLE institutes ADD COLUMN is_active BOOLEAN DEFAULT TRUE')
        
        # Create new tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdf_downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                institute_id INTEGER,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (institute_id) REFERENCES institutes (id)
            )
        ''')
        print("Created pdf_downloads table")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS it_admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Created it_admins table")
        
        # Create default IT admin if not exists
        cursor.execute('SELECT COUNT(*) FROM it_admins')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO it_admins (username, password_hash)
                VALUES (?, ?)
            ''', ('itadmin', generate_password_hash('itadmin123')))
            print("Created default IT admin (username: itadmin, password: itadmin123)")
        
        conn.commit()
        print("\n[SUCCESS] Database migration completed!")
        print("\nNew features available:")
        print("- Configurable course amounts")
        print("- PDF download tracking")
        print("- IT admin panel")
        print("- Institute enable/disable")
        print("- Image upload for testimonials")
        
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()