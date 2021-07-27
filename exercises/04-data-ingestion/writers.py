import datetime
import json
import os

class DataTypeUnsupported(Exception):
    def __init__(self, data) -> None:
        super().__init__(self.message)
        self.data = data
        self.message = f'Data type {type(data)} unsupported.'

class DataWriter:
    def __init__(self, api: str, coin: str) -> None:
        self.api = api
        self.coin = coin
        self.file_name = f'{self.api}/{self.coin}/{datetime.datetime.now()}.json'

    def _write_row(self, row: str) -> str:
        os.makedirs(os.path.dirname(self.file_name), exist_ok = True)

        with open(self.file_name, 'a') as f:
            f.write(row)

    def write(self, data):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n')
        elif isinstance(data, list):
            for item in data:
                self.write(item)
        else:
            raise DataTypeUnsupported(data)
