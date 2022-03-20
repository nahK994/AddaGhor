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

@app.get("/users/{user_id}")
def getUser(user_id: int, db: Session = Depends(get_db)):    
    return db.query(models.User).filter(models.User.userId == user_id).first()


@app.get("/users")
def getUsers(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.delete("/user/delete/{user_id}")
def deleteUser(user_id: int, db: Session = Depends(get_db)):    
    db.query(models.User).filter(models.User.userId == user_id).delete(synchronize_session=False)
    db.commit()
    return user_id


@app.put("/user/update/{user_id}")
def updateUser(userInfo: schemas.CreateUserModel, user_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.User).filter(models.User.userId == user_id)
        
        previousEmail = query.first().email
        userInfo = userInfo.dict()

        if userInfo['email'] == previousEmail:
            del userInfo['email']

        query.update(
            userInfo, synchronize_session=False
        )
        db.commit()
        return userInfo
    except:
        raise HTTPException(status_code=400, detail="Email already registered")
    

@app.post("/user/create")
def createUsers(userInfo: schemas.CreateUserModel, db: Session = Depends(get_db)):  
    userData = models.User(
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
        user_id = db.query(models.User).filter(models.User.email == userData.email).first().userId
        return user_id
    except:
        raise HTTPException(status_code=400, detail="Email already registered")
