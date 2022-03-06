from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    bio = Column(String)
    occupation = Column(String)