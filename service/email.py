import os
import pytz
import math

from flask import abort
from dotenv import load_dotenv
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from database.models import Email
from database import session as db
from datetime import datetime
from database.celeryconfig import celery

load_dotenv()

def convert_tz(dt):
    timezone = pytz.timezone(os.environ.get('TIMEZONE'))
    return timezone.localize(dt)

@celery.task
def send(event_id, email_subject, email_content, timestamp):
    # smtp_host = 'smtp.example.com'
    # smtp_port = 587
    # smtp_username = 'your_smtp_username'
    # smtp_password = 'your_smtp_password'
    # sender_email = 'sender@example.com'
    # recipient_email = 'recipient@example.com'

    # msg = MIMEMultipart()
    # msg['From'] = sender_email
    # msg['To'] = recipient_email
    # msg['Subject'] = email_subject

    # msg.attach(MIMEText(email_content, 'plain'))

    # try:
    #     with smtplib.SMTP(smtp_host, smtp_port) as server:
    #         server.starttls()
    #         server.login(smtp_username, smtp_password)
    #         server.sendmail(sender_email, recipient_email, msg.as_string())
    #         print("Email sent successfully.")
    # except Exception as e:
    #     print(f"Failed to send email: {e}")
    print('send email')

def save(data):
    event_id = data['event_id']
    email_subject = data['email_subject']
    email_content = data['email_content']
    timestamp_str = data['timestamp']
    
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        abort(400, 'Invalid timestamp format')

    email = Email(event_id=event_id,
                  email_subject=email_subject,
                  email_content=email_content,
                  timestamp=convert_tz(timestamp))

    db.add(email)
    db.commit()

    # send.apply_async(args=[event_id, email_subject, email_content], eta=convert_tz(timestamp))

    return {
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

def get_all(page, size):
    total_emails = db.query(Email).count()
    total_pages = math.ceil(total_emails / size)

    offset = (page - 1) * size

    emails = db.query(Email).limit(size).offset(offset).all()

    email_list = [{
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for email in emails]

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
    email = db.query(Email).get(id)

    if not email:
        abort(404, f"Email with ID {id} not found")

    data = {
        'id': email.id,
        'event_id': email.event_id,
        'email_subject': email.email_subject,
        'email_content': email.email_content,
        'timestamp': email.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

    return data

def delete(id):
    email = db.query(Email).get(id)

    if not email:
        abort(404, f"Email with ID {id} not found")

    db.delete(email)
    db.commit()

    return True