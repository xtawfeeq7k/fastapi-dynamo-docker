from enum import Enum
from pydantic import *
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import date, datetime, time, timedelta

# enum
class Gender(str, Enum):
    gender1 = 'male'
    gender2 = 'female'

# user
class user(BaseModel):
    username: str
    email:EmailStr
    password: str
    age: int
    birthday: date
    gender: Gender

class userupdateusername(BaseModel):
    id: str
    username: str

class userupdatepassword(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
