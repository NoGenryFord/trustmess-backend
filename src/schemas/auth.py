from pydantic import BaseModel

# ? SCHEMAS
# * AUTH ROUTES
class AuthRequest(BaseModel):
    username: str
    password: str