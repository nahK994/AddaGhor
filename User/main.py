from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional, List

app = FastAPI()

class UserInfo(BaseModel):
    userName: str
    bio: Optional[str] = None
    email: str

class UserModel(BaseModel):
    userId: str
    userName: str
    bio: Optional[str] = None
    email: str

userList: List[UserModel] = []

@app.get("/users/{user_id}")
def getUser(user_id: int):    
    for user in userList:
        if user.userId == str(user_id):
            userInfo = UserInfo(
                userName = user.userName,
                bio = user.bio,
                email = user.email
            )
            return userInfo

    return "User not found"

@app.get("/users")
def getUsersList():    
    return userList

@app.delete("/user/delete/{user_id}")
def deleteUser(user_id: int):    
    
    for user in userList:
        if str(user_id) == user.userId:
            userList.remove(user)
            return "deleted"

    return "can not be deleted"

@app.put("/user/update/{user_id}")
def updateUser(userInfo: UserInfo, user_id: int):    
    
    for user in userList:
        if str(user_id) == user.userId:
            user.userName = userInfo.userName
            user.bio = userInfo.bio
            user.email = userInfo.email
            return "updated"

    return "can not be updated"

@app.post("/user/create")
def getUsersList(userInfo: UserInfo):    
    if(isEmailUnique(userInfo.email) == False):
        return "Email has been used"

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