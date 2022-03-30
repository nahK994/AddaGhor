from typing import Optional

from pydantic import BaseModel

class PostModel(BaseModel):
    postId: int
    userId: int
    postText: str
    postDateTime: str

class ResponsePostModel(BaseModel):
    userId: int
    userName: str
    postId: int
    postText: str
    postDateTime: str

class CreatePostModel(BaseModel):
    userId: int
    postText: str


class UserModel(BaseModel):
    userId: int
    userName: str
    bio: Optional[str] = None
    email: str
    password: str
    occupation: str