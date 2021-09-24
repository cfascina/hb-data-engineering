import datetime
import time

from schedule import repeat, every, run_pending
from src.ingestors import IngestorDaySummaryAWS
from src.writers import S3DataWriter


if __name__ == "__main__":
    ingestor_day_summary = IngestorDaySummaryAWS(
        writer=S3DataWriter,
        coins=["BTC", "ETH"],
        default_date_from=datetime.date(2021, 6, 1),
    )

    @repeat(every(1).seconds)
    def job():
        ingestor_day_summary.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
