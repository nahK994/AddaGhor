from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import app.database as database


class Comment(database.Base):
    __tablename__ = "comments"

    commentId = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, unique=True)
    userId = Column(Integer, unique=True)
    userName = Column(String)
    commentText = Column(String)
    commentDateTime = Column(String)

class Post(database.Base):
    __tablename__ = "posts"

    postId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, unique=True)
    postText = Column(String)
    postDateTime = Column(String)

class React(database.Base):
    __tablename__ = "reacts"

    reactId = Column(Integer, primary_key=True)
    postId = Column(Integer, unique=True, index=True)
    smileReactCount = Column(Integer)
    loveReactCount = Column(Integer)
    likeReactCount = Column(Integer)