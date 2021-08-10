# Run with:
# python -m pytest

import datetime
from os import read
from unittest import mock
import pytest

from ingestors import DataIngestor
from unittest.mock import mock_open, patch
from writers import DataWriter

@patch("ingestors.DataIngestor.__abstractmethods__", set())
class TestDataIngestor:
    def test_checkpoint_filename(self):
        actual = DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date(2020, 12, 31)
        )._checkpoint_filename

        expected = "DataIngestor.checkpoint"
        
        assert actual == expected

    @patch("builtins.open", new_callable = mock_open, read_data = '1990-11-14')
    @patch("ingestors.DataIngestor._checkpoint_filename", return_value = 'foo.checkpoint')
    def test_save_checkpoint(self, mock_file, mock_with_open):
        data_ingestor = DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date.today()
        )
        data_ingestor._save_checkpoint()

        mock_with_open.assert_called_with(mock_file, 'w')

    @patch("builtins.open", new_callable = mock_open, read_data = '2021-07-26')
    def test_load_checkpoint_existent(self, mock):
        actual = DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date(2020, 12, 31)
        )._load_checkpoint()
        
        expected = datetime.date(2021, 7, 26)

        assert actual == expected

    def test_load_checkpoint_nonexistent(self):
        actual = DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date(2020, 12, 31)
        )._load_checkpoint()

        expected = None

        assert actual == expected

    @patch("ingestors.DataIngestor._save_checkpoint", return_value = None)
    def test_update_checkpoint_by_value(self, mock):
        data_ingestor = DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date(2020, 12, 31)
        )
        data_ingestor._update_checkpoint(datetime.date(2020, 12, 31))

        actual = data_ingestor._checkpoint
        expected = datetime.date(2020, 12, 31)

        assert actual == expected
    
    @patch("ingestors.DataIngestor._save_checkpoint", return_value = None)
    def test_update_checkpoint_by_method(self, mock):
        data_ingestor = DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date.today()
        )
        data_ingestor._update_checkpoint('')

        mock.assert_called_once()