def is_prime(p):
    if p < 2:
        return False
    for i in range(2,p):
        if p % i == 0:
            return False
    return True