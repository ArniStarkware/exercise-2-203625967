def is_prime(p):
    return (p>=2) and all(p %i !=0 for i in range(2,p))
