import pytest

import e5a
import e5b


def test_e5a():
    @e5a.exception_safe
    def f(error):
        raise error()
    for error in [NameError, TypeError, ValueError, Exception]:
        f(error)


def test_e5a_wraps():
    _test_wraps(e5a.exception_safe)


def test_e5b():
    @e5b.exception_safe(NameError, TypeError)
    def f(error):
        raise error()
    f(NameError)
    f(TypeError)
    with pytest.raises(ValueError):
        f(ValueError)
    with pytest.raises(Exception):
        f(Exception)


def test_e5b_all():
    @e5b.exception_safe
    def f(error):
        raise error()
    for error in [NameError, TypeError, ValueError, Exception]:
        f(error)


def test_e5b_wraps():
    _test_wraps(e5b.exception_safe)
    _test_wraps(e5b.exception_safe(NameError, TypeError))


def _test_wraps(exception_safe):
    @exception_safe
    def function():
        'Documentation.'
    assert function.__name__ == 'function'
    assert function.__doc__ == 'Documentation.'
