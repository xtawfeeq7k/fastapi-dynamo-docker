import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table
import uuid
class Dynamo:
    _instances = {}

    def put_user(self,id:str,username:str,email:str,password:str,age:int,gender:str,birthday:str,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,
                                      region_name='eu-central-1', aws_access_key_id="hello",
                                      aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        response = table.put_item(Item={
                'id': id,
                'username': username,
                'email': email,
                'password': password,
                'age': age,
                'gender':gender,
                'birthday':birthday
            }
        )
        return response

    def create_reso(self):
        try:
            if "resource" not in self._instances:
                dynamodb = \
                    boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=False,
                                   region_name='eu-central-1',
                                   aws_access_key_id="hello",
                                   aws_secret_access_key = "hello")
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
                                   region_name='eu-central-1',
                                  aws_access_key_id="hello",
                                  aws_secret_access_key="hello")
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise "Error"

    def create_users_table(dynamodb=None):
        dynamodb = boto3.resource('dynamodb',
                                  endpoint_url=settings.endpoint_url,
                                  verify=False,
                                  region_name='eu-central-1',
                                  aws_access_key_id="hello",
                                  aws_secret_access_key="hello")
        # Table defination
        table = dynamodb.create_table(
            TableName='table',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'username',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    # AttributeType defines the data type. 'S' is string type and 'N' is number type
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                # ReadCapacityUnits set to 10 strongly consistent reads per second
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
            }
        )
        return table

    def get_table(self,dynamodb=None):
        if "table" not in self._instances:
            dynamodb = self.create_reso()
            table = dynamodb.Table(settings.table)
            self._instances["table"] = table
        return self._instances["table"]

    def get_user(self, id, username, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb',endpoint_url=settings.endpoint_url,verify=False,region_name='eu-central-1',aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        try:
            response = table.get_item(Key={'id': id, 'username': username})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def get_all_users(self,dynamodb=None):
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

    def update_username(self,id:str,username:str,newusername:str, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        if self.delete_user(id=id,username=username):
            table.update_item(
                Key={
                    'id': id,
                    'username': username
                },
                UpdateExpression='SET username = :val1',
                ExpressionAttributeValues={
                    ':val1': newusername,
                },
            )

    def delete_user(self,id: str,username:str,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        table.delete_item(
            Key={
                'id':id,
                'username':username,
            }
        )

    def delete_all_users(self,dynamodb=None,responses=[]):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        scan = self.get_all_users()
        for index in scan:
            try:
                r = table.delete_item(Key={
                    "id": index["id"]
                })
                responses.append(r)
            except:
                responses.append(index["id"] + "error")
        return responses

dynamo = Dynamo()