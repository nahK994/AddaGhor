from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends, BackgroundTasks
from typing import Optional, List
from sqlalchemy.orm import Session
import json

import app.schemas as schemas
import app.models as models
import app.database as database


def get_db():
    db = database.SessionLocal()
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

@app.post("/post/create/{postInfo}")
def createPosts(postInfo: str, db: Session = Depends(get_db)):  
    postInfo = json.loads(postInfo)
    postData = models.Post(
        userId = int(postInfo['userId']),
        postId = int(postInfo['postId']),
        postText = postInfo['postText'],
        postDateTime = postInfo['postDateTime']
    )

    try:
        db.add(postData)
        db.commit()
        db.refresh(postData)
        return postInfo.postId
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

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

@app.post("/comment/create")
def createComments(commentInfo: schemas.CreateCommentModel, db: Session = Depends(get_db)):  
    commentData = models.Comment(
        commentText = commentInfo.commentText,
        commentDateTime = commentInfo.commentDateTime,
        postId = commentInfo.postId,
        userId = commentInfo.userId,
        userName = commentInfo.userName
    )

    try:
        db.add(commentData)
        db.commit()
        db.refresh(commentData)
        comment_id = db.query(models.Comment).filter(models.Comment.commentDateTime == commentInfo.commentDateTime and models.Comment.userId == commentInfo.userId).first().commentId
        return comment_id
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

    try:
        db.add(reactData)
        db.commit()
        db.refresh(reactData)

        react_id = db.query(models.React).filter(models.React.postId == post_id).first().reactId
        return react_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

def initiatePost(postInfo: schemas.PostModel):  
    postData = models.Post(
        userId = postInfo.userId,
        postText = postInfo.postText,
        postDateTime = postInfo.postDateTime,
        postId = postInfo.postId
    )
    db = database.SessionLocal()

    try:
        db.add(postData)
        db.commit()
        db.refresh(postData)
        post = db.query(models.Post).filter(models.Post.postDateTime == postInfo.postDateTime and models.Post.userId == postInfo.userId).first()
        post_model = schemas.PostModel(
            postId = post.postId,
            userId = post.userId,
            postText = post.postText,
            postDateTime = post.postDateTime
        )
        return post_model
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

def updateReactsForPost(reactInfo: schemas.ReactModel):
    db = database.SessionLocal()
    try:
        reactData = schemas.CreateReactModel(
            postId = reactInfo.postId,
            smileReactCount = reactInfo.smileReactCount,
            loveReactCount = reactInfo.loveReactCount,
            likeReactCount = reactInfo.likeReactCount
        )
        reactData = reactData.dict()

        query = db.query(models.React).filter(models.React.postId == reactInfo.postId)
        query.update(
            reactData,
            synchronize_session=False
        )
        db.commit()
        return reactData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")