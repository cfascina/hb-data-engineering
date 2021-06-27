#%%
import requests
import json

#%%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
r = requests.get(url)

#%%
if r:
    print(r)
else:
    print('Error')

#%%
usd = json.loads(r.text)['USDBRL']

# %%
print(f"20 USD: {float(usd['bid']) * 20} BRL")