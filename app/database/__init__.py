import boto3
from botocore.exceptions import ClientError
from app.config import settings

class Dynamo:
    _instances = {
        "created_users": []
    }
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

    # get_all_users > working
    def get_all_users(self,dynamodb=None,users=[]):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        for user in self._instances["created_users"]:
            try:
                response = table.get_item(Key={'id': id})
                user.append(response)
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                users.append(response['Item'])
        return users

    def response_test(self):
        return "hey!"

    # create user > not working ( example )
    def put_movie(self ,title, year, plot, rating, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")

        table = dynamodb.Table('table')
        response = table.put_item(
            Item={
                'year': year,
                'title': title,
                'info': {
                    'plot': plot,
                    'rating': rating
                }
            }
        )
        return response

dynamo = Dynamo()
