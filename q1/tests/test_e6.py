import threading
import time

from e6 import synchronize


lock = threading.Lock()


def test_synchronize():
    output = []
    @synchronize(lock)
    def f():
        time.sleep(1)
        output.append(1)
    t1 = threading.Thread(target=f)
    t2 = threading.Thread(target=f)
    t1.start()
    t2.start()
    assert len(output) == 0
    time.sleep(1.1)
    assert len(output) == 1
    time.sleep(1.1)
    assert len(output) == 2


def test_wraps():
    @synchronize(lock)
    def function():
        'Documentation.'
    assert function.__name__ == 'function'
    assert function.__doc__ == 'Documentation.'
