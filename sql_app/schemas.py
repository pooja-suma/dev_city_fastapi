from pydantic import BaseModel

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

    class Config():
        orm_mode = True

