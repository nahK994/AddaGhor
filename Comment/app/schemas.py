from typing import Optional

from pydantic import BaseModel

class CommentModel(BaseModel):
    commentId: int
    postId: int
    userId: int
    userName: str
    commentText: str
    commentDateTime: str

class ResponseCommentModel(BaseModel):
    postId: int
    userName: str
    commentText: str
    commentDateTime: str

class CreateCommentModel(BaseModel):
    postId: int
    userId: int
    userName: str
    commentText: str
    commentDateTime: str

class UserModel(BaseModel):
    userId: int
    userName: str
    bio: Optional[str] = None
    email: str
    password: str
    occupation: str