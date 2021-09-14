import datetime

from abc import ABC, abstractmethod
from apis import ApiDaySummary, ApiTrades
from os import write

class DataIngestor(ABC):
    def __init__(self, writer, coins, default_date_from: datetime.date) -> None:
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

class IngestorTrades(DataIngestor):
    def ingest(self) -> None:
        for coin in self.coins:
            api = ApiTrades(coin = coin)
            data = api.get_data(day = self.default_date_from)
            self.writer(api = 'trades', coin = coin).write(data)