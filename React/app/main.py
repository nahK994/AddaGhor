from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends
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


@app.get("/reacts")
def getReacts(db: Session = Depends(get_db)):
    return db.query(models.React).all()

@app.get("/reacts/{post_id}")
def getReactsByPost(post_id: int, db: Session = Depends(get_db)):
    return db.query(models.React).filter(models.React.postId == post_id).first()

@app.post("/react/create")
def createReactsForPost(reactInfo: schemas.CreateReactModel, db: Session = Depends(get_db)):  
    reactData = models.React(
        postId = reactInfo.postId,
        smileReactCount = reactInfo.smileReactCount,
        loveReactCount = reactInfo.loveReactCount,
        likeReactCount = reactInfo.likeReactCount
    )

    try:
        db.add(reactData)
        db.commit()
        db.refresh(reactData)
        post_id = db.query(models.React).filter(models.React.postId == reactData.postId).first().postId
        return post_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/react/create")
def createReactsForPost(reactInfo: schemas.CreateReactModel, db: Session = Depends(get_db)):  
    reactData = models.React(
        postId = reactInfo.postId,
        smileReactCount = reactInfo.smileReactCount,
        loveReactCount = reactInfo.loveReactCount,
        likeReactCount = reactInfo.likeReactCount
    )

    try:
        db.add(reactData)
        db.commit()
        db.refresh(reactData)
        post_id = db.query(models.React).filter(models.React.postId == post_id).first().postId
        return post_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/react/{post_id}/love")
def updateLoveReactForPost(post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.React).filter(models.React.postId == post_id)
        reactInfo = query.first().dict()
        reactInfo["loveReactCount"] = reactInfo["loveReactCount"]+1

        query.update(
            reactInfo, synchronize_session=False
        )
        db.commit()
        return reactInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/react/{post_id}/like")
def updateLikeReactForPost(post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.React).filter(models.React.postId == post_id)
        reactInfo = query.first().dict()
        reactInfo["likeReactCount"] = reactInfo["likeReactCount"]+1

        query.update(
            reactInfo, synchronize_session=False
        )
        db.commit()
        return reactInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/react/{post_id}/smile")
def updateSmileReactForPost(post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.React).filter(models.React.postId == post_id)
        reactInfo = query.first().dict()
        reactInfo["smileReactCount"] = reactInfo["smileReactCount"]+1

        query.update(
            reactInfo, synchronize_session=False
        )
        db.commit()
        return reactInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
