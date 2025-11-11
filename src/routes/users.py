from fastapi import APIRouter, HTTPException
from src.db import queries
from src.schemas.auth import AuthRequest
from src.secure.auth_middleware import get_current_user

router = APIRouter()

# ? ROOT ROUTE
# *****************************************************************************
@app.get("/")
async def read_root():
    return {
        "status": "Ok",
        "docs": "/docs",
        }
# *****************************************************************************


# * Get all users
# *****************************************************************************
@app.get("/users/", name="Read Users from SQLite DB", tags=["database"])
async def read_sqlite_users():
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    users = db_connector.get_all_users(conn)
    conn.close()
    return [dict(user) for user in users]
# *****************************************************************************

# ! DEV ROUTE
# ! ONLY DEV, DELETE BEFORE DEPLOY
# ! Get All users with passwords
# ! *****************************************************************************
@app.get("/dev/users_with_pass/", name="Read Users with pass", tags=["dev"])
async def read_sqlite_users_with_pass():
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    users = db_connector.get_all_users_with_pass(conn)
    conn.close()
    return [dict(user) for user in users]
# ! *****************************************************************************
