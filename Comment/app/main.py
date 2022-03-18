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


@app.get("/comments")
def getComments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()

@app.get("/comments/{comment_id}")
def getComment(comment_id: int, db: Session = Depends(get_db)):    
    comment = db.query(models.Comment).filter(models.Comment.commentId == comment_id).first()
    
    if(comment == None):
        raise HTTPException(status_code=404, detail="Not found")
    
    response = schemas.ResponseCommentModel(
        postId = comment.postId,
        userName = comment.userName,
        commentText = comment.commentText,
        commentDateTime = comment.commentDateTime
    )
    return response

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

@app.delete("/comment/delete/{comment_id}")
def deleteComment(comment_id: int, db: Session = Depends(get_db)):    
    try:
        db.query(models.Comment).filter(models.Comment.commentId == post_id).delete(synchronize_session=False)
        db.commit()
        return post_id
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
        return commentInfo
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
