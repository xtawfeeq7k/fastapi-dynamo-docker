import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def login(username: str, password: str, dynamodb=None):
    if not dynamodb:
        dynamodb = \
            boto3.resource('dynamodb',
                           endpoint_url=settings.endpoint_url,
                           verify=settings.verify,
                           region_name=settings.region_name,
                           aws_access_key_id=settings.aws_access_key_id,
                           aws_secret_access_key=settings.aws_secret_access_key)
    table = dynamodb.Table(settings.table)
    response = table.scan()
    users = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        users.extend(response['Items'])
    for user in users:
        if user["username"] == username and user["password"] == password:
            return {'Message': 'Logged in Succsessfully'}
        if user["username"] == username:
            return {'Message': 'Incorrect username or password'}
    return {'Message': 'Incorrect username or password'}