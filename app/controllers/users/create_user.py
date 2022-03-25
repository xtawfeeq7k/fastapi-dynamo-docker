from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from app.models.User import User
from app.services.create_user import create_user as create_user_crud
router = APIRouter()

@router.post("/create/user")
def create_user(usr: User):
    try:
        create_user_crud(usr)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response)