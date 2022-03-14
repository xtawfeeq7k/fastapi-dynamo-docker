import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table
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
    # get_all_users
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


    # insert item > not working
    def insert_items(self,id: str,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.endpoint_url, verify=False,region_name='eu-central-1', aws_access_key_id="hello",aws_secret_access_key="hello")
        table = dynamodb.Table('table')
        response = table.put_item(
            Item={
                "id":id
            }
        )
        self._instances["created_users"].append(id)

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
