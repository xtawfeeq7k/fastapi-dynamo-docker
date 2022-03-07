import boto3
from botocore.exceptions import ClientError
from app.config import settings

def create_user(self, user):
    try:
        if user.id not in self._instances['created_users']:
            dynamodb = self.create_reso()
            table = dynamodb.Table('users')
            response = table.get_item(

                Key={

                    'id': user.id,
                    'username': user.username,
                    'email': str(user.email),
                    'password': user.password,
                    'age': user.age,
                    'gender': user.gender,
                    'birthday': str(user.birthday)

                }

            )

            if 'Item' in response:

                return response['Item']

            else:

                return {

                    'statusCode': '404',

                    'body': 'Not found'

                }
        else:
            return {'Error': 'User in already exists'}

    except ClientError as e:
        pass