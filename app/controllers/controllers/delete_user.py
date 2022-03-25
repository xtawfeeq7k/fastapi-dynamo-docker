from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from app.services.delete_user import delete_user as delete_user_crud
router = APIRouter()
@router.delete("/{id}/{username}")
def delete_user(id: str,username:str):
    try:
        return delete_user_crud(id=id,username=username)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response)