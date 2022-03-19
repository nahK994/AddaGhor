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

@app.post("/post/create")
def createPosts(postInfo: schemas.CreatePostModel, db: Session = Depends(get_db)):  
    postData = models.Post(
        userId = postInfo.userId,
        postText = postInfo.postText,
        postDateTime = postInfo.postDateTime
    )

    try:
        db.add(postData)
        db.commit()
        db.refresh(postData)
        post_id = db.query(models.Post).filter(models.Post.postDateTime == postInfo.postDateTime and models.Post.userId == postInfo.userId).first().postId
        publisher.publish_message(str(post_id))
        return post_id
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
