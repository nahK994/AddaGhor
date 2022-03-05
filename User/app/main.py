from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response
from typing import Optional, List

app = FastAPI()

class UserModel(BaseModel):
    userId: Optional[str]
    userName: str
    bio: Optional[str] = None
    email: str

class CreateUserModel(BaseModel):
    userName: str
    bio: Optional[str] = None
    email: str

userList: List[UserModel] = []

@app.get("/users/{user_id}")
def getUser(user_id: int):    
    for user in userList:
        if user.userId == str(user_id):
            userModel = CreateUserModel(
                userName = user.userName,
                bio = user.bio,
                email = user.email
            )
            return userModel

    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users")
def getUsersList():    
    return userList

@app.delete("/user/delete/{user_id}")
def deleteUser(user_id: int):    
    
    for user in userList:
        if str(user_id) == user.userId:
            userList.remove(user)
            return Response(status_code=204)

    raise HTTPException(status_code=500, detail="Cannot be deleted")

@app.put("/user/update/{user_id}")
def updateUser(userInfo: UserModel, user_id: int):    
    
    for user in userList:
        if str(user_id) == user.userId:
            user.userName = userInfo.userName
            user.bio = userInfo.bio
            user.email = userInfo.email
            return "updated"

    raise HTTPException(status_code=500, detail="Cannot update")

@app.post("/user/create")
def getUsersList(userInfo: CreateUserModel):  
    if(isEmailUnique(userInfo.email) == False):
        raise HTTPException(status_code=400, detail="Email has been used")

    userData = UserModel(
        userName = userInfo.userName,
        email = userInfo.email,
        bio = userInfo.bio,
        userId = len(userList)
    )
    userList.append(userData)

    return userData

def isEmailUnique(email: str):
    for user in userList:
        if email == user.email:
            return False
    return True