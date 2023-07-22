import os
import pytz
import math

from flask import abort
from dotenv import load_dotenv
from database.models import Email, EmailRecipient
from database import session as db
from datetime import datetime
from database.celeryconfig import celery

load_dotenv()

def convert_tz(dt):
    timezone = pytz.timezone(os.environ.get('TIMEZONE'))
    return timezone.localize(dt)

@celery.task
def send(event_id, email_subject, email_content, recipients):
    # Send Email
    for recipient in recipients:
        print(f"Send to email: {recipient['recipient_email']}, Event ID {event_id}, Subject: {email_subject}, Content: {email_content}, Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def save(data):
    event_id = data['event_id']
    email_subject = data['email_subject']
    email_content = data['email_content']
    email_recipients = data['recipients']
    timestamp_str = data['timestamp']
    
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        abort(400, 'Invalid timestamp format')

    recipients = []
    email = Email(event_id=event_id,
                  email_subject=email_subject,
                  email_content=email_content,
                  timestamp=convert_tz(timestamp))

    db.add(email)
    db.commit()

    for recipient_email in email_recipients:
        recipient = EmailRecipient(email_id=email.id, recipient_email=recipient_email)
        db.add(recipient)
        db.commit()
        recipients.append({
            'id': recipient.id,
            'email_id': recipient.email_id,
            'recipient_email': recipient.recipient_email,
        })

    send.apply_async(args=[event_id, email_subject, email_content, recipients], eta=convert_tz(timestamp))

    return {
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'recipients': recipients
    }

def get_all(page, size):
    total_emails = db.query(Email).count()
    total_pages = math.ceil(total_emails / size)

    offset = (page - 1) * size
    
    email_list = []
    emails = db.query(Email).limit(size).offset(offset).all()

    for email in emails:
        recipients = []

        for recipient in email.recipients:
            recipients.append({
                'id': recipient.id,
                'email_id': recipient.email_id,
                'recipient_email': recipient.recipient_email,
            })

        email_list.append({
            'id': email.id,
            'event_id': email.event_id,
            'email_subject': email.email_subject,
            'email_content': email.email_content,
            'timestamp': email.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'recipients': recipients
        })

    pagination_info = {
        'total_data': total_emails,
        'total_pages': total_pages,
        'current_page': page,
        'data_per_page': size
    }

    response_data = {
        'data': email_list,
        'pagination': pagination_info
    }

    return response_data

def get_by_id(id):
    recipients = []
    email = db.query(Email).get(id)

    if not email:
        abort(404, f"Email with ID {id} not found")

    for recipient in email.recipients:
        recipients.append({
            'id': recipient.id,
            'email_id': recipient.email_id,
            'recipient_email': recipient.recipient_email,
        })

    data = {
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'recipients': recipients
    }

    return data