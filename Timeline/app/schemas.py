from typing import Optional

from pydantic import BaseModel

class PostModel(BaseModel):
    postId: int
    userId: int
    postText: str
    postDateTime: str
class ResponsePostModel(BaseModel):
    userId: int
    postText: str
    postDateTime: str

class CreatePostModel(BaseModel):
    userId: int
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