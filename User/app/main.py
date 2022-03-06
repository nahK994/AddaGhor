from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, List
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

from . import schemas, crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

app = FastAPI()

userList: List[schemas.UserModel] = []

@app.get("/users/{user_id}")
def getUser(user_id: int):    
    for user in userList:
        if user.userId == str(user_id):
            userModel = schemas.CreateUserModel(
                userName = user.userName,
                bio = user.bio,
                email = user.email
            )
            return userModel

    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users")
def getUsersList(db: Session = Depends(get_db)):
    crud.get_users(db)
    return userList

@app.delete("/user/delete/{user_id}")
def deleteUser(user_id: int):    
    
    for user in userList:
        if str(user_id) == user.userId:
            userList.remove(user)
            return Response(status_code=204)

    raise HTTPException(status_code=500, detail="Cannot be deleted")

@app.put("/user/update/{user_id}")
def updateUser(userInfo: schemas.UserModel, user_id: int):    
    
    for user in userList:
        if str(user_id) == user.userId:
            user.userName = userInfo.userName
            user.bio = userInfo.bio
            user.email = userInfo.email
            user.password = userInfo.password
            return "updated"

    raise HTTPException(status_code=500, detail="Cannot update")

@app.post("/user/create")
def getUsersList(userInfo: schemas.UserModel):  
    if(isEmailUnique(userInfo.email) == False):
        raise HTTPException(status_code=400, detail="Email has been used")

    userData = schemas.UserModel(
        userName = userInfo.userName,
        email = userInfo.email,
        bio = userInfo.bio,
        userId = len(userList),
        password = userInfo.password
    )
    userList.append(userData)

    return userData

def isEmailUnique(email: str):
    for user in userList:
        if email == user.email:
            return False
    return True