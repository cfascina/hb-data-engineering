# Run with:
# python -m pytest

import datetime
import pytest

from apis import ApiDaySummary, ApiTrades

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

