import functools
def cache(max_size):
    def decorator(f):
        cache = {}
        @functools.wraps(f)
        def wrapper(*args):
            if args not in cache:
                out = f(*args)
                if len(cache) == max_size:
                    del cache[list(cache.keys())[0]]
                cache[args] = out
            return cache[args]
        wrapper.cache = cache
        return wrapper
    return decorator