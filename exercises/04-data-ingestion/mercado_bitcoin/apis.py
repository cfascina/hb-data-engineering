import datetime
import logging
import ratelimit
import requests

from abc import ABC, abstractmethod
from backoff import expo, on_exception

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
    def _get_date_unix(self, day: datetime.datetime) -> int:
        return int(day.timestamp())

    def _get_endpoint(self, day: datetime.datetime) -> str:
        if day == datetime.datetime.today().strftime('%Y-%m-%d'):
            raise RuntimeError("Can't request for current day.")
        else:
            day_unix = self._get_date_unix(day)
            return f'{self.base_endpoint}/{self.coin}/trades/{day_unix}'