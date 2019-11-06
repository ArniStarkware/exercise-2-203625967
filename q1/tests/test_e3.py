import e3a
import e3b
import e3c
import e3d


def test_e3a(capsys):
    _test_cached(capsys, e3a.cache)


def test_e3a_wraps():
    _test_wraps(e3a.cache)


def test_e3b(capsys):
    _test_cached(capsys, e3b.cache)


def test_e3b_cache():
    @e3b.cache
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib.cache == {}
    assert fib(3) == 2
    assert fib.cache == {(0,): 0, (1,): 1, (2,): 1, (3,): 2}
    assert fib(5) == 5
    assert fib.cache == {(0,): 0, (1,): 1, (2,): 1, (3,): 2, (4,): 3, (5,): 5}


def test_e3b_wraps():
    _test_wraps(e3b.cache)


def test_e3c(capsys):
    _test_cached(capsys, e3c.cache(128))


def test_e3c_max_size():
    @e3c.cache(3)
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib.cache == {}
    assert fib(2) == 1
    assert fib.cache == {(0,): 0, (1,): 1, (2,): 1}
    assert fib(5) == 5
    assert fib.cache == {(3,): 2, (4,): 3, (5,): 5}


def test_e3c_wraps():
    _test_wraps(e3c.cache(None))


def test_e3d(capsys):
    _test_cached(capsys, e3d.cache)


def test_e3d_max_size():
    @e3d.cache(max_size=3)
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib.cache == {}
    assert fib(2) == 1
    assert fib.cache == {(0,): 0, (1,): 1, (2,): 1}
    assert fib(5) == 5
    assert fib.cache == {(3,): 2, (4,): 3, (5,): 5}


def test_e3d_no_max_size():
    @e3d.cache
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib.cache == {}
    assert fib(3) == 2
    assert fib.cache == {(0,): 0, (1,): 1, (2,): 1, (3,): 2}
    assert fib(5) == 5
    assert fib.cache == {(0,): 0, (1,): 1, (2,): 1, (3,): 2, (4,): 3, (5,): 5}


def test_e3d_wraps():
    _test_wraps(e3d.cache)
    _test_wraps(e3d.cache(max_size=128))


def _test_cached(capsys, cache):
    @cache
    def fib(n):
        print(f'computing fib({n})...')
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(10) == 55
    out, err = capsys.readouterr()
    for n in range(10):
        assert out.count(f'computing fib({n})') == 1


def _test_wraps(cache):
    @cache
    def function():
        'Documentation.'
    assert function.__name__ == 'function'
    assert function.__doc__ == 'Documentation.'
