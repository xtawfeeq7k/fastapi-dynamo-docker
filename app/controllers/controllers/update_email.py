from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from app.services.update_email import update_email as update_email_crud
from app.models.update_email import Update_Email as u
router = APIRouter()
@router.put("/email")
def update_email(usr: u):
    try:
        update_email_crud(usr)
    except ClientError as e:
        raise HTTPException(status_code=400,detail=e.response)