from typing import Optional

from pydantic import BaseModel

class UserModel(BaseModel):
    userId: int
    userName: str
    bio: Optional[str] = None
    email: str
    password: str
    occupation: str
    avatar: str

class ResponseUserModel(BaseModel):
    userName: str
    bio: Optional[str] = None
    email: str
    occupation: str
    avatar: str

class CreateUserModel(BaseModel):
    userName: str
    bio: Optional[str] = None
    email: str
    occupation: str
    password: str
    avatar: str