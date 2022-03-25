from app.config import settings
from app.database import dynamo as dynamodb
from app.models.update_password import Update_Password as u
def update_password(usr: u):
    table = dynamodb.get_resource().Table(settings.table)
    response = table.update_item(
        Key={
            'id': usr.id,
            'username': usr.username,
        },
        UpdateExpression="set password = :r",
        ExpressionAttributeValues={
            ':r': usr.password,
        },
        ReturnValues="UPDATED_NEW"
    )