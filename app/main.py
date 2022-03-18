# framework
from fastapi import Depends, FastAPI,APIRouter
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBasicCredentials
# libs
from pydantic import *
import uuid
# models
from app.models import user,userupdatepassword,UserLogin
from app.models import Gender
from app.models import userupdateusername as update_user_username
# db
from .database.__init__ import dynamo
from .database.create_user import create_user as db_create_user
from .database.delete_all_users import delete_all_users as db_delete_all_users
from .database.delete_user import delete_user as db_delete_user
from .database.get_user import get_user as db_get_user
from .database.login import login as db_login
from .database.get_all_users import get_all_users as db_get_all_users

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
    db_create_user(id=str("1"), username="xt", email="tawfiq@altooro.com", password="xt", age=16,birthday="19-05-2006", gender="male")

@app.get("/get/user-by-id-username")
def get_user(id: str,username: str):
    try:
        r= db_get_user(id=id,username=username)
        return r
    except:
        return {"Error":"User Not Found"}

@app.get("/get/allusers")
def getallusers(APIkey: str = Depends(api_key_header)):
    if APIkey == "altooro":
        r = db_get_all_users()
        if r != None:
            return r
    else:
        return {"Error":"Your API Key is wrong"}

@app.put("/update/username/{username}" , tags=["not working"])
def update_username(user: update_user_username,username: str):
    dynamo.update_username(id=user.id ,username=user.username , newusername=username)

@app.put('/update/password/{id}/{password}' , tags=['not working'])
def update_password(id:str,password:str):
    dynamo.update_password(id=id,password=password)

@app.post("/login/{username}/{password}")
def login(username:str,password:str):
    return(db_login(username=username,password=password))

@app.post("/create/user")
def create_user(usr: user):
    id = str(uuid.uuid4())
    db_create_user(id=str(id),username=usr.username,email=usr.email,password=usr.password,age=usr.age,birthday=str(usr.birthday),gender=str(usr.gender))

@app.delete("/delete/user/{id}/{username}")
def delete_user(id: str,username:str):
    return db_delete_user(id=id,username=username)

@app.delete("/delete/all/users")
def delete_all_users_(APIkey: str = Depends(api_key_header)):
    if APIkey == "altooro":
        r = db_delete_all_users()
        return r
    return {"Error":"Your API Key is wrong"}
