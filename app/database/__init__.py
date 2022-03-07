import boto3
from botocore.exceptions import ClientError
from app.config import settings

class Dynamo:
    _instances = {

    }
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


    def get_table(self):
        if "table" not in self._instances:
            dynamodb = self.create_reso()
            table = dynamodb.Table(settings.table)
            self._instances["table"] = table
        return self._instances["table"]


dynamo = Dynamo()
