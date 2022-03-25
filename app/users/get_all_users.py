from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException
from app.services.get_all_users import get_all_users as get_all_users_crud
from app.models.constans import api_key_header
from app.models.constans import api_key
router = APIRouter()

@router.get("/all")
def getallusers(APIkey: str = Depends(api_key_header)):
    try:
        if APIkey == str(api_key):
            r = get_all_users_crud()
            if r:
                return r
        return {"Error":"Your API Key is wrong"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response)