from app.config import settings
from app.database import dynamo as dynamodb
def login(username: str, password: str):
    table = dynamodb.get_resource().Table(settings.table)
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