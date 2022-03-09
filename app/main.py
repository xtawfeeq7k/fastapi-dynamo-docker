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

# fake users db
users = {
    "xt": {
        "id":"74ffb6ee-c413-47ae-875a-14cb2b07bd51",
        "username":"xt",
        "email": "tawfiq@altooro.com",
        "password":"xt",
        "gender":"male",
        "birthday":"19.5",
        "age":16,

    },
}
# api key
APIKey = "123"

# db

@app.on_event("startup")
async def stratup_table():
    dynamo.create_table()

@app.get("/get/table")
async def get_table():
    return dynamo.get_table()

@app.get("/getuser/{username}", tags=["Users"])
async def GetUserByUsername(username: str):
    return users[username]

@app.get("/getallusers", tags=["Users"])
async def getAllUsers(api_key: APIKeyHeader = Depends(api_key_header)):
    if api_key == APIKey:
        return users
    else:
        return {"Error":"You're API Key is wrong"}

@app.put("/updateuser/", tags=["Users"])
async def UpdateUser(upduser: update_user_username_email):
    if upduser.username not in users:
        return {"Error":"User Not Found"}
    if upduser.username != "string":
        users[upduser.username]= upduser.username
        users[upduser.username]["username"]= upduser.username
    if upduser.email != "string":
        users[upduser.username]["email"] = upduser.email
    return users[user.username]

@app.get("/getuserbyemail/{email}", tags=["Users"])
def getUserByEmail(email: str):
    for usr in users:
        if users[usr]["email"]==email:
            return usr
    return {"Error":"User Not Found"}

@app.put("/updatepassword/{password}", tags=["Users"])
async def ChangePassword(user: userupdatepassword):
    if user.password != None or user.password != "string":
        users[user.username]["password"] = user.password
    return {"Data":"Password Changed Succsessfully"}

@app.post("/signup", tags=["Users"])
async def signup(User: user):
    if User.username in users:
        return {"Error":"This username exists"}
    users[User.username] = User
    x = User.username
    try:
        users[x]["id"] = str(uuid.uuid4())
    except:
        pass
    return users[User.username]

@app.post("/login", tags=["Users"])
async def login(User: UserLogin):
    if UserLogin.username not in users:
        return {"Error":"User Not Found"}
    if UserLogin.password == users[UserLogin]["password"]:
        return {"Data":"Logged in Succsessfully"}

@app.delete("/delete-user/{username}", tags=["Users"])
def DeleteUserByID(username: str , api_key: APIKeyHeader = Depends(api_key_header)):
    if username not in users:
        return {"Eroor":"Can't Find the User"}
    del users[username]
    return {"Data":"User Deleted Succsessfully"}

@app.delete("/delete-allusers/", tags=["Users"])
def DeleteAllUsers(api_key: APIKeyHeader = Depends(api_key_header)):
    temparr = []
    for key in users:
        temparr.append(key)
    for i in range(len(temparr)):
        del users[temparr[i]]
    return {"Data": "Users Deleted Succsessfully"}
