from fastapi import APIRouter, HTTPException
from src.db import queries

# * POST /auth/login
@app.post("/auth/login", name="Authenticate User", tags=["authentication"])
async def login(auth_request: AuthRequest):
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    user = db_connector.check_authentication(conn, auth_request.username)
    conn.close()

    verify_password = pswhach.verify_hached_password_def(auth_request.password, user['password'])

    if (user and verify_password and user['username'] == auth_request.username):
        access_token = create_access_token(
            data={
                "sub": user['username'],
                "user_id": user["id"]
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {
            "status": "success", 
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user['id'], 
                "username": user['username']
                }
            }
    else:
        return {"status": "failure", "message": "Invalid credentials"}
    
# * POST /auth/register
@app.post("/auth/register", name="Sign Up User", tags=["authentication"])
async def register(auth_request: AuthRequest):
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)

    # Check if user exist
    existing_user = db_connector.get_user_by_username(conn, auth_request.username)
    if existing_user:
        conn.close()
        return {"status": "failure", "message": "User already exists"}
    
    hashed_password = pswhach.hash_password_def(auth_request.password)
    
    # Create new user
    new_user = db_connector.create_user(conn, auth_request.username, hashed_password)
    conn.close()

    if new_user:
        return {"status": "success", "user": dict(new_user)}
    else:
        return {"status": "failure", "message": "Failed to create user"}
    