import datetime

from mercado_bitcoin.apis import ApiDaySummary

class TestApiDatSummary:
    def test_get_data_all(self):
        actual = ApiDaySummary(coin = 'BTC').get_data(date = datetime.date(2021, 1, 31))
        expected = {'date': '2021-01-31', 'opening': 185398.9571, 'closing': 185649.97825, 'lowest': 178143.38597, 'highest': 186709.45702, 'volume': 23765954.28016561, 'quantity': 130.41570809, 'amount': 10118, 'avg_price': 182232.29876392}

        assert actual == expected

    def test_get_data_date(self):
        actual = ApiDaySummary(coin = 'BTC').get_data(date = datetime.date(2021, 1, 31)).get('date')
        expected = '2021-01-31'
        
        assert actual == expected 