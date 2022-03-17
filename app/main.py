# framework
from fastapi import Depends, FastAPI,APIRouter
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBasicCredentials
# models
from app.models import user,userupdatepassword,UserLogin
from app.models import Gender
from app.models import userupdateusername as update_user_username
# db
from .database.__init__ import dynamo
# libs
from pydantic import *
import uuid

# app
app = FastAPI()
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
API_Key = "altooro"
app_auth = APIRouter()

@app.on_event("startup")
async def stratup_table():
    dynamo.create_table()
    dynamo.create_users_table()
    # user for tests
    dynamo.put_user(id="1", username="xt", email="tawfiq@altooro.com", password="xt", age=16,birthday="19-05-2006", gender="male")

@app.get("/get/user-by-id-username")
def get_user(id: str,username: str):
    try:
        r= dynamo.get_user(id=id,username=username)
        return r
    except:
        return {"Error":"User Not Found"}

@app.get("/get/allusers")
def getallusers(APIkey: str = Depends(api_key_header)):
    if APIkey == "altooro":
        r = dynamo.get_all_users()
        if r != None:
            return r
    else:
        return {"Error":"Your API Key is wrong"}

@app.put("/update/username/{username}")
def update_username(user: update_user_username,username: str):
    dynamo.update_username(id=user.id ,username=user.username , newusername=username)

@app.put('/update/password/{id}/{password}')
def update_password(id:str,password:str):
    dynamo.update_password(id=id,password=password)

@app.post("/login/{username}/{password}")
def login(username:str,password:str):
    return(dynamo.login(username=username,password=password))

@app.post("/create/user")
def create_user(usr: user):
    usr.dict()
    id = str(uuid.uuid4())
    dynamo.put_user(id=id,username=usr.username,email=usr.email,password=usr.password,age=usr.age,birthday=str(usr.birthday),gender=str(usr.gender))

@app.delete("/delete/user/{id}/{username}")
def delete_user(id: str,username:str):
    return dynamo.delete_user(id=id,username=username)

@app.delete("/delete/all/users")
def delete_all_users(APIkey: str = Depends(api_key_header)):
    if APIkey == "altooro":
        r = dynamo.delete_all_users()
        return r
    return {"Error":"Your API Key is wrong"}