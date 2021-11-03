import boto3
import logging
import pandas as pd

from abc import ABC
from botocore import exceptions
from botocore.exceptions import ClientError
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

load_dotenv('/opt/outputs/.env')


class AwsAirflow(ABC):
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY')
        )
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY')
        )

    def _check_bucket(self) -> None:
        try:
            self.s3_client.list_buckets()['Buckets'][0]['Name']
        except IndexError:
            print('Bucket no found.')
            return True
        
        return False

    def _create_bucket(self, name) -> bool:
        try:
            self.s3_client.create_bucket(Bucket = name)
        except ClientError as e:
            logging.error(e)
            return False

        return True

    def download_data(self):
        url = 'https://s3-sa-east-1.amazonaws.com/'

        df = pd.read_csv(url)
        df.to_csv('/opt/airflow/outputs/data.csv', index = False)

    def send_file(self) -> None:
        cur_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.s3_resource.Bucket('cf-s3-bucket').upload_file(
            '/opt/airflow/outputs/data.csv',
            f"airflow/data/inputs/data_{cur_time}.csv"
        )

    def run(self) -> None:
        if self._check_bucket():
            self._create_bucket('cf-s3-bucket')
            print('Bucket created.')
        else:
            print(f"Bucket already exists: {self.s3_client.list_buckets()['Buckets'][0]['Name']}")



