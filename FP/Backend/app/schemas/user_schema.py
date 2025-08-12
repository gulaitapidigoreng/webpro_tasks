from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema with common attributes
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Schema for creating a new user (includes password)
class UserCreate(UserBase):
    password: str

# Schema for reading/returning user data (never includes password)
class UserOut(UserBase):
    id: int
    bio: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for the login response token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for data stored inside the token
class TokenData(BaseModel):
    username: Optional[str] = None