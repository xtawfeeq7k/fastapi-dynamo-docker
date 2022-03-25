from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from app.services.get_user import get_user as get_user_crud
from app.services.delete_user import delete_user as delete_user_crud
from app.services.create_user import create_user as create_user_crud
from app.models.update_username import Update_Username as u
router = APIRouter()
@router.put("/username")
def update_username(user: u):
    try:
        usr = get_user_crud(id=user.id,username=user.username)
        delete_user_crud(id=user.id,username=user.username)
        usr.username=user.newusername
        create_user_crud(usr)
        return usr
    except ClientError as e:
        raise HTTPException(status_code=400,detail=e.response)