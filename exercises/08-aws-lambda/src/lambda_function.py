import datetime
import logging

from src.ingestors import IngestorDaySummaryAWS
from src.writers import S3DataWriter

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    logger.info(f"{event}")
    logger.info(f"{context}")

    IngestorDaySummaryAWS(
        writer=S3DataWriter,
        coins=["BTC", "ETH"],
        default_date_from=datetime.date(2021, 7, 1),
    ).ingest()
