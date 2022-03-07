import boto3
from botocore.exceptions import ClientError
from app.config import settings

def get_users_table(self):
    if "users" not in self._instances:
        dynamodb = self.create_reso()
        table = dynamodb.Table(settings.table)
        self._instances["users"] = table
    return self._instances["users"]