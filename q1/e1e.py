import itertools
def permutations(alphabet, repeat):
    return {word[0]+word[1] for word in itertools.permutations(alphabet,r = repeat)}