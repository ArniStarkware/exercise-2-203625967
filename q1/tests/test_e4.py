import re
import time

from e4 import time_execution


_regex = re.compile('(.*?) took (.*?) seconds to execute')


def test_output(capsys):
    @time_execution
    def wait(n):
        time.sleep(1)
    for n in [1, 2]:
        started = time.time()
        wait(1)
        elapsed = time.time() - started
        out, err = capsys.readouterr()
        match = _regex.match(out)
        assert match
        name, seconds = match.groups()
        assert name == wait.__name__
        assert abs(float(seconds) - elapsed) < 0.2


def test_wraps():
    @time_execution
    def function():
        'Documentation.'
    assert function.__name__ == 'function'
    assert function.__doc__ == 'Documentation.'
