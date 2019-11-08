import inspect
import itertools
import os

import pytest

from e1a import file_sizes
from e1b import sieve_of_eratosthenes
from e1c import is_prime
from e1d import product
from e1e import permutations
from e1f import combinations
from e1g import combinations_with_replacement


_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
_ALPHABET = 'ABCD'

optional = pytest.mark.xfail(reason='optional')


def test_e1a(tmp_path):
    old_path = os.getcwd()
    try:
        os.chdir(tmp_path)
        (tmp_path / 'file.txt').write_text('Hello, world!')
        (tmp_path / 'directory').mkdir()
        assert file_sizes() == {'file.txt': 13}
    finally:
        os.chdir(old_path)


def test_e1a_one_liner():
    _test_one_liner(file_sizes)


def test_e1b():
    assert sieve_of_eratosthenes(100) == _PRIMES


def test_e1b_one_liner():
    _test_one_liner(sieve_of_eratosthenes)


def test_e1c():
    for n in range(100):
        if n in _PRIMES:
            assert is_prime(n)
        else:
            assert not is_prime(n)


def test_e1c_one_liner():
    _test_one_liner(is_prime)


@optional
def test_e1d():
    for repeat in range(1, 5):
        assert {''.join(x) for x in itertools.product(_ALPHABET, repeat=repeat)} == product(_ALPHABET, repeat)


@optional
def test_e1d_one_liner():
    _test_one_liner(product)


@optional
def test_e1e():
    for repeat in range(1, 5):
        assert {''.join(x) for x in itertools.permutations(_ALPHABET, repeat)} == permutations(_ALPHABET, repeat)


@optional
def test_e1e_one_liner():
    _test_one_liner(permutations)


@optional
def test_e1f():
    for repeat in range(1, 5):
        assert {''.join(x) for x in itertools.combinations(_ALPHABET, repeat)} == combinations(_ALPHABET, repeat)


@optional
def test_e1f_one_liner():
    _test_one_liner(combinations)


@optional
def test_e1g():
    for repeat in range(1, 5):
        assert {''.join(x) for x in itertools.combinations_with_replacement(_ALPHABET, repeat)} == combinations_with_replacement(_ALPHABET, repeat)


@optional
def test_e1g_one_liner():
    _test_one_liner(combinations_with_replacement)


def _test_one_liner(f):
    lines = [line.strip() for line in inspect.getsource(f).splitlines() if not line.startswith('def')]
    assert len(lines) == 1
    line = lines[0]
    assert line.startswith('return')
    assert eval(line.replace('return', 'lambda: '))
