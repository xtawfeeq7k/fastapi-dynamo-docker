import boto3
from botocore.exceptions import ClientError
from app.config import settings

class Dynamo:
    _instances = {
        'created_users':[]
    }

    # crate response
    def create_reso(self):
        try:
            if "resource" not in self._instances:
                dynamodb = \
                    boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=False)
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise e

    # create table
    def create_table(self):
        try:
            if "created_table" not in self._instances:
                dynamodb = self.create_reso()
                table = \
                    dynamodb.create_table(
                        TableName="users",
                        KeySchema=[
                            {
                                'AttributeName': 'id',
                                'KeyType': 'HASH'
                            }
                        ],
                        AttributeDefinitions=[
                            {
                                'AttributeName': 'id',
                                'AttributeType': 'S'
                            },
                        ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                        }
                    )
                self._instances["created_table"] = True
        except ClientError as e:
            pass

    # create user (should edit)
    def create_user(self,user):
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
                return {'Error':'User in already exists'}

        except ClientError as e:
            pass


    def get_users_table(self):
        if "users" not in self._instances:
            dynamodb = self.create_reso()
            table = dynamodb.Table(settings.table)
            self._instances["users"] = table
        return self._instances["users"]


dynamo = Dynamo()
