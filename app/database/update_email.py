import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def update_email(id: str, username: str, newpassword: str, dynamodb=None):
    if not dynamodb:
        dynamodb = \
            boto3.resource('dynamodb',
                           endpoint_url=settings.endpoint_url,
                           verify=settings.verify,
                           region_name=settings.region_name,
                           aws_access_key_id=settings.aws_access_key_id,
                           aws_secret_access_key=settings.aws_secret_access_key)
    table = dynamodb.Table(settings.table)
    response = table.update_item(
        Key={
            'id': id,
            'username': username
        },
        UpdateExpression='SET username = :newUserName',
        ConditionExpression='attribute_not_exists(deletedAt)',
        ExpressionAttributeValues={':newUserName': newpassword, }, ReturnValues="UPDATED_NEW", )
    return response