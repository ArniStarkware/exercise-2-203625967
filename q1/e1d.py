import itertools
def product(alphabet, repeat):
    return {word[0]+word[1] for word in itertools.product(alphabet,repeat = repeat)}