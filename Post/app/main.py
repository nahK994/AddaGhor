from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends, BackgroundTasks
from typing import Optional, List
from sqlalchemy.orm import Session

import app.schemas as schemas
import app.models as models
import app.database as database
import app.publisher as publisher

from fastapi.middleware.cors import CORSMiddleware

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

def processResponse(users, posts):
    response = []
    userData = {}
    for user in users:
        userData[user.userId] = user

    for post in posts:
        res = schemas.ResponsePostModel(
            postId = post.postId,
            postText = post.postText,
            postDateTime = post.postDateTime,
            userId = post.userId,
            userName = userData[post.userId].userName
        )
        response.append(res)
    return response

@app.get("/posts")
def getPosts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    posts = db.query(models.Post).all()
    return processResponse(users, posts)

@app.get("/posts/{user_id}")
def getPosts(user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.userId == user_id).all()
    posts = db.query(models.Post).filter(models.Post.userId == user_id).all()
    return processResponse(users, posts)

@app.get("/users")
def getPosts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

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
        post = db.query(models.Post).filter(models.Post.postDateTime == postInfo.postDateTime and models.Post.userId == postInfo.userId).first()
        post_model = schemas.PostModel(
            postId = post.postId,
            postText = post.postText,
            userId = post.userId,
            postDateTime = post.postDateTime
        )
        publisher.publish_message(post_model)
        return post
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/post/delete/{post_id}")
def deletePost(post_id: int, db: Session = Depends(get_db)):    
    try:
        db.query(models.Post).filter(models.Post.postId == post_id).delete(synchronize_session=False)
        db.commit()
        return post_id
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/post/update/{post_id}")
def updatePost(postInfo: schemas.CreatePostModel, post_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.Post).filter(models.Post.postId == post_id)
        postInfo = postInfo.dict()
        query.update(
            postInfo, synchronize_session=False
        )
        db.commit()

        post_model = schemas.PostModel(
            postId = post_id,
            userId = postInfo['userId'],
            postText = postInfo['postText'],
            postDateTime = postInfo['postDateTime']
        )
        publisher.publish_message(post_model)
        return postInfo
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
