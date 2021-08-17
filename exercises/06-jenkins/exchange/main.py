import json
import requests
import time

from datetime import datetime

def get_exchange(value):
    url = 'https://economia.awesomeapi.com.br/last/USD-BRL'
    r = requests.get(url)
    quotation = json.loads(r.text)['USDBRL']

    return float(quotation['bid']) * value

exchange = get_exchange(1)
time.sleep(5)
print(exchange)

with open('exchange.csv', 'a') as f:
    f.write("{};{}\n".format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), exchange))
