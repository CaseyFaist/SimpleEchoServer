from app import app

def test_ping():
    """Check that the root endpoint is live"""

    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data == b"Hello! I'll echo what you send me!"