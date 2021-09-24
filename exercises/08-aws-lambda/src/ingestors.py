import datetime

from abc import abstractmethod
from apis import ApiDaySummary
from checkpoints import CheckpointModel, DynamoCheckpoints


class DataIngestorAWS:
    def __init__(self, writer, coins, default_date_from: datetime.date) -> None:
        self.dynamo_checkpoint = DynamoCheckpoints(
            model=CheckpointModel,
            report_id=self.__class__.__name__,
            default_start_date=default_date_from,
        )
        self.writer = writer
        self.coins = coins
        self.default_date_from = default_date_from
        self._checkpoint = self._load_checkpoint()

    def _load_checkpoint(self) -> datetime.date:
        return self.dynamo_checkpoint.get_checkpoint()

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self.dynamo_checkpoint.create_or_update_checkpoint(date=self._checkpoint)

    @abstractmethod
    def ingest(self) -> None:
        pass


class IngestorDaySummaryAWS(DataIngestorAWS):
    def ingest(self) -> None:
        date = self._load_checkpoint()

        if date < datetime.date.today():
            for coin in self.coins:
                api = ApiDaySummary(coin=coin)
                data = api.get_data(date=date)
                self.writer(api="day-summary", coin=coin).write(data)

            self._update_checkpoint(date + datetime.timedelta(days=1))
