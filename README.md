## FastAPI DynamoDB Task

## Running
```shell
$ python -m venv env

$ source env/Scripts/activate

$ pip install -r requirements.txt

$ docker-compose up --build
```

## Task:

* your task is to create a database application for sign up/log in
* overall the functionality that should be included is:
  * Login in
  * Sign up
  * Change password
  * Change username/email
  * get user details
  * get all users (this should have an authorization check)
  * delete user
  * Delete all users
* The technology you will use is:
  * FastAPI
  * Docker
  * DynamoDB
* Each user should have at least the following:
  * Username
  * Email
  * Password
  * Age
  * Birthday
  * Gender
* Note:
  * You need to create the database using Boto3
  * You need to create all of the Models using Pydantic