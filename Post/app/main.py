from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends, BackgroundTasks
from typing import Optional, List
from .database import SessionLocal, engine
from sqlalchemy.orm import Session


from . import schemas, models, publisher


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

@app.get("/posts/{post_id}")
def getPost(post_id: int, db: Session = Depends(get_db)):    
    post = db.query(models.Post).filter(models.Post.postId == post_id).first()
    
    if(post == None):
        raise HTTPException(status_code=404, detail="Not found")
    
    response = schemas.ResponsePostModel(
        userId = post.userId,
        postText = post.postText,
        postDateTime = post.postDateTime
    )
    return response

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
        return postInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
