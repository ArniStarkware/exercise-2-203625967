def trace(f):
    def wrapper(*args,**kwargs):
        print('enter '+f.__name__)
        out = f(*args,**kwargs)
        print('leave '+f.__name__)
        return out
    return wrapper