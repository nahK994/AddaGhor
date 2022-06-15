from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, List
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
import app.database as database
import app.publisher as publisher

# import models
# import schemas
# import database
# import publisher

from fastapi.middleware.cors import CORSMiddleware

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except:
        db.close()

app = FastAPI()
origins = [
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/reacts")
def getReacts(db: Session = Depends(get_db)):
    return db.query(models.React).all()

@app.get("/reacts/{post_id}")
def getReactsByPost(post_id: int, db: Session = Depends(get_db)):
    return db.query(models.React).filter(models.React.postId == post_id).first()

@app.post("/react/create/{post_id}")
def createReactsForPost(post_id: int, db: Session = Depends(get_db)):
    reactData = models.React(
        postId = post_id,
        smileReactCount = 0,
        loveReactCount = 0,
        likeReactCount = 0
    )

    try:
        db.add(reactData)
        db.commit()
        db.refresh(reactData)

        react_id = db.query(models.React).filter(models.React.postId == post_id).first().reactId
        return react_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/react/{post_id}/love")
def updateLoveReactForPost(post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.React).filter(models.React.postId == post_id)
        reactInfo = query.first()
        reactData = schemas.CreateReactModel(
            postId = reactInfo.postId,
            loveReactCount = reactInfo.loveReactCount+1,
            smileReactCount = reactInfo.smileReactCount,
            likeReactCount = reactInfo.likeReactCount
        )
        reactData = reactData.dict()
        query.update(
            reactData,
            synchronize_session=False
        )
        db.commit()

        sendToPublisher(post_id, db)
        return reactData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/react/{post_id}/like")
def updateLikeReactForPost(post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.React).filter(models.React.postId == post_id)
        reactInfo = query.first()
        reactData = schemas.CreateReactModel(
            postId = reactInfo.postId,
            loveReactCount = reactInfo.loveReactCount,
            smileReactCount = reactInfo.smileReactCount,
            likeReactCount = reactInfo.likeReactCount+1
        )
        reactData = reactData.dict()

        query.update(
            reactData,
            synchronize_session=False
        )
        db.commit()

        sendToPublisher(post_id, db)
        return reactData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/react/{post_id}/smile")
def updateSmileReactForPost(post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.React).filter(models.React.postId == post_id)
        reactInfo = query.first()
        reactData = schemas.CreateReactModel(
            postId = reactInfo.postId,
            loveReactCount = reactInfo.loveReactCount,
            smileReactCount = reactInfo.smileReactCount+1,
            likeReactCount = reactInfo.likeReactCount
        )
        reactData = reactData.dict()

        query.update(
            reactData,
            synchronize_session=False
        )
        db.commit()

        sendToPublisher(post_id, db)
        return reactData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")



def initiateReactsForPost(post_id: int):
    db = database.SessionLocal()

    reactData = models.React(
        postId = post_id,
        smileReactCount = 0,
        loveReactCount = 0,
        likeReactCount = 0
    )
    reactForPostInitiated = db.query(models.React).filter(models.React.postId == post_id).first()
    if reactForPostInitiated is not None:
        return None

    try:
        db.add(reactData)
        db.commit()
        db.refresh(reactData)

        react_id = db.query(models.React).filter(models.React.postId == post_id).first().reactId
        return react_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


def sendToPublisher(post_id: int, db: Session):
    react = db.query(models.React).filter(models.React.postId == post_id).first()
    react_model = schemas.ReactModel(
        postId = react.postId,
        reactId = react.reactId,
        smileReactCount = react.smileReactCount,
        loveReactCount = react.loveReactCount,
        likeReactCount = react.likeReactCount
    )
    publisher.publish_message(react_model)