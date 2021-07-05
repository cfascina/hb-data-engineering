# %%
import logging
import pandas as pd
import requests

from bs4 import BeautifulSoup as bs

# %%
log = logging.getLogger()
log_channel = logging.StreamHandler()
log_formatter = logging.Formatter(f'''
    %(asctime)s - %(name)s - %(levelname)s - %(message)s
''')

# %%
log.setLevel(logging.DEBUG)

# %%
log_channel.setFormatter(log_formatter)

# %%
log.addHandler(log_channel)

# %%
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

# %%
def get_podcasts(url):
    r = requests.get(url)
    soup = bs(r.text, features = 'html.parser')

    return soup.find_all('h5')

# %%
block = 1
lst_podcasts = []

# %%
while True:
    podcast_block = get_podcasts(url.format(block))
    log.debug(f'Collecting block {block} ({len(podcast_block)} episodes)...')

    if len(podcast_block) > 0:
        lst_podcasts = lst_podcasts + podcast_block
        block += 1
    else:
        break

# %%
len(lst_podcasts)

# %%
df = pd.DataFrame(columns = ['nome', 'link'])

# %%
for item in lst_podcasts:
    df.loc[df.shape[0]] = [item.text, item.a['href']]

# %%
df.to_csv('podcasts.csv', sep = ';', index = False)
