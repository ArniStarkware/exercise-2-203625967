def cache(max_size):
    def decorator(f):
        cache = {}
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

@cache(max_size = 4)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)