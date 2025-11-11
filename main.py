from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import src.db_connector as db_connector

import src.secure.passhashing as pswhach

from src.secure.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.secure.auth_middleware import get_current_user
from datetime import timedelta
from fastapi import Depends

app = FastAPI()

'''Integrate Web socked form create list of online users'''
from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
import json

active_connections: Dict[int, WebSocket] = {}
online_users: Dict[int,str] = {}

async def broadcast_online_users():
    '''Send list of online users all conected users'''
    online_list = [
        {"id": user_id, "username": username}
        for user_id, username in online_users.items()
    ]

    # create message
    message = {
        "type": "online_users",
        "users": online_list,
        "count": len(online_list)
    }

    # send to all

    disconnected = []
    for user_id, connection in active_connections.items():
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")
            disconnected.append(user_id)

    # Delete disconnected users
    for user_id in disconnected:
        if user_id in active_connections:
            del active_connections[user_id]
        if user_id in online_users:
            del online_users[user_id]

# ? CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   


# ? ROOT ROUTE
@app.get("/")
async def read_root():
    return {
        "status": "Ok",
        "docs": "/docs",
        }

# * GET USERS ROUTE
@app.get("/users/", name="Read Users from SQLite DB", tags=["database"])
async def read_sqlite_users():
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    users = db_connector.get_all_users(conn)
    conn.close()
    return [dict(user) for user in users]

# ? WebSocket endpoints
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket connection for control online status
    """
    # Get connection
    await websocket.accept()
    print(f"User {user_id} connecnted")

    # Get info user info from DB
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    user = db_connector.get_user_by_id(conn, user_id)
    conn.close()

    if not user:
        await websocket.close()
        return
    
    # Add active connection
    active_connections[user_id] = websocket
    online_users[user_id] = user['username']

    await broadcast_online_users()

    try:
        # wain new messege (support connection)
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        # User disconnect
        print(f"User {user_id} disconnected")

        # Delete user from active users
        if user_id in active_connections:
            del active_connections[user_id]
        if user_id in online_users:
            del online_users[user_id]

        # "Say" all about update
        await broadcast_online_users()

# ! DEV ROUTE
# !ONLY DEV, DELETE BEFORE DEPLOY
@app.get("/dev/users_with_pass/", name="Read Users with pass", tags=["dev"])
async def read_sqlite_users_with_pass():
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    users = db_connector.get_all_users_with_pass(conn)
    conn.close()
    return [dict(user) for user in users]

# ! DEV ROUTE
@app.get("/dev/online_debug", name="Debug Online Users", tags=["dev"])
async def debug_online_users():
    """DEV: info about online users"""
    return {
        "status": "debug",
        "online_users": dict(online_users),  # {id: username}
        "active_connections_count": len(active_connections),
        "connection_ids": list(active_connections.keys()),
        "full_list": [
            {"id": user_id, "username": username}
            for user_id, username in online_users.items()
        ]
    }

# ? Run the app with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
