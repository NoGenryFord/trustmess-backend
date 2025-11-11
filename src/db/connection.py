import psycopg2
from psycopg2 import pool 
from psycopg2.extras import RealDictCursor
import os 
from dotenv import load_dotenv


load_dotenv()

#Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'messenger_db')
    DB_USER = os.getenv('DB_USER', 'messenger_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'localhost')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

connection_pool = None

def init_connection_pool(minconn=1, maxconn=20):
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn, maxconn,
            DATABASE_URL
        )
        if connection_pool:
            print("Connection pool created successfully")
    except Exception as error:
        print(f'Error creating connection pool: {error}')
        raise

def get_connection():
    global connection_pool
    if connection_pool is None:
        init_connection_pool()

    try:
        conn = connection_pool.getconn()
        conn.cursor_factory = RealDictCursor
        return conn
    except Exception as e:
        print(f"Error getting connection: {e}")
        raise

def get_admin_connection():
    """Get connection to db (for admin operations)"""
    admin_url = DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    return psycopg2.connect(admin_url)

def release_connection(conn):
    """Return connection back to pool"""
    global connection_pool
    if connection_pool and conn:
        connection_pool.putconn(conn)

def close_all_connection():
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print(f'All database connection closed')

