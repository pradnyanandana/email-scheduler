from service.email import save, get_all, get_by_id, delete
from datetime import datetime, timezone

def test_save_email():
    data = {
        "event_id": 1,
        "email_subject": "Test Subject",
        "email_content": "Test Content",
        "timestamp": "2023-07-31 15:30:00"
    }

    email = save(data)
    assert email is not None
    assert email.event_id == 1
    assert email.email_subject == "Test Subject"
    assert email.email_content == "Test Content"
    assert email.timestamp == datetime(2023, 7, 31, 15, 30, tzinfo=timezone.utc)

def test_get_all_emails():
    emails = get_all(1, 10)
    assert 'emails' in emails
    assert 'pagination' in emails

def test_get_email_by_id():
    email = get_by_id(1)
    assert email is not None
    assert email['id'] == 1

def test_delete_email():
    assert delete(1) is True
