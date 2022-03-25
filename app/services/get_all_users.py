from app.config import settings
from app.database import dynamo as dynamodb
def get_all_users():
    table = dynamodb.get_resource().Table(settings.table)
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data