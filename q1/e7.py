import functools

import inspect

def validate_types(**types):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            callargs = inspect.getcallargs(f, *args, **kwargs)
            for key,value in callargs.items():
                if not type(value) == types[key]:
                    raise ValueError
            out = f(*args,**kwargs)
            if not type(out) == types['return_value']:
                raise ValueError
            return out
        return wrapper
    return decorator
