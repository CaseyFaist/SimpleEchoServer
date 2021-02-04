from app import app

def test_echo():
    """Test the echo function"""

    test_string = "A string to test that our endpoint echos"
    response = app.test_client().post('/', data=test_string)

    assert response.status_code == 200
    assert response.data == test_string.encode('utf-8')