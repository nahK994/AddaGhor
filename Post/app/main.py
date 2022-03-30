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

@app.get("/posts")
def getPosts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.get("/posts/{post_id}")
def getPost(post_id: int, db: Session = Depends(get_db)):    
    post = db.query(models.Post).filter(models.Post.postId == post_id).first()
    
    if(post is None):
        raise HTTPException(status_code=404, detail="Not found")
    
    response = schemas.ResponsePostModel(
        userId = post.userId,
        userName = post.userName,
        postText = post.postText,
        postDateTime = post.postDateTime
    )
    return response

@app.post("/post/create")
def createPosts(postInfo: schemas.CreatePostModel, db: Session = Depends(get_db)):  
    postData = models.Post(
        userId = postInfo.userId,
        userName = postInfo.userName,
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
            userId = post.userId,
            userName = post.userName,
            postText = post.postText,
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
            userName = postInfo['userName'],
            postText = postInfo['postText'],
            postDateTime = postInfo['postDateTime']
        )
        publisher.publish_message(post_model)
        return postInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


def updateUserInfo(user: schemas.UserModel):
    db = database.SessionLocal()
    query = db.query(models.Post).filter(models.Post.userId == user.userId)
    query.update(
        {
            "userName": user.userName
        },
        synchronize_session=False
    )
    db.commit()
