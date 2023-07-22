import pytest
from controller import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_save_emails(client):
    data = {
        "event_id": 1,
        "email_subject": "Test Subject",
        "email_content": "Test Content",
        "timestamp": "2023-07-31 15:30:00"
    }

    response = client.post('/save_emails', json=data)
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'data' in response.json

def test_get_all_emails(client):
    response = client.get('/emails')
    assert response.status_code == 200
    assert 'emails' in response.json
    assert 'pagination' in response.json

def test_get_email_by_id(client):
    response = client.get('/emails/1')
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'event_id' in response.json
    assert 'email_subject' in response.json
    assert 'email_content' in response.json
    assert 'timestamp' in response.json

def test_delete_email(client):
    response = client.delete('/emails/1')
    assert response.status_code == 200
    assert 'message' in response.json
