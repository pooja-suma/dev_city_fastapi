from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from . import crud, models, schemas, utils
from .database import SessionLocal, engine
from fastapi import status, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pydantic import parse_obj_as
from fastapi.exceptions import HTTPException
import os, shutil

SECRET_KEY = "3c492103ee725d778784f6ec01128887bb45176b4963d98153aed911c2622f91"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

@app.post("/login")
def login(user: schemas.Login, db:Session= Depends(get_db)):
    result = crud.login(db,user = user)
    return result

@app.delete("/user/{id}")
def delete_id(id:int, db:Session= Depends(get_db)):
    result = crud.delete(db, id = id)
    return result

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session= Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session= Depends(get_db)
):
    user_obj = parse_obj_as(schemas.Login, {'username' :form_data.username,
                           'password': form_data.password})
    user = crud.login(db, user_obj)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/uploadfile")
async def upload_file(file: UploadFile):
    file.file.seek(0, 2)
    file_size = file.file.tell()

    await file.seek(0)

    if file_size > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    upload_dir = os.path.join(os.getcwd(), "uploads")
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    dest = os.path.join(upload_dir, file.filename)
    print(dest)

    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename":file.filename}






# @app.post("/files")
# async def UploadImage(file: bytes = File(...)):
#     with open('images.jpeg','wb') as image:
#         image.write(file)
#         image.close() 
#     return 'Avatar uploaded'
