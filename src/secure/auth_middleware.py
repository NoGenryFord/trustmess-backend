from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.secure.jwt_handler import verify_token

security = HTTPBearer()

def get_token_from_coockie(request: Request):
    token = request.cookies.get("acces_token") or request.cookies.get("refresh_token")
    return token

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), request: Request = None):
    """
    Get token and return user data 
    """

    token = None
    if credentials and credentials.credentials:
        token = credentials.credentials
    if not token and request:
        token = get_token_from_coockie(request)

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = verify_token(token)