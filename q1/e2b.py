import functools
def trace(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        call = f'{f.__name__}('
        if args:
            call += ', '.join(repr(arg) for arg in args)
        # These two lines are by me.
        if args and kwargs:
            call += ', '
        if kwargs:
            call += ', '.join(f'{key}={value!r}' for key, value in kwargs.items())
        call += ')'
        print(f'enter {call}')
        try:
            result = f(*args, **kwargs)
            print(f'leave {call}: {result!r}')
            return result
        except Exception as error:
            print(f'leave {call} on error: {error}')
            raise
    return wrapper
