# framework
from fastapi import Depends, FastAPI,APIRouter
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBasicCredentials
# models
from app.models import user,userupdatepassword,UserLogin
from app.models import Gender
from app.models import userupdateuseremail as update_user_username_email
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


@app.post("/create/user")
def create_user(usr: user):
    usr.dict()
    id = str(uuid.uuid4())
    dynamo.put_user(id=id,username=usr.username,email=usr.email,password=usr.password,age=usr.age,birthday=str(usr.birthday),gender=str(usr.gender))

@app.get("/get/user-by-id-username")
def get_user(id: str,username: str):
    r= dynamo.get_user(id=id,username=username)
    if r != None:
        return r
    else:
        return {"Error":"User Not Found"}

@app.get("/get/allusers")
def getallusers(APIkey: str = Depends(api_key_header)):
    if APIkey == "altooro":
        r = dynamo.get_all_users()
        if r != None:
            return r
    else:
        return {"Error":"Your API Key is wrong"}

@app.put("/update/username-email")
def update_username_email(user: update_user_username_email):
    if get_user(user.id,user.username):
        try:
            dynamo.update_username_email(id=user.id,username=user.username,email=user.email)
            return {"Message":"User Updated Succsessfully"}
        except:
            return {"Error":"Somthing Wrong Happen"}
    else:
        return {"Error":"User Not Found"}

@app.delete("/delete/user/{id}")
def delete_user(id: str):
    return dynamo.delete_user(id)

@app.delete("/delete/all/users")
def delete_all_users():
    return dynamo.delete_all_users()

@app.get("/response-test",tags=["test"])
def responsetest():
    return dynamo.response_test()