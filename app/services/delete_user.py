from app.config import settings
from app.database import dynamo as dynamodb

def delete_user(id: str, username: str):
    table = dynamodb.get_resource().Table(settings.table)
    table.delete_item(
        Key={
            'id': id,
            'username': username,
        }
    )