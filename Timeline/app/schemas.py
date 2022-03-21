from typing import Optional

from pydantic import BaseModel

class PostModel(BaseModel):
    postId: int
    userId: int
    userName: str
    postText: str
    postDateTime: str

class ResponsePostModel(BaseModel):
    userId: int
    userName: str
    postText: str
    postDateTime: str

class CreatePostModel(BaseModel):
    userId: int
    userName: str
    postText: str
    postDateTime: str

class ReactModel(BaseModel):
    postId: int
    reactId: int
    smileReactCount: int
    loveReactCount: int
    likeReactCount: int
class CreateReactModel(BaseModel):
    postId: int
    smileReactCount: int
    loveReactCount: int
    likeReactCount: int

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