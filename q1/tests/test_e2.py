import pytest

import e2a
import e2b
import e2c
import e2d
import e2e


_INC_OUTPUT = '''\
enter inc
leave inc
'''

_DIV_OUTPUT = '''\
enter div(4, 2)
leave div(4, 2): 2.0
'''

_DIV_OUTPUT_ERROR = '''\
enter div(x=1, y=0)
leave div(x=1, y=0) on error: division by zero
'''

_FIB_OUTPUT = '''\
enter fib(3)
 enter fib(2)
  enter fib(1)
  leave fib(1): 1
  enter fib(0)
  leave fib(0): 0
 leave fib(2): 1
 enter fib(1)
 leave fib(1): 1
leave fib(3): 2
'''


def test_e2a(capsys):
    @e2a.trace
    def inc(x):
        return x + 1
    assert inc(1) == 2
    out, err = capsys.readouterr()
    assert out == _INC_OUTPUT


def test_e2a_wraps():
    _test_wraps(e2a.trace)


def test_e2b(capsys):
    @e2b.trace
    def div(x, y):
        return x / y
    assert div(4, 2) == 2.0
    out, err = capsys.readouterr()
    assert out == _DIV_OUTPUT


def test_e2b_error(capsys):
    @e2b.trace
    def div(x, y):
        return x / y
    with pytest.raises(ZeroDivisionError):
        div(x=1, y=0)
    out, err = capsys.readouterr()
    assert out == _DIV_OUTPUT_ERROR


def test_e2b_wraps():
    _test_wraps(e2b.trace)


def test_e2c(capsys):
    @e2c.trace
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(3) == 2
    out, err = capsys.readouterr()
    assert out == _FIB_OUTPUT


def test_e2c_wraps():
    _test_wraps(e2c.trace)


def test_e2d_print(capsys):
    @e2d.trace(print)
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(3) == 2
    out, err = capsys.readouterr()
    assert out == _FIB_OUTPUT


def test_e2d_write(tmp_path):
    path = tmp_path / 'log.txt'
    def write(line):
        with path.open('a') as fp:
            fp.write(line + '\n')
    @e2d.trace(write)
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(3) == 2
    assert path.read_text() == _FIB_OUTPUT


def test_e2d_wraps():
    _test_wraps(e2d.trace(None))


def test_e2e(capsys):
    @e2e.trace
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(3) == 2
    out, err = capsys.readouterr()
    assert out == _FIB_OUTPUT


def test_e2e_print(capsys):
    @e2e.trace(log=print)
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(3) == 2
    out, err = capsys.readouterr()
    assert out == _FIB_OUTPUT


def test_e2e_write(tmp_path):
    path = tmp_path / 'log.txt'
    def write(line):
        with path.open('a') as fp:
            fp.write(line + '\n')
    @e2e.trace(log=write)
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(3) == 2
    assert path.read_text() == _FIB_OUTPUT


def test_e2e_wraps():
    _test_wraps(e2e.trace)
    _test_wraps(e2e.trace(log=print))


def _test_wraps(trace):
    @trace
    def function():
        'Documentation.'
    assert function.__name__ == 'function'
    assert function.__doc__ == 'Documentation.'
