# Run with:
# python -m pytest

import datetime
from os import read
import pytest
from unittest import mock

from mercado_bitcoin.ingestors import DataIngestor
from mercado_bitcoin.writers import DataWriter
from unittest.mock import mock_open, patch

@pytest.fixture
@patch("mercado_bitcoin.ingestors.DataIngestor.__abstractmethods__", set())
def fixture_data_ingestor():
    return (
        DataIngestor(
            writer = DataWriter,
            coins = ['A', 'B', 'C'],
            default_date_from = datetime.date.today()
        )
    )

class TestDataIngestor:
    def test_checkpoint_filename(self, fixture_data_ingestor):
        actual = fixture_data_ingestor._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        
        assert actual == expected

    @patch("builtins.open", new_callable = mock_open, read_data = '1990-11-14')
    @patch("mercado_bitcoin.ingestors.DataIngestor._checkpoint_filename", return_value = 'foo.checkpoint')
    def test_save_checkpoint(self, mock_file, mock_with_open, fixture_data_ingestor):
        fixture_data_ingestor._save_checkpoint()
        mock_with_open.assert_called_with(mock_file, 'w')

    @patch("builtins.open", new_callable = mock_open, read_data = '1990-11-14')
    def test_load_checkpoint_existent(self, mock, fixture_data_ingestor):
        actual = fixture_data_ingestor._load_checkpoint() 
        expected = datetime.date(1990, 11, 14)

        assert actual == expected

    def test_load_checkpoint_nonexistent(self, fixture_data_ingestor):
        actual = fixture_data_ingestor._load_checkpoint()
        expected = None

        assert actual == expected

    @patch("mercado_bitcoin.ingestors.DataIngestor._save_checkpoint", return_value = None)
    def test_update_checkpoint_by_value(self, mock, fixture_data_ingestor):
        fixture_data_ingestor._update_checkpoint(datetime.date(1990, 11, 14))
        actual = fixture_data_ingestor._checkpoint
        expected = datetime.date(1990, 11, 14)

        assert actual == expected
    
    @patch("mercado_bitcoin.ingestors.DataIngestor._save_checkpoint", return_value = None)
    def test_update_checkpoint_by_method(self, mock, fixture_data_ingestor):
        fixture_data_ingestor._update_checkpoint('')
        mock.assert_called_once()
