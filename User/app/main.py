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

# userList: List[schemas.UserModel] = []

@app.get("/users/{user_id}")
def getUser(user_id: int, db: Session = Depends(get_db)):    
    return crud.get_user(db, user_id)

@app.get("/users")
def getUsers(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.delete("/user/delete/{user_id}")
def deleteUser(user_id: int):    
    # for user in userList:
    #     if str(user_id) == user.userId:
    #         userList.remove(user)
    #         return Response(status_code=204)

    # raise HTTPException(status_code=500, detail="Cannot be deleted")
    pass

@app.put("/user/update/{user_id}")
def updateUser(userInfo: schemas.CreateUserModel, user_id: int, db: Session = Depends(get_db)):    
    return crud.update_user(db, userInfo, user_id)

@app.post("/user/create")
def createUsers(userInfo: schemas.CreateUserModel, db: Session = Depends(get_db)):  
    # if(isEmailUnique(userInfo.email) == False):
    #     raise HTTPException(status_code=400, detail="Email has been used")
    response = crud.create_user(db, userInfo)
    # userList.append(userData)

    return response

# def isEmailUnique(email: str):
#     for user in userList:
#         if email == user.email:
#             return False
#     return True