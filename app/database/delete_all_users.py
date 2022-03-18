import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def delete_all_users( dynamodb=None, responses=[]):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,
                                  region_name='eu-central-1', aws_access_key_id="hello", aws_secret_access_key="hello")
    table = dynamodb.Table(settings.table)
    response = table.scan()
    scan = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        scan.extend(response['Items'])
    for index in scan:
        try:
            r = table.delete_item(Key={
                "id": index["id"],
                'username': index['username']
            })
            responses.append(r)
        except:
            responses.append((index["id"],None))