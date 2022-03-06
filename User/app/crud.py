from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.userId == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def update_user(db: Session, userInfo: schemas.CreateUserModel, user_id: int):
    db.query(models.User.userId == user_id).update(
        {
            "userName": userInfo.userName,
            "email": userInfo.email,
            "bio": userInfo.bio,
            "occupation": userInfo.occupation,
            "password": userInfo.password
        }
    )
    db.commit()

def create_user(db: Session, userInfo: schemas.CreateUserModel):
    userData = models.User(
        userName = userInfo.userName,
        email = userInfo.email,
        bio = userInfo.bio,
        password = userInfo.password,
        occupation = userInfo.occupation
    )

    db.add(userData)
    db.commit()
    db.refresh(userData)
    return userData