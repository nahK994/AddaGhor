from typing import Optional

from pydantic import BaseModel

class CommentModel(BaseModel):
    postId: int
    userId: int
    commentId: int
    commentText: str
    commentDateTime: str

class ResponseCommentModel(BaseModel):
    postId: int
    userId: int
    avatar: str
    userName: str
    commentId: int
    commentText: str
    commentDateTime: str

class CreateCommentModel(BaseModel):
    postId: int
    userId: int
    commentText: str

class UserModel(BaseModel):
    userId: int
    userName: str
    bio: Optional[str] = None
    email: str
    password: str
    occupation: str
    avatar: str