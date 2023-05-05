from sqlalchemy.orm import Session

from . import models, schemas, utils
from random import randint

def get_user(db: Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password(user.password)
    db_user = models.User(username= user.username, password = hashed_password, role =user.role)
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

def change_password(db : Session, user: schemas.UserDetails):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if db_user is None:
        return 'user not found'
    
    if not utils.verify_password(user.old_password, db_user.password):
        return 'old password is incorrect'
    
    hash_password = utils.get_password(user.new_password)
    db_user.password = hash_password

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return 'Password changed successfully'
    return db_user


def forgot_password(db: Session, user: schemas.ForgotPassword):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if db_user is None:
        return 'user not found'
    
    otp = str(randint(1000,9999))

    token = models.Token(
        user_id = db_user.id,
        token = otp
    )

    db.add(token)
    db.commit()

    return 'OTP was sent to your email'

def reset_password(db: Session, user: schemas.ResetPassword):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if db_user is None:
        return 'user not found'
    
    db_token = db.query(models.Token).filter(models.Token.user_id == db_user.id).first()

    if db_token is None:
        return 'Token not found'
    
    if not db_token.token == user.token:
        return 'OTP incorrect'
    
    hash_password = utils.get_password(user.password)
    db_user.password = hash_password

    db.commit()

    return 'Password reset successfully'

    
    


    


