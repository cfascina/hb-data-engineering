# %%
import logging
import random

# %%
log = logging.getLogger()

# %%
log.setLevel(logging.DEBUG)

# %%
log_formatter = logging.Formatter(f'''
    %(asctime)s - %(name)s - %(levelname)s - %(message)s
''')

# %%
log_channel = logging.StreamHandler()

# %%
log_channel.setFormatter(log_formatter)

# %%
log.addHandler(log_channel)

# %%
def fake_api(*args):
    rand = random.random()
    log.debug(f'Random number: {rand}')
    log.info(f'Args: {args}')

    if rand < .2:
        log.error('Connection aborted.')
    if rand < .4:
        log.error('Connection refused.')
    if rand < .6:
        log.error('Timeout.')
    else:
        return "Success."

# %%
fake_api(1)
