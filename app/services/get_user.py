from botocore.exceptions import ClientError
from app.config import settings
from app.database import dynamo as dynamodb

def get_user(id: str, username:str ):
    table = dynamodb.get_resource().Table(settings.table)
    try:
        response = table.get_item(Key={'id': id, 'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']