from enum import Enum
from pydantic import *
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import date, datetime, time, timedelta

# enum
class gender(str, Enum):
    gender1 = 'male'
    gender2 = 'female'

# user
class user(BaseModel):
    username: str
    email:EmailStr
    password: str
    age: int
    birthday: date

class userupdateuseremail(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]

class userupdatepassword(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
