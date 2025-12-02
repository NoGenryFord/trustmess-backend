from fastapi import APIRouter, HTTPException, Response, Depends, Cookie
from src.db import queries
from src.schemas.auth import AuthRequest
from src.secure.passhashing import (
    hash_password_def,
    verify_hached_password_def as hashed_password,
)
from src.secure.jwt_handler import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_refresh_token,
    verify_refresh_token,
)
from src.secure.auth_middleware import get_current_user
from datetime import timedelta

router = APIRouter()


# * POST /auth/login
# *****************************************************************************
@router.post("/auth/login", name="Authenticate User", tags=["authentication"])
async def login(auth_request: AuthRequest, response: Response):
    """Authenticate user and return JWT token"""
    user = queries.check_authentication(auth_request.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalide credenrials")
    if not hashed_password(auth_request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalide credenrials")

    # Create token for user
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["id"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Create refresh token for user
    refresh_token = create_refresh_token(
        data={"sub": user["username"], "user_id": user["id"]}
    )

    # Set cookies (HttpOnly)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # ! False для HTTP, True для HTTPS in production
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # ! False для HTTP, True для HTTPS in production
        samesite="lax",
        max_age=24 * 60 * 60,
        path="/",
    )

    return {
        "status": "success",
        "user": {"id": user["id"], "username": user["username"]},
    }


# *****************************************************************************


# * POST /auth/logout
# *****************************************************************************
@router.post("/auth/logout", tags=["authentication"])
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return {"status": "success"}


# *****************************************************************************


# * POST /auth/register
# *****************************************************************************
@router.post("/auth/register", name="Sign Up User", tags=["authentication"])
async def register(auth_request: AuthRequest):
    """Register new user"""
    # Check if user exist
    existing_user = queries.get_user_by_username(auth_request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exist")

    # Hash password
    hashed_password_in_db = hash_password_def(auth_request.password)

    # Create new user
    try:
        user_id = queries.create_user(auth_request.username, hashed_password_in_db)
        new_user = queries.get_user_by_id(user_id)

        return {
            "status": "success",
            "user": {"id": new_user["id"], "username": new_user["username"]},
        }
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to create user: {str(error)}"
        )


# *****************************************************************************


# * POST /auth/delete_user
# *****************************************************************************
@router.post("/auth/delete_user", tags=["authentication"])
async def delete_user(username: str):
    deleted = queries.delete_user(username)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "succes", "messaga": "User deleted successfully"}


# *****************************************************************************


# * GET /auth/me
# *****************************************************************************
@router.get("/auth/me", tags=["authentication"])
async def me(current_user=Depends(get_current_user)):
    return {"status": "success", "user": current_user}


# *****************************************************************************


# * POST /auth/refresh
# *****************************************************************************
@router.post("/auth/refresh", tags=["authentication"])
async def refresh_toket(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    user = verify_refresh_token(refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["id"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # ! False для HTTP, True для HTTPS in production
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"status": "success"}


# *****************************************************************************
