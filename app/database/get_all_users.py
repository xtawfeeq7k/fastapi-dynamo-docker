import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def get_all_users(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,
                                  region_name='eu-central-1', aws_access_key_id="hello",
                                  aws_secret_access_key="hello")
    table = dynamodb.Table(settings.table)
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data