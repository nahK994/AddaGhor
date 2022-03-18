from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends, BackgroundTasks
from typing import Optional, List
from .database import SessionLocal, engine
from sqlalchemy.orm import Session


from . import schemas, models


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

app = FastAPI()

@app.get("/posts")
def getPosts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.get("/reacts")
def getReacts(db: Session = Depends(get_db)):
    return db.query(models.React).all()

@app.get("/comments")
def getComments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()

