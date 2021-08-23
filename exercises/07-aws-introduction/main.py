import boto3
import logging

from boto3 import exceptions
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')

s3_client = boto3.client(
    's3',
    aws_access_key_id = getenv('AWS_ID'),
    aws_secret_access_key = getenv('AWS_KEY')
)

def create_bucket(name):
    try:
        s3_client.create_bucket(Bucket = name)
    except ClientError as e:
        logging.error(e)
        return False
        
    return True

if create_bucket('s3-matilde-videos'):
    print('Bucket created.')
else:
    print('Failed to create bucket.')
