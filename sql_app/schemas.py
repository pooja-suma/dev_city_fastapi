from pydantic import BaseModel
from datetime import datetime

class ProfileBase(BaseModel):
    first_name : str
    last_name : str
    email : str
    phone : str
    avatar : str
    exp : str
    skills : str

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id : int
    user_id : int

    class Config():
        orm_mode = True

class UserBase(BaseModel):
    username : str
    role : str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id : int
    profiles : list[Profile] = []
    created_at: datetime

    class Config():
        orm_mode = True

class UserDetails(BaseModel):
    username: str
    old_password: str
    new_password: str

class ForgotPassword(BaseModel):
    username: str

class ResetPassword(BaseModel):
    username: str
    token: str
    password: str

class Login(BaseModel):
    username: str
    password: str


