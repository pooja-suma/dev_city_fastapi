from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key= True)
    username = Column(String(50),unique= True, nullable=False )
    password = Column(String(50), nullable= False)
    role = Column(String(200), nullable= False)
    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow, onupdate= datetime.utcnow)
    deleted_at = Column(DateTime, nullable= True)

    profiles = relationship("Profile", back_populates= "owner")


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key= True, index= True)
    user_id = Column(Integer, ForeignKey('user.id'))
    first_name = Column(String(50), nullable= False)
    last_name = Column(String(50), nullable= False)
    email = Column(String(50),unique= True)
    phone = Column(String(50),unique= True)
    avatar = Column(Text, nullable= True)
    exp = Column(String(2), nullable=True)
    skills = Column(Text, nullable=True)
    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow, onupdate= datetime.utcnow)
    deleted_at = Column(DateTime, nullable= True)

    owner = relationship("User", back_populates= "profiles")