import boto3
from botocore.exceptions import ClientError
from app.config import settings

class Dynamo:
    _instances = {

    }
    # crate response
    def create_reso(self):
        try:
            if "resource" not in self._instances:
                dynamodb = \
                    boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=False,
                                   region_name='dummy')
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise e



    def create_table(self,dynamodb=None):
        try:
            if not dynamodb or "resource" not in self._instances:
                dynamodb = boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=False,
                                   region_name='dummy')
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise "Error"

    def create_table2(self,dynamodb=None):
        table = dynamodb.create_table(
            TableName='table',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'S'  # Sort key
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        self._instances["created_table"] = True
        return table

    def get_table(self):
        if "table" not in self._instances:
            dynamodb = self.create_reso()
            table = dynamodb.Table(settings.table)
            self._instances["table"] = table
        return table

    def create_user(self, user):
        try:
            if user.id not in self._instances['created_users']:
                dynamodb = self.create_reso()
                table = dynamodb.Table('table')
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
dynamo = Dynamo()
