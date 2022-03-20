from typing import Optional

from pydantic import BaseModel

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