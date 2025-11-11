# * ALL CRUD OPERATIONS (* Queries)
from .connection import get_connection, release_connection

def get_all_users():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, username, created_at FROM users')
            return cursor.fetchall()
    finally:
        release_connection(conn)

def get_user_by_id(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, username, created_at FROM users WHERE id = %s', (user_id,))
            return cursor.fetchone()
    finally:
        release_connection(conn)

def get_user_by_username(username: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, username, created_at FROM users WHERE username = %s', (username,))
            return cursor.fetchone()
    finally:
        release_connection(conn)


def check_authentication(username: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT id, username, password FROM users WHERE username = %s', (username,)
            )
            return cursor.fetchone()
    finally:
        release_connection(conn)


def create_user(username: str, hashed_password: str, isAdmin: bool = False):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s) RETURNING id',
                (username, hashed_password, isAdmin)
            )
            user_id = cursor.fetchone()['id']
            conn.commit()
            return user_id
    except Exception as error:
        conn.rollback()
        raise
    finally:
        release_connection(conn)

# ! *************************************** ! #
# !ONLY DEV, DELETE BEFORE DEPLOY
def get_all_users_with_pass():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, username, password, created_at FROM users')
            return cursor.fetchall()

    finally:
            release_connection(conn)
# ! *************************************** ! #
