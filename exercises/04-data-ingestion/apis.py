import datetime
import json
import logging
import os
import ratelimit
import requests
import time

from abc import ABC, abstractmethod
from backoff import expo, on_exception
from schedule import repeat, every, run_pending

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class ApiMercadoBitcoin(ABC):
    def __init__(self, coin: str) -> None:
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'
        self.coin = coin

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    @on_exception(expo, ratelimit.RateLimitException, max_tries = 10)
    @ratelimit.limits(calls = 29, period = 30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries = 10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Getting data from {endpoint}')

        response = requests.get(endpoint)
        response.raise_for_status()

        return response.json()

class ApiDaySummary(ApiMercadoBitcoin):
    def _get_endpoint(self, date: datetime.date) -> str:
        return f'{self.base_endpoint}/{self.coin}/day-summary/{date.year}/{date.month}/{date.day}'

class ApiTrades(ApiMercadoBitcoin):
    def _get_date_unix(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime, date_to: datetime.datetime) -> str:
        if date_from > date_to:
            raise RuntimeError("The 'date_from' must be greater or equal than 'dat_from'")
        else:
            date_from_unix = self._get_date_unix(date_from)
            date_to_unix = self._get_date_unix(date_to)
            
            return f'{self.base_endpoint}/{self.coin}/trades/{date_from_unix}/{date_to_unix}'

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

class DataIngestor(ABC):
    def __init__(self, writer: DataWriter, coins, default_date_from: datetime.date) -> None:
        self.writer = writer
        self.coins = coins
        self.default_date_from = default_date_from
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self) -> str:
        return f'{self.__class__.__name__}.checkpoint'

    def _save_checkpoint(self):
        with open(self._checkpoint_filename, 'w') as f:
            f.write(f'{self._checkpoint}')

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, 'r') as f:
                return datetime.datetime.strptime(f.read(), '%Y-%m-%d').date()
        except FileNotFoundError:
            return None
    
    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_date_from
        else:
            return self._checkpoint

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._save_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass

class IngestorDaySummary(DataIngestor):
    def ingest(self) -> None:
        date = self._get_checkpoint()

        if date < datetime.date.today():
            for coin in self.coins:
                api = ApiDaySummary(coin = coin)
                data = api.get_data(date = date)
                self.writer(api = 'day-summary', coin = coin).write(data)
            
            self._update_checkpoint(date + datetime.timedelta(days = 1))

ingestor = IngestorDaySummary(writer = DataWriter, coins = ['BTC', 'ETH', 'LTC', 'BCH'], default_date_from = datetime.date(2021, 7, 1))

@repeat(every(1).seconds)
def job():
    ingestor.ingest()

while True:
    run_pending()
    time.sleep(.5)