import uuid
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.database import dynamo as dynamodb
from app.models.User import User
from app.config import settings

def create_user(usr: User):
    id = str(uuid.uuid4())
    try:
        table = dynamodb.get_resource().Table(settings.table)
        response = table.put_item(
            Item={'id': id, **usr.dict()})
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response)
    return response