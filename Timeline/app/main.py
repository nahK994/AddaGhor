from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends, BackgroundTasks
from typing import Optional, List
from sqlalchemy.orm import Session
import json

import app.schemas as schemas
import app.models as models
import app.database as database

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

def timelineResponse(posts, comments, reacts, users):
    responses = []

    if posts is None:
        return responses
    
    userData = {}
    for user in users:
        userData[user.userId] = user

    for post in posts:
        rspPost = {
            "userId": post.userId,
            "userName": userData[post.userId].userName,
            "avatar": userData[post.userId].avatar,
            "postId": post.postId,
            "postText": post.postText,
            "postDateTime": post.postDateTime,
            "smileReactCount": 0,
            "likeReactCount": 0,
            "loveReactCount": 0,
            "comments": []
        }

        if reacts is not None:
            for react in reacts:
                if post.postId == react.postId:
                    rspPost['loveReactCount'] = react.loveReactCount
                    rspPost['smileReactCount'] = react.smileReactCount
                    rspPost['likeReactCount'] = react.likeReactCount

        if comments is not None:
            for comment in comments:
                if comment.postId == post.postId:
                    rspComment = {
                        "userId": comment.userId,
                        "userName": userData[comment.userId].userName,
                        "avatar": userData[comment.userId].avatar,
                        "commentId": comment.commentId,
                        "commentText": comment.commentText,
                        "commentDateTime": comment.commentDateTime
                    }
                    rspPost['comments'].append(rspComment)
        
        responses.append(rspPost)

    return responses

@app.get("/timeline/all")
def getAll(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    comments = db.query(models.Comment).all()
    reacts = db.query(models.React).all()
    users = db.query(models.User).all()
    
    return timelineResponse(posts, comments, reacts, users)

@app.get("/timeline/{user_id}")
def getAll(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.userId == user_id).all()
    comments = db.query(models.Comment).all()
    reacts = db.query(models.React).all()
    users = db.query(models.User).filter(models.User.userId == user_id).all()
    
    return timelineResponse(posts, comments, reacts, users)

@app.get("/users")
def getPosts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/posts")
def getPosts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.get("/reacts")
def getReacts(db: Session = Depends(get_db)):
    return db.query(models.React).all()

@app.get("/comments")
def getComments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()

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
        userId = commentInfo.userId
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

def consumePost(postInfo: schemas.PostModel):
    db = database.SessionLocal()
    post = db.query(models.Post).filter(models.Post.postId == postInfo.postId).first()
    if post is None:
        initiatePost(postInfo)
        initiateReactsForPost(postInfo.postId)
    else:
        updatePost(postInfo)

def updatePost(postInfo: schemas.PostModel):
    postData = schemas.CreatePostModel(
        userId = postInfo.userId,
        postText = postInfo.postText,
        postDateTime = postInfo.postDateTime
    )
    db = database.SessionLocal()

    try:
        postData = postData.dict()

        query = db.query(models.Post).filter(models.Post.postId == postInfo.postId)
        query.update(
            postData,
            synchronize_session=False
        )
        db.commit()
        return postData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

def initiatePost(postInfo: schemas.PostModel):  
    postData = models.Post(
        userId = postInfo.userId,
        postId = postInfo.postId,
        postText = postInfo.postText,
        postDateTime = postInfo.postDateTime
    )
    db = database.SessionLocal()

    try:
        db.add(postData)
        db.commit()
        db.refresh(postData)
        post = db.query(models.Post).filter(models.Post.postDateTime == postInfo.postDateTime and models.Post.userId == postInfo.userId).first()
        post_model = schemas.PostModel(
            userId = post.userId,
            postId = post.postId,
            postText = post.postText,
            postDateTime = post.postDateTime
        )
        return post_model
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

def consumeReactsForPost(reactInfo: schemas.ReactModel):
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

def consumeComment(commentInfo: schemas.CommentModel):
    db = database.SessionLocal()
    comment = db.query(models.Comment).filter(models.Comment.commentId == commentInfo.commentId).first()
    if comment is None:
        initiateComment(commentInfo)
    else:
        updateComment(commentInfo)

def updateComment(commentInfo: schemas.CommentModel):
    commentData = schemas.CreateCommentModel(
        commentText = commentInfo.commentText,
        commentDateTime = commentInfo.commentDateTime,
        postId = commentInfo.postId,
        userId = commentInfo.userId
    )
    db = database.SessionLocal()

    try:
        commentData = commentData.dict()
        query = db.query(models.Comment).filter(models.Comment.commentId == commentInfo.commentId)
        query.update(
            commentData,
            synchronize_session=False
        )
        db.commit()
        return commentData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

def initiateComment(commentInfo: schemas.CommentModel):  
    commentData = models.Comment(
        commentId = commentInfo.commentId,
        commentText = commentInfo.commentText,
        commentDateTime = commentInfo.commentDateTime,
        postId = commentInfo.postId,
        userId = commentInfo.userId
    )
    db = database.SessionLocal()

    try:
        db.add(commentData)
        db.commit()
        db.refresh(commentData)
        return commentData
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
        occupation = userInfo.occupation,
        avatar = userInfo.avatar
    )
    try:
        db.add(userData)
        db.commit()
        db.refresh(userData)
        return userData
    except:
        raise HTTPException(status_code=500, detail="Internal server error")