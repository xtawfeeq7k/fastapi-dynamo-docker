import boto3
from botocore.exceptions import ClientError
from app.config import settings
# functions
from create_table import create_table
from create_user import create_user
from get_users_table import get_users_table

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

dynamo = Dynamo()