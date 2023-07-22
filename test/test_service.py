import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.email import save, get_by_id, get_all
from database.models import Email, EmailRecipient
from database import session as db

def test_save_email():
    data = {
        "event_id": 123,
        "email_subject": "Test Subject",
        "email_content": "Test Content",
        "timestamp": "2023-07-31 15:30:00",
        "recipients": ["recipient1@example.com", "recipient2@example.com"]
    }

    email = save(data)

    assert email['event_id'] == data['event_id']
    assert email['email_subject'] == data['email_subject']
    assert email['email_content'] == data['email_content']
    assert email['recipients'][0]['recipient_email'] == data['recipients'][0]
    assert email['recipients'][1]['recipient_email'] == data['recipients'][1]

    # Clean up
    for recipient in email['recipients']:
        recipient_id = recipient['id']
        recipient_obj = db.query(EmailRecipient).get(recipient_id)
        db.delete(recipient_obj)
        db.commit()

    email_id = email['id']
    email_obj = db.query(Email).get(email_id)
    db.delete(email_obj)
    db.commit()

def test_get_by_id_email():
    data = {
        "event_id": 123,
        "email_subject": "Test Subject",
        "email_content": "Test Content",
        "timestamp": "2023-07-31 15:30:00",
        "recipients": ["recipient1@example.com", "recipient2@example.com"]
    }

    email = save(data)
    email_id = email['id']

    retrieved_email = get_by_id(email_id)

    assert retrieved_email['id'] == email_id
    assert retrieved_email['event_id'] == data['event_id']
    assert retrieved_email['email_subject'] == data['email_subject']
    assert retrieved_email['email_content'] == data['email_content']
    assert retrieved_email['recipients'][0]['recipient_email'] == data['recipients'][0]
    assert retrieved_email['recipients'][1]['recipient_email'] == data['recipients'][1]

    # Clean up
    for recipient in retrieved_email['recipients']:
        recipient_id = recipient['id']
        recipient_obj = db.query(EmailRecipient).get(recipient_id)
        db.delete(recipient_obj)
        db.commit()

    email_obj = db.query(Email).get(email_id)
    db.delete(email_obj)
    db.commit()

def test_get_all_emails():
    data1 = {
        "event_id": 123,
        "email_subject": "Test Subject 1",
        "email_content": "Test Content 1",
        "timestamp": "2023-07-31 15:30:00",
        "recipients": ["recipient1@example.com", "recipient2@example.com"]
    }

    data2 = {
        "event_id": 456,
        "email_subject": "Test Subject 2",
        "email_content": "Test Content 2",
        "timestamp": "2023-07-31 16:30:00",
        "recipients": ["recipient3@example.com", "recipient4@example.com"]
    }

    email1 = save(data1)
    email2 = save(data2)

    emails = get_all(page=1, size=10)

    assert len(emails['data']) >= 2
    assert emails['pagination']['total_data'] >= 2

    # Clean up
    for recipient in email1['recipients']:
        recipient_id = recipient['id']
        recipient_obj = db.query(EmailRecipient).get(recipient_id)
        db.delete(recipient_obj)
        db.commit()

    email_id1 = email1['id']
    email_obj1 = db.query(Email).get(email_id1)
    db.delete(email_obj1)

    for recipient in email2['recipients']:
        recipient_id = recipient['id']
        recipient_obj = db.query(EmailRecipient).get(recipient_id)
        db.delete(recipient_obj)
        db.commit()

    email_id2 = email2['id']
    email_obj2 = db.query(Email).get(email_id2)
    db.delete(email_obj2)

    db.commit()

if __name__ == '__main__':
    pytest.main()
