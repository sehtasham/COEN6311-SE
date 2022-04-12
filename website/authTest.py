import os
import tempfile

import pytest

from flaskr import flaskr


@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_pass(client):
    rv = login(client, flaskr.app.config['email'], flaskr.app.config['password'])
    assert rv.status_code == 200

def test_login_fail_username(client):
    rv = login(client, flaskr.app.config['email'] + "x", flaskr.app.config['password'])
    assert rv.status_code != 200


def test_login_fail_username(client):
    rv = login(client, flaskr.app.config['email'] , flaskr.app.config['password'] + "x")
    assert rv.status_code != 200

def test_logout_pass(client):
    rv = logout(client)
    assert rv.status_code == 200
