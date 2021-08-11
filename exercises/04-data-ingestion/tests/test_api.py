# Run with:
# python -m pytest

import datetime
import pytest
import requests

from apis import ApiMercadoBitcoin, ApiDaySummary, ApiTrades
from unittest.mock import patch

@pytest.fixture()
@patch("apis.ApiMercadoBitcoin.__abstractmethods__", set())
def fixture_api_mercado_bitcoin():
    return ApiMercadoBitcoin(coin = 'ND')

def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, status_code, json_data):
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception

    if args[0] == 'Response success.':
        return MockResponse(status_code = 200, json_data = {"foo": "bar"})
    else:
        return MockResponse(status_code = 404, json_data = None)

class TestApiMercadoBitcoin:
    @patch("requests.get")
    @patch("apis.ApiMercadoBitcoin._get_endpoint", return_value = 'Request done.')
    def test_get_data_request(self, mock_get_endpoint, mock_requests, fixture_api_mercado_bitcoin):
        fixture_api_mercado_bitcoin.get_data()

        mock_requests.assert_called_once_with('Request done.')

    @patch("requests.get", side_effect = mocked_requests_get)
    @patch("apis.ApiMercadoBitcoin._get_endpoint", return_value = 'Response success.')
    def test_get_data_response_success(self, mock_get_endpoint, mock_requests, fixture_api_mercado_bitcoin):
        actual = fixture_api_mercado_bitcoin.get_data()
        expected = {"foo": "bar"}

        assert actual == expected

    @patch("requests.get", side_effect = mocked_requests_get)
    @patch("apis.ApiMercadoBitcoin._get_endpoint", return_value = 'Response failure.')
    def test_get_data_response_failure(self, mock_get_endpoint, mock_requests, fixture_api_mercado_bitcoin):
        with pytest.raises(Exception):
            fixture_api_mercado_bitcoin.get_data()

class TestApiDaySummary:
    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            ('BTC', datetime.date(2021, 6, 15), 'https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/15'),
            ('ETH', datetime.date(2021, 6, 15), 'https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/15'),
            ('ETH', datetime.date(2021, 6, 30), 'https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/30')
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = ApiDaySummary(coin = coin)
        actual = api._get_endpoint(date = date)
        
        assert actual == expected

class TestApiTrades:
    @pytest.mark.parametrize(
        "day, expected",
        [
            (datetime.datetime(2021, 1, 25), 1611543600),
            (datetime.datetime(2012, 12, 16), 1355623200),
            (datetime.datetime(2012, 12, 16, 0, 0, 5), 1355623205)
        ]
    )
    def test_get_date_unix(self, day, expected):
        actual = ApiTrades(coin = 'ND')._get_date_unix(day)
        assert actual == expected

    @pytest.mark.parametrize(
        "coin, day, expected",
        [
            ('ND', datetime.datetime(2021, 1, 25), 'https://www.mercadobitcoin.net/api/ND/trades/1611543600'),
            ('ND', datetime.datetime(2012, 12, 16), 'https://www.mercadobitcoin.net/api/ND/trades/1355623200'),
            ('ND', datetime.datetime(2012, 12, 16, 0, 0, 5), 'https://www.mercadobitcoin.net/api/ND/trades/1355623205')
        ]
    )
    def test_get_endpoint(self, coin, day, expected):
        actual = ApiTrades(coin = coin)._get_endpoint(day = day)
        assert actual == expected

    def test_get_endpoint_current_day(self):
        with pytest.raises(RuntimeError):
            ApiTrades(coin = 'ND')._get_endpoint(day = datetime.datetime.today().strftime('%Y-%m-%d'))

