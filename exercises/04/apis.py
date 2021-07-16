import datetime
import logging
import requests

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class ApiMercadoBitcoin(ABC):
    def __init__(self, coin: str) -> None:
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'
        self.coin = coin

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

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

# TO DO
class DataWriter():
    pass

# api = ApiDaySummary(coin = 'BTC')
# data = api.get_data(date = datetime.date(2021, 7, 1))
# print(data)

# api = ApiTrades(coin = 'BTC')
# data = api.get_data(date_from = datetime.datetime(2021, 7, 1), date_to = datetime.datetime(2021, 6, 2))
# print(data)