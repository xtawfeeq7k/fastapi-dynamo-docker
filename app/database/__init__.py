import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table
class Dynamo:
    _instances = {}

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

    # not ready yet
    def update_username(self,id:str,username:str,newusername:str, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        if self.get_user(id=id,username=username):
            response = table.update_item(
                Key={
                    'id': id,
                },
                UpdateExpression='SET username = :newUserName',
            ConditionExpression = 'attribute_not_exists(deletedAt)',
            ExpressionAttributeValues = {':newUserName': newusername,},ReturnValues = "UPDATED_NEW",)
        return(response)

    def update_password(self,id:str,password:str,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table(settings.table)
        response = table.update_item(
            Key={
                'id': id,
            },
            UpdateExpression="set password = :r",
            ExpressionAttributeValues={
                ':r': password,
            },
            ReturnValues="UPDATED_NEW"
        )

dynamo = Dynamo()