from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, Depends
from app.services.delete_all_users import delete_all_users as delete_all_users_crud
from app.models.constans import api_key_header
from app.models.constans import api_key
router = APIRouter()

@router.delete("/all")
def delete_all_users_(APIkey: str = Depends(api_key_header)):
    try:
        if APIkey == api_key:
            r = delete_all_users_crud()
            return r
        return {"Error":"Your API Key is Wrong"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response)