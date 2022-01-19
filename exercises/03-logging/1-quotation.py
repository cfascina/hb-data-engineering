# %%
import json
import requests

# %%
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

# %%
@error_check
def get_quotation(value, currency):
    url = f'https://economia.awesomeapi.com.br/last/{currency}'
    r = requests.get(url)
    quotation = json.loads(r.text)[currency.replace('-', '')]

    print(f"{value} {currency[:3]}: {float(quotation['bid']) * value} {currency[-3:]}")

# %%
get_quotation(20, 'USD-BRL')
get_quotation(20, 'EUR-BRL')
get_quotation(20, 'BTC-BRL')
get_quotation(20, 'RPL-BRL')
get_quotation(20, 'JPY-BRL')
