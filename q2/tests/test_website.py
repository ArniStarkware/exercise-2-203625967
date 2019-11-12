import multiprocessing
import pathlib
import time

import pytest
import requests

import web
from website import Website


_ADDRESS = '127.0.0.1', 8000
_URL = f'http://{_ADDRESS[0]}:{_ADDRESS[1]}'
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_WEBSERVER_PATH = _ROOT / 'web.py'
_DATA_DIR = _ROOT / 'data'


@pytest.fixture
def website():
    process = multiprocessing.Process(target=run_website)
    process.start()
    time.sleep(1)
    try:
        yield website
    finally:
        process.kill()


def run_website():
    website = Website()
    @website.route('/')
    def index():
        return 200, 'users list'
    @website.route('/users/([0-9]+)')
    def user(user_id):
        if user_id not in ['1', '2']:
            return 404, ''
        return 200, f'user {user_id}'
    website.run(_ADDRESS)


def test_index(website):
    response = requests.get(_URL)
    assert response.status_code == 200
    assert response.text == 'users list'


def test_user(website):
    for user_id in [1, 2]:
        response = requests.get(f'{_URL}/users/{user_id}')
        assert response.status_code == 200
        assert response.text == f'user {user_id}'


def test_invalid_user(website):
    for user_id in [3, 4]:
        response = requests.get(f'{_URL}/users/{user_id}')
        assert response.status_code == 404
        assert response.text == f''


def test_invalid_path(website):
    response = requests.get(f'{_URL}/hello')
    assert response.status_code == 404
    assert response.text == ''


def test_web():
    process = multiprocessing.Process(target=run_webserver)
    process.start()
    time.sleep(1)
    try:
        response = requests.get(_URL)
        for user_dir in _DATA_DIR.iterdir():
            assert f'user {user_dir.name}' in response.text
        for user_dir in _DATA_DIR.iterdir():
            response = requests.get(f'{_URL}/users/{user_dir.name}')
            assert f'User {user_dir.name}' in response.text
            for thought_file in user_dir.iterdir():
                assert thought_file.read_text() in response.text
    finally:
        process.terminate()


def run_webserver():
    web.run_webserver(_ADDRESS, _DATA_DIR)
