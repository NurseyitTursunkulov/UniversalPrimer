from databases import Database
from database import Base
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    tax = Column(Float, default=0.0)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    hashed_password: str

class PasswordChange(BaseModel):
    new_password:str
