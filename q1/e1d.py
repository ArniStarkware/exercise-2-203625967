import itertools
def product(alphabet, repeat):
    if repeat == 0:
        return set()
    elif repeat == 1:
        return {str(l) for l in set(alphabet)}
    else:
        recursive_prod = product(alphabet,repeat -1)
        output = set()
        for letter in set(alphabet):
            letter_output = {word + letter for word in recursive_prod}
            output = output.union(letter_output)
        return output