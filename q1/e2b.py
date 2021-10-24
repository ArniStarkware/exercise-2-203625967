def trace(f):
    def wrapper(*args,**kwargs):
        print('enter '+f.__name__+str(args))
        try:
            out = f(*args,**kwargs)
            print('leave '+f.__name__+str(args)+': '+str(out))
            return out
        except Exception as inst:
            print('leave '+f.__name__+str(args)+' on error: '+str(inst))
            raise(inst)
    return wrapper