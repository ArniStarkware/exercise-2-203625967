import inspect

def exception_safe(*args):
    if args and inspect.isfunction(args[0]):
        def wrapper(*wargs,**wkwargs):
            try:
                out = args[0](*wargs,**wkwargs)
                return out
            except:
                return
        return wrapper
    else:
        def decorator(f):
            def wrapper(*wargs,**wkwargs):
                try:
                    out = f(*wargs,**wkwargs)
                    return out
                except Exception as inst:
                    if inst.__class__ in args:
                        return
                    else:
                        raise inst
            return wrapper
        return decorator
        