from app import app
from os import environ

SERVER_KEY=environ.get("SERVER_KEY")

def test_echo():
    """Test the echo function"""

    test_string = "A string to test that our endpoint echos"
    response = app.test_client().post('/', 
                                        headers=dict(server_key=SERVER_KEY), 
                                        data=test_string)

    assert response.status_code == 200
    assert response.data == test_string.encode('utf-8')