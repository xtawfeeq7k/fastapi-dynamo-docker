# framework
from fastapi import Depends, FastAPI,APIRouter
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBasicCredentials
# models
from app.models import user,userupdatepassword,UserLogin
from app.models import gender as Gender
from app.models import userupdateuseremail as update_user_username_email
# db
from .database.__init__ import dynamo
# libs
from pydantic import *
import uuid

# app
app = FastAPI()
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
app_auth = APIRouter()

@app.on_event("startup")
async def stratup_table():
    dynamo.create_table()

@app.get("/get/user-by-id-username")
def get_user(id: str,username: str):
    dynamo.get_user(id=id,username=username)

@app.get("/get/allusers")
def getallusers():
    dynamo.get_all_users()

@app.post("/create/user")
def create_user():
    dynamo.put_movie(title="hi", year="hh", plot="hi", rating="alo")

@app.get("/response-test")
def responsetest():
    return dynamo.response_test()
