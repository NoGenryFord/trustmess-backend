#!/usr/bin/env python3
"""Initialize database on startup"""
import sqlite3
import sys
from src.secure.passhashing import hash_password

DB_PATH = './db.db'

def init_database():
    """Create database and tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        
        # Create test users if database is empty
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Database is empty, creating test users...")
            # Add test users with hashed passwords
            test_users = [
                ('admin', hash_password('admin123'), 1),
                ('user1', hash_password('password1'), 0),
                ('user2', hash_password('password2'), 0),
            ]
            cursor.executemany(
                'INSERT INTO users (username, password, isAdmin) VALUES (?, ?, ?)',
                test_users
            )
            print(f"Created {len(test_users)} test users")
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
