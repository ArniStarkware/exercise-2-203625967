from e1c import is_prime


def sieve_of_eratosthenes(n):
    return {x for x in range(1,n) if is_prime(x)}

print(sieve_of_eratosthenes(100))