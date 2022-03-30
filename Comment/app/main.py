from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends, BackgroundTasks
from typing import Optional, List
from sqlalchemy.orm import Session


import app.schemas as schemas
import app.models as models
import app.database as database
import app.publisher as publisher

from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except:
        db.close()

app = FastAPI()
origins = [
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def processResponse(users, comments):
    response = []
    userData = {}
    for user in users:
        userData[user.userId] = user

    for comment in comments:
        res = schemas.ResponseCommentModel(
            postId = comment.commentId,
            userId = comment.userId,
            userName = comment.userName,
            commentId = comment.commentId,
            commentText = comment.commentText,
            commentDateTime = userData[post.userId].userName
        )
        response.append(res)
    return response

@app.get("/users")
def getPosts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/comments")
def getComments(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    comments = db.query(models.Comment).all()
    return processResponse(users, comments)

@app.get("/comments/{comment_id}")
def getComment(comment_id: int, db: Session = Depends(get_db)):    
    users = db.query(models.User).filter(models.User.userId == user_id).all()
    comments = db.query(models.Comment).filter(models.Comment.userId == user_id).all()
    return processResponse(users, comments)

@app.post("/comment/create")
def createComments(commentInfo: schemas.CreateCommentModel, db: Session = Depends(get_db)):  
    commentData = models.Comment(
        commentText = commentInfo.commentText,
        commentDateTime = str(datetime.utcnow()),
        postId = commentInfo.postId,
        userId = commentInfo.userId
    )

    try:
        db.add(commentData)
        db.commit()
        db.refresh(commentData)

        comment = db.query(models.Comment).filter(models.Comment.commentDateTime == commentData.commentDateTime and models.Comment.userId == commentData.userId and models.Comment.postId == commentData.postId).first()
        comment_model = schemas.CommentModel(
            commentId = comment.commentId,
            commentText = comment.commentText,
            commentDateTime = comment.commentDateTime,
            postId = comment.postId,
            userId = comment.userId
        )
        publisher.publish_message(comment_model)
        return comment_model
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/comment/delete/{comment_id}")
def deleteComment(comment_id: int, db: Session = Depends(get_db)):    
    try:
        db.query(models.Comment).filter(models.Comment.commentId == comment_id).delete(synchronize_session=False)
        db.commit()
        return comment_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/comment/update/{comment_id}")
def updateComment(commentInfo: schemas.CreateCommentModel, comment_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.Comment).filter(models.Comment.commentId == comment_id)

        commentInfo = commentInfo.dict()
        query.update(
            commentInfo, synchronize_session=False
        )
        db.commit()

        comment_model = schemas.CommentModel(
            commentId = comment_id,
            commentText = commentInfo['commentText'],
            commentDateTime = str(datetime.utcnow()),
            postId = commentInfo['postId'],
            userId = commentInfo['userId']
        )
        publisher.publish_message(comment_model)
        return commentInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


def consumeUser(userInfo: schemas.UserModel):
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.userId == userInfo.userId).first()
    if user is None:
        initiateUser(userInfo)
    else:
        updateUser(userInfo)

def updateUser(userInfo: schemas.UserModel):
    db = database.SessionLocal()

    try:
        query = db.query(models.User).filter(models.User.userId == userInfo.userId)
        
        userData = userInfo.dict()
        query.update(
            userData,
            synchronize_session=False
        )
        db.commit()
        return userData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

def initiateUser(userInfo: schemas.UserModel):  
    db = database.SessionLocal()
    userData = models.User(
        userId = userInfo.userId,
        userName = userInfo.userName,
        email = userInfo.email,
        bio = userInfo.bio,
        password = userInfo.password,
        occupation = userInfo.occupation
    )
    try:
        db.add(userData)
        db.commit()
        db.refresh(userData)
        return userData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")