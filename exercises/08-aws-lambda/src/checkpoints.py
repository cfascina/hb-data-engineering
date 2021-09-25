from datetime import datetime
import logging

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class CheckpointModel(Model):
    class Meta:
        table_name = "mercado_bitcoin_checkpoint"
        region = "us-east-1"

    report_id = UnicodeAttribute(hash_key=True)
    checkpoint_date = UnicodeAttribute()


class DynamoCheckpoints:
    def __init__(self, model, report_id, default_start_date):
        self.model = model
        self.default_start_date = default_start_date
        self.report_id = report_id
        self.create_table()

    def get_checkpoint(self):
        if self.has_checkpoint:
            checkpoint = list(self.model.query(self.report_id))[0].checkpoint_date
            logger.info(f"Checkpoint found for {self.report_id}: {checkpoint}")
            return datetime.strptime(checkpoint, "%Y-%m-%d").date()
        else:
            logger.info(
                f"Checkpoint not found for {self.report_id} using default_start_date."
            )
            return self.default_start_date

    def create_checkpoint(self, date):
        checkpoint = self.model(self.report_id, checkpoint_date=f"{date}")
        checkpoint.save()

    def update_checkpoint(self, date):
        checkpoint = self.model.get(self.report_id)
        checkpoint.date = f"{date}"
        checkpoint.save()

    @property
    def has_checkpoint(self):
        try:
            return list(self.model.query(self.report_id)) != []
        except KeyError:
            logger.warning(f"KeyError: {self.report_id}")
            return False

    def create_or_update_checkpoint(self, date):
        logger.info(f"Saving checkpoint for {self.report_id}: {date}")

        if not self.has_checkpoint:
            self.create_checkpoint(date)
        else:
            self.update_checkpoint(date)

    def create_table(self):
        logger.info("Creating Dynamo table...")

        if not self.model.exists():
            self.model.create_table(billing_mode="PAY_PER_REQUEST", wait=True)
