import boto3
from botocore.exceptions import ClientError
from app.config import settings


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