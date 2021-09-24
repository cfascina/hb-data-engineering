import boto3
import datetime
import json
import os

from tempfile import NamedTemporaryFile


class DataTypeUnsupported(Exception):
    def __init__(self, data) -> None:
        super().__init__(self.message)
        self.data = data
        self.message = f"Data type {type(data)} unsupported."


class DataWriter:
    def __init__(self, api: str, coin: str) -> None:
        self.api = api
        self.coin = coin
        self.file_name = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> str:
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)

        with open(self.file_name, "a") as f:
            f.write(row)

    def _write_to_file(self, data):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, list):
            for item in data:
                self.write(item)
        else:
            raise DataTypeUnsupported(data)

    def write(self, data):
        self._write_to_file(data=data)


class S3DataWriter(DataWriter):
    def __init__(self, api: str, coin: str) -> None:
        super().__init__(api, coin)
        self.temp_file = NamedTemporaryFile()
        self.client = boto3.client("s3")
        self.key = f"mercado-bitcoin/{self.api}/coin={self.coin}/extracted-at={datetime.datetime.now().date()}/{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> str:
        with open(self.temp_file.name, "a") as f:
            f.write(row)

    def write(self, data):
        self._write_to_file(data=data)
        self._write_at_s3()

    def _write_at_s3(self):
        self.client.put_object(
            Body=self.temp_file, Bucket="mercado-bitcoin", Key=self.key
        )
