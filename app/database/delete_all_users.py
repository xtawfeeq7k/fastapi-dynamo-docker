import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table

def delete_all_users( dynamodb=None, responses=[]):
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