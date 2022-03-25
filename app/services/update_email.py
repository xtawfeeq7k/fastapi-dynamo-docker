from app.config import settings
from app.database import dynamo as dynamodb
from app.models.update_email import Update_Email as u
def update_email(usr: u):
    table = dynamodb.get_resource().Table(settings.table)
    response = table.update_item(
        Key={
            'id': usr.id,
            'username': usr.username,
        },
        UpdateExpression="set email = :r",
        ExpressionAttributeValues={
            ':r': usr.newemail,
        },
        ReturnValues="UPDATED_NEW"
    )