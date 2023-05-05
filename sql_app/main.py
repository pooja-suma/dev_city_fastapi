from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username = user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def show_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{username}", response_model=schemas.User)
def show_single_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/profiles/", response_model=schemas.Profile)
def create_profile_for_user(
    user_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)
):
    return crud.create_user_profile(db=db, profile=profile, user_id=user_id)


@app.get("/profiles/", response_model=list[schemas.Profile])
def show_all_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles

@app.post("/change_password/")
def change_password(user: schemas.UserDetails, db: Session= Depends(get_db)):
    result = crud.change_password(db, user = user)
    return result

@app.post("/forgot_password")
def forgot_password(user: schemas.ForgotPassword, db: Session= Depends(get_db)):
    result = crud.forgot_password(db, user=user)
    return result

@app.post("/reset_password")
def reset_password(user: schemas.ResetPassword, db: Session= Depends(get_db)):
    result = crud.reset_password(db, user=user)
    return result
