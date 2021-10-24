def cache(f):
    cache = {}
    def wrapper(*args):
        if args not in cache: #will Gittik not like this?
            cache[args] = f(*args)
        return cache[args]
    return wrapper