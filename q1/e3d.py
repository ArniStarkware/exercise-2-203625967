import functools
def cache(f=None, *, max_size=None):
    if f is None:
        return lambda f: cache(f, max_size= max_size)
    dic = {}
    @functools.wraps(f)
    def wrapper(*args):
        if args not in dic:
            out = f(*args)
            if len(dic) == max_size:
                del dic[list(dic.keys())[0]]
            dic[args] = out
        return dic[args]
    wrapper.cache = dic
    return wrapper
    