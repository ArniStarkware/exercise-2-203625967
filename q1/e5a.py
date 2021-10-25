import functools

def exception_safe(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        try:
            out = f(*args,**kwargs)
            return out
        except:
            return
    return wrapper
