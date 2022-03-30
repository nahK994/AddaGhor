from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import app.database as database


class Comment(database.Base):
    __tablename__ = "comments"

    commentId = Column(Integer, primary_key=True, index=True)
    commentText = Column(String)
    commentDateTime = Column(String)
    postId = Column(Integer)
    userId = Column(Integer)

class Post(database.Base):
    __tablename__ = "posts"

    postId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    postText = Column(String)
    postDateTime = Column(String)

class React(database.Base):
    __tablename__ = "reacts"

    reactId = Column(Integer, primary_key=True)
    postId = Column(Integer, unique=True, index=True)
    smileReactCount = Column(Integer)
    loveReactCount = Column(Integer)
    likeReactCount = Column(Integer)

class User(database.Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    email = Column(String, unique=True, index=True)
    bio = Column(String)
    occupation = Column(String)
    password = Column(String)
    avatar = Column(String)