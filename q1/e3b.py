import functools
def cache(f):
    cache = {}
    @functools.wraps(f)
    def wrapper(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    wrapper.cache = cache
    return wrapper