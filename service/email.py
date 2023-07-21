import os
from flask import abort
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from database.models import Email
from database import db
from datetime import datetime, timezone
from database.celeryconfig import celery

load_dotenv()

def convert_tz(dt):
    tz = timezone(os.environ.get('TIMEZONE'))
    return dt.astimezone(tz)

@celery.task
def send(event_id, email_subject, email_content, timestamp):
    smtp_host = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_smtp_username'
    smtp_password = 'your_smtp_password'
    sender_email = 'sender@example.com'
    recipient_email = 'recipient@example.com'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_content, 'plain'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def save(data):
    event_id = data['event_id']
    email_subject = data['email_subject']
    email_content = data['email_content']
    timestamp_str = data['timestamp']
    
    try:
        timestamp = datetime.strptime(timestamp_str, '%d %b %Y %H:%M')
    except ValueError:
        abort(400, 'Invalid timestamp format')

    email = Email(event_id=event_id,
                  email_subject=email_subject,
                  email_content=email_content,
                  timestamp=convert_tz(timestamp))

    db.session.add(email)
    db.session.commit()

    send.apply_async(args=[event_id, email_subject, email_content], eta=convert_tz(timestamp))

    return email

def get_all(page, size):
    emails_query = Email.query.order_by(Email.timestamp.desc())

    total_emails = emails_query.count()
    total_pages = (total_emails + size - 1) // size

    emails = emails_query.paginate(page, per_page=size)

    email_list = [{
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%d %b %Y %H:%M')
    } for email in emails.items]

    pagination_info = {
        'total_emails': total_emails,
        'total_pages': total_pages,
        'current_page': page,
        'emails_per_page': size
    }

    response_data = {
        'emails': email_list,
        'pagination': pagination_info
    }

    return response_data

def get_by_id(id):
    email = Email.query.get(id)

    if not email:
        abort(404, f"Email with ID {id} not found")

    data = {
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%d %b %Y %H:%M')
    }

    return data

def delete(email_id):
    email = Email.query.get(email_id)

    if not email:
        abort(404, f"Email with ID {email_id} not found")

    db.session.delete(email)
    db.session.commit()

    return True