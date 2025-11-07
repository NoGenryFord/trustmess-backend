# Connector for SQLite DB
import sqlite3
from sqlite3 import Connection
import os

# Use /tmp for the database path, as it's a writable in-memory filesystem in Cloud Run
DB_PATH_MAIN = '/tmp/db.db'

def get_db_connection(db_path: str) -> Connection:
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: Connection):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
    return 'Database initialized successfully'

def get_all_users(conn: Connection):
    cursor = conn.execute('SELECT id, username, isAdmin FROM users')
    return cursor.fetchall()

# !ONLY DEV, DELETE BEFORE DEPLOY
def get_all_users_with_pass(conn: Connection):
    cursor = conn.execute('SELECT id, username, password, isAdmin FROM users')
    return cursor.fetchall()

def get_user_by_id(conn: Connection, user_id: int):
    cursor = conn.execute('SELECT id, username, isAdmin FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()

def get_user_by_username(conn: Connection, username: str):
    cursor = conn.execute('SELECT id, username FROM users WHERE username = ?', (username,))
    return cursor.fetchone()


def check_authentication(conn: Connection, username: str):
    cursor = conn.execute(
        'SELECT id, username, password FROM users WHERE username = ?', (username,)
    )
    return cursor.fetchone()


def create_user(conn: Connection, username: str, password: str, isAdmin: bool = False):
    with conn:
        cursor = conn.execute(
            'INSERT INTO users (username, password, isAdmin) VALUES (?, ?, ?)',
            (username, password, isAdmin)
        )
        user_id = cursor.lastrowid
        conn.commit()

    return get_user_by_id(conn, user_id)
