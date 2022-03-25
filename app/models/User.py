from datetime import date as Date
from app.models.Gender import Gender
from pydantic import  BaseModel,EmailStr
class User(BaseModel):
    username: str
    email:EmailStr
    password: str
    age: int
    birthday: str # work on this later
    gender: Gender
