import contextlib
import multiprocessing
import pathlib
import signal
import socket
import subprocess
import sys
import threading
import time

import pytest

from cli import CommandLineInterface


_SERVER_ADDRESS = '127.0.0.1', 5000
_SERVER_BACKLOG = 1000
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_SERVER_PATH = _ROOT / 'server.py'
_CLIENT_PATH = _ROOT / 'client.py'


@pytest.fixture
def cli():
    cli = CommandLineInterface()
    @cli.command
    def inc(x):
        return x + 1
    @cli.command
    def add(x, y):
        return x + y
    return cli


def test_inc(cli, capsys):
    with _argv('inc', 'x=1') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert out == '2\n'
        assert command.exit_code == 0
    with _argv('inc', 'x=2') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert out == '3\n'
        assert command.exit_code == 0


def test_add(cli, capsys):
    with _argv('add', 'x=1', 'y=2') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert out == '3\n'
        assert command.exit_code == 0
    with _argv('inc', 'x=2', 'y=3') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert out == '5\n'
        assert command.exit_code == 0


def test_no_command(cli, capsys):
    with _argv() as command:
        cli.main()
        out, err = capsys.readouterr()
        assert 'usage' in out.lower()
        assert command.exit_code != 0


def test_invalid_command(cli, capsys):
    with _argv('foo') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert 'usage' in out.lower()
        assert command.exit_code != 0


def test_invalid_argument_format(cli, capsys):
    with _argv('inc', '1') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert 'usage' in out.lower()
        assert command.exit_code != 0


def test_invalid_arguments(cli, capsys):
    with _argv('inc', 'y=1') as command:
        cli.main()
        out, err = capsys.readouterr()
        assert 'usage' in out.lower()
        assert command.exit_code != 0


def test_client():
    def run_server():
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(_SERVER_ADDRESS)
        server.listen(_SERVER_BACKLOG)
        try:
            while True:
                connection, address = server.accept()
                connection.close()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
    server = multiprocessing.Process(target=run_server)
    server.start()
    try:
        time.sleep(0.1)
        host, port = _SERVER_ADDRESS
        process = subprocess.Popen(
            ['python', _CLIENT_PATH, f'{host}:{port}', '1', "I'm hungry"],
            stdout = subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        assert b'usage' in stdout.lower()
        process = subprocess.Popen(
            ['python', _CLIENT_PATH, 'upload', f'address={host}:{port}', f'user=1', f"thought=I'm hungry"],
            stdout = subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        assert b'done' in stdout.lower()
    finally:
        server.terminate()


def test_server():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', _SERVER_PATH, f'{host}:{port}', 'data/'],
        stdout = subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert b'usage' in stdout.lower()
    process = subprocess.Popen(
        ['python', _SERVER_PATH, 'run', f'address={host}:{port}', 'data=data/'],
        stdout = subprocess.PIPE,
    )
    stdout = None
    def run_server():
        nonlocal stdout
        stdout, _ = process.communicate()
    thread = threading.Thread(target=run_server)
    thread.start()
    time.sleep(0.1)
    try:
        connection = socket.socket()
        connection.connect(_SERVER_ADDRESS)
        connection.close()
    finally:
        process.send_signal(signal.SIGINT)
        thread.join()


@contextlib.contextmanager
def _argv(*args):
    command = lambda: None
    try:
        argv = sys.argv[1:]
        sys.argv[1:] = args
        yield command
    except SystemExit as e:
        command.exit_code = e.args[0]
    finally:
        sys.argv[1:] = argv