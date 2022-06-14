from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, List
from sqlalchemy.orm import Session

import app.schemas as schemas
import app.models as models
import app.database as database
import app.publisher as publisher

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

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

@app.get("/users/{user_id}")
def getUser(user_id: int, db: Session = Depends(get_db)):    
    return db.query(models.User).filter(models.User.userId == user_id).first()


@app.get("/users")
def getUsers(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/login/{email}/{password}")
def getUsers(email: str, password: str, db: Session = Depends(get_db)):
    try:
        return db.query(models.User).filter(models.User.email == email and models.User.password == password).first().userId
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/delete/{user_id}")
def deleteUser(user_id: int, db: Session = Depends(get_db)):    
    db.query(models.User).filter(models.User.userId == user_id).delete(synchronize_session=False)
    db.commit()
    return user_id


@app.put("/user/update/{user_id}")
def updateUser(userInfo: schemas.CreateUserModel, user_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.User).filter(models.User.userId == user_id)

        userInfo = userInfo.dict()
        query.update(
            userInfo, synchronize_session=False
        )
        db.commit()

        userData = schemas.UserModel(
            userId = user_id,
            userName = userInfo['userName'],
            email = userInfo['email'],
            bio = userInfo['bio'],
            password = userInfo['password'],
            occupation = userInfo['occupation'],
            avatar = userInfo['avatar']
        )
        publisher.publish_message(userData)
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
        occupation = userInfo.occupation,
        avatar = userInfo.avatar
    )

    try:
        db.add(userData)
        db.commit()
        db.refresh(userData)
        user = db.query(models.User).filter(models.User.email == userData.email).first()

        userInfo = schemas.UserModel(
            userId = user.userId,
            userName = user.userName,
            email = user.email,
            bio = user.bio,
            password = user.password,
            occupation = user.occupation,
            avatar = user.avatar
        )
        publisher.publish_message(userInfo)
        return user
    except:
        raise HTTPException(status_code=400, detail="Email already registered")
