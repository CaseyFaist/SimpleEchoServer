from app import app

def test_ping():
    """Check that the root endpoint is live"""

    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data == "Hello! I will echo whatever you send me!".encode("UTF_8")