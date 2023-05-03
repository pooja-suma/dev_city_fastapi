from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username= user.username, password = fake_hashed_password, role =user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_profiles(db : Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def create_user_profile(db :  Session, profile : schemas.ProfileCreate, user_id : int):
    db_profile = models.Profile(**profile.dict(), user_id= user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
