import pytest

from e7 import validate_types


def test_type_validation():
    @validate_types(x=int, y=int, return_value=int)
    def add(x, y):
        return x + y
    assert add(1, 2) == 3
    with pytest.raises(ValueError):
        add('foo', 'bar')


def test_wraps():
    @validate_types()
    def function():
        'Documentation.'
    assert function.__name__ == 'function'
    assert function.__doc__ == 'Documentation.'
