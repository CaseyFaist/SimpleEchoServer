from app import app
import pytest
from os import getenv


def test_no_key_ping():
    """Check that the root endpoint is live"""

    response = app.test_client().get('/')
    assert "server_key" not in response.headers
    assert response.status_code == 403
    assert response.data == "Please add server_key to access".encode("UTF_8")

def test_wrong_key_ping():
    """Check that the root endpoint is live"""

    response = app.test_client().get('/', headers=dict(server_key="bla"))
    assert response.status_code == 403
    assert response.data == "Incorrect server key".encode("UTF_8")

def test_correct_key_ping():
    """Check that the root endpoint is live"""

    SERVER_KEY = getenv('SERVER_KEY')
    response = app.test_client().get('/', headers=dict(server_key=SERVER_KEY))
    assert response.status_code == 200
    assert response.data != "Incorrect server key".encode("UTF_8")
    assert response.data == "Hello! I will echo whatever you send me!".encode("UTF_8")