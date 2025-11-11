from fastapi import APIRouter, HTTPException
from src.db import queries
from src.schemas.auth import AuthRequest
from src.secure.passhashing import hash_password_def, verify_hached_password_def as hashed_password
from src.secure.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

# * POST /auth/login
# *****************************************************************************
@router.post("/auth/login", name="Authenticate User", tags=["authentication"])
async def login(auth_request: AuthRequest):
    '''Authenticate user and return JWT token'''
    user = queries.check_authentication(auth_request.username)

    if not user:
        raise HTTPException(status_code=401, detail='Invalide credenrials')
    if not hashed_password.verify_hached_password_def(auth_request.password, user['password']):
        raise HTTPException(status_code=401, detail='Invalide credenrials')
    
    # Create token for user
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
# *****************************************************************************

    
# * POST /auth/register
# *****************************************************************************
@router.post("/auth/register", name="Sign Up User", tags=["authentication"])
async def register(auth_request: AuthRequest):
    '''Register new user'''
    # Check if user exist
    existing_user = queries.get_user_by_username(auth_request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail='User already exist')
    
    # Hash password
    hashed_password_in_db = hashed_password.hash_password_def(auth_request.password)
    
    # Create new user
    try:
        user_id = queries.create_user(auth_request.username, hashed_password_in_db)
        new_user = queries.get_user_by_id(user_id)

        # Create token for new user
        access_token = create_access_token(
        data={
                "sub": new_user['username'],
                "user_id": new_user["id"]
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
        return {
            "status": "success",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": new_user['id'],
                "username": new_user['username']
            }
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(error)}")
# *****************************************************************************
