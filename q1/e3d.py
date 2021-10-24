def cache(f=None, *, max_size=None):
    if f is None:
        return lambda f: cache(f, max_size= max_size)
    dic = {}
    def wrapper(*args):
        if args not in dic:
            out = f(*args)
            if len(dic) == max_size:
                del dic[list(dic.keys())[0]]
            dic[args] = out
        return dic[args]
    wrapper.cache = dic
    return wrapper
    
@cache(max_size = 4)
def fir(n):
    return n if n < 2 else fir(n-1) + fir(n-2)
@cache
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
