# %%
import backoff
import random

# %%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries = 10)
def fake_api(*args, **kargs):
    rand = random.random()

    print(f"""
        Random number: {rand}
        args: {args if args else 'no args.'}
        kargs: {kargs if kargs else 'no kargs.'}
    """)

    if rand < .2:
        raise ConnectionAbortedError('Connection aborted.')
    if rand < .4:
        raise ConnectionRefusedError('Connection refused.')
    if rand < .6:
        raise TimeoutError('Timeout.')
    else:
        return "Success."

# %%
fake_api()

# %%
fake_api(1)

# %%
fake_api(2, number = 4)
