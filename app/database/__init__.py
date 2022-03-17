import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table
import uuid
class Dynamo:
    _instances = {}

    # create user > working
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
    # create response > working
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

    # create_table > working
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

    # get_table > working
    def get_table(self,dynamodb=None):
        if "table" not in self._instances:
            dynamodb = self.create_reso()
            table = dynamodb.Table(settings.table)
            self._instances["table"] = table
        return self._instances["table"]

    # get_user > working
    def get_user(self, id, username, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb',endpoint_url=settings.endpoint_url,verify=False,region_name='eu-central-1',aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        try:
            response = table.get_item(Key={'id': id, 'username': username})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def get_user_by_id(self,id:str,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb',endpoint_url=settings.endpoint_url,verify=False,region_name='eu-central-1',aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        try:
            response = table.get_item(Key={'id': id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    # get_all_user
    def get_all_users(self,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,
                                      region_name='eu-central-1', aws_access_key_id="hello",
                                      aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data

    def response_test(self,dynamodb=None):
        return "hey!"

    # update_user
    def update_username_email(self,id: str, username: str = None , email: str = None, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        if self.get_user_by_id(id)!=None:
            if username != None:
                response = table.update_item(
                    Key={'id': id},
                    AttributeUpdates={
                    'username': username,
                    },
                    ConditionExpression = 'attribute_not_exists(deletedAt)',  # Do not update if deleted
                    ExpressionAttributeValues={
                        'username': username
                    },
                    ReturnValues="UPDATED_NEW"
                )
            if email != None:
                response2 = table.update_item(
                    Key={'id': id},
                    AttributeUpdates={
                        'email': email,
                    },
                    ConditionExpression = 'attribute_not_exists(deletedAt)',  # Do not update if deleted
                    ExpressionAttributeValues={
                        'email': email
                    },
                    ReturnValues="UPDATED_NEW")
            return {
                "username":response,
                "email":response2,
            }
        else:
            return {"Error":"User Not Found"}

    def delete_user(self,id: str,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        if self.get_user_by_id(id=id):
            response = table.table.delete_item(Key={
                "id": id
            })
            return response
        else:
            return {"Error":"User not Found"}

    def delete_all_users(self,dynamodb=None,responses=[],i=0):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        for index in self._instances["created_users"]:
            response = self.delete_user(id=index)
            responses[i]=response
            i+=1
        return responses

dynamo = Dynamo()