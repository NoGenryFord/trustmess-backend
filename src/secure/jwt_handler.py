import jwt
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import os 

load_dotenv()


'''Secret key adn other constants'''
SECRET_KEY = os.getenv('SECRET_KEY')  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    '''Create JWT token'''
    to_encode = data.copy()

    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    '''Check JWT token and return user data'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            return None
        
        return {"username": username, "user_id": user_id}
    except jwt.ExpiredSignatureError:
        # Old token
        return None
    except jwt.InvalidTokenError:
        # Invaled token
        return None
    
def verify_refresh_token(token: str):
    '''Check JWT token and return user data'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        username = payload.get("sub")
        user_id = payload.get("user_id")
        if not username or not user_id:
            return None
        return {"username": username, "user_id": user_id}
    except ...:
        return None
    
def create_refresh_token(data: dict):
    """Create refresh token with long life term"""
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(days=1)
    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt