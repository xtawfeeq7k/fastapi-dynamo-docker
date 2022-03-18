import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def login(username: str, password: str, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,
                                  region_name='eu-central-1', aws_access_key_id="hello", aws_secret_access_key="hello")
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