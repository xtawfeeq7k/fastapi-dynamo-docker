from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from app.services.get_user import get_user as get_user_crud
from app.services.delete_user import delete_user as delete_user_crud
from app.config import settings
from app.models.update_username import Update_Username as u
from app.database import dynamo as dynamodb
router = APIRouter()
@router.put("/username")
def update_username(user: u):
    try:
        table = dynamodb.get_resource().Table(settings.table)
        usr = get_user_crud(id=user.id,username=user.username)
        delete_user_crud(id=user.id,username=user.username)
        response = table.put_item(
            Item={
                'id': user.id,
                'username': user.newusername,
                'email': usr['email'],
                'gender': usr['gender'],
                'birthday': usr['birthday'],
            })

        return usr
    except ClientError as e:
        raise HTTPException(status_code=400,detail=e.response)