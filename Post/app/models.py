from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import app.database as database

class Post(database.Base):
    __tablename__ = "posts"

    postId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    userName = Column(String)
    postText = Column(String)
    postDateTime = Column(String)