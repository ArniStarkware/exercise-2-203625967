import functools

import time

def time_execution(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        start = time.time()
        try:
            out = f(*args,**kwargs)
            end = time.time()
            elapsed = end - start
            print(f"{f.__name__} took {elapsed:0.2f} seconds to execute")
            return out
        except:
            end = time.time()
            elapsed = end - start
            print(f"{f.__name__} took '{elapsed:0.2f}' seconds to execute")
            raise
    return wrapper