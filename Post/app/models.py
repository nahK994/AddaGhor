from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import app.database as database

class Post(database.Base):
    __tablename__ = "posts"

    postId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    postText = Column(String)
    postDateTime = Column(String)

class User(database.Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    email = Column(String, unique=True, index=True)
    bio = Column(String)
    occupation = Column(String)
    password = Column(String)