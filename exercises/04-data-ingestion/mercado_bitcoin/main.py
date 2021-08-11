import datetime
import time

from schedule import repeat, every, run_pending
from ingestors import IngestorDaySummary, IngestorTrades
from writers import DataWriter


if __name__ == '__main__':
    ingestor_day_summary = IngestorDaySummary(
        writer = DataWriter, 
        coins = ['BTC', 'ETH'], 
        default_date_from = datetime.date(2021, 7, 1)
    )

    ingestor_trades = IngestorTrades(
        writer = DataWriter, 
        coins = ['BCH', 'XRP'],
        default_date_from = datetime.datetime(2021, 7, 15)
    )

    @repeat(every(1).seconds)
    def job():
        # ingestor_day_summary.ingest()
        ingestor_trades.ingest()

    while True:
        run_pending()
        time.sleep(.5)