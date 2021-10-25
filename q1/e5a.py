def exception_safe(f):
    def wrapper(*args,**kwargs):
        try:
            out = f(*args,**kwargs)
            return out
        except:
            return
    return wrapper
