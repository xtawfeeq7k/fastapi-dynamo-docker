import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def get_user(id: str, username:str , dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,
                                  region_name='eu-central-1', aws_access_key_id="hello", aws_secret_access_key="hello")
    table = dynamodb.Table(settings.table)
    try:
        response = table.get_item(Key={'id': id, 'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']