from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Comment(Base):
    __tablename__ = "comments"

    commentId = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer)
    userId = Column(Integer)
    userName = Column(String)
    commentText = Column(String)
    commentDateTime = Column(String)