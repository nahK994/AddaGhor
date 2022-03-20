from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import app.database as database

class React(database.Base):
    __tablename__ = "reacts"

    reactId = Column(Integer, primary_key=True)
    postId = Column(Integer, unique=True, index=True)
    smileReactCount = Column(Integer)
    loveReactCount = Column(Integer)
    likeReactCount = Column(Integer)