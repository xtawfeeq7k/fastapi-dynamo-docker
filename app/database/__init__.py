import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table
class Dynamo:
    _instances = {}

    def get_resource(self):
        try:
            if "resource" not in self._instances:
                dynamodb = \
                    boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=settings.verify,
                                   region_name=settings.region_name,
                                   aws_access_key_id=settings.aws_access_key_id,
                                   aws_secret_access_key = settings.aws_secret_access_key)
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise e

    def create_users_table(self):
        dynamodb = \
            boto3.resource('dynamodb',
                           endpoint_url=settings.endpoint_url,
                           verify=settings.verify,
                           region_name=settings.region_name,
                           aws_access_key_id=settings.aws_access_key_id,
                           aws_secret_access_key=settings.aws_secret_access_key)
        # Table defination
        table = dynamodb.create_table(
            TableName=settings.table,
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

    # Returns the table called Table
    def get_table(self):
        if settings.table not in self._instances:
            dynamodb = self.get_resource()
            table = dynamodb.Table(settings.table)
            self._instances["table"] = table
        return self._instances["table"]

dynamo = Dynamo()