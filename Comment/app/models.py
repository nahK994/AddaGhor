from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Comment(Base):
    __tablename__ = "comments"

    postId = Column(Integer)
    userId = Column(Integer)
    commentId = Column(Integer, primary_key=True, index=True)
    commentText = Column(String)
    commentDateTime = Column(String)

class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    email = Column(String, unique=True, index=True)
    bio = Column(String)
    occupation = Column(String)
    password = Column(String)