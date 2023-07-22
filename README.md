# Email Scheduler Web Application

The Email Scheduler Web Application is a simple web app built with Python 3+ and the Flask microframework. It allows users to schedule emails for a particular group of recipients, which will be sent automatically at a later time. The application provides a RESTful API to interact with the email scheduling functionality and includes Swagger documentation for easy exploration and testing of the API endpoints.

## Features

- Schedule emails for a specific group of recipients.
- Emails are sent automatically at the specified timestamp.
- RESTful API with several endpoints for managing emails.
- Swagger documentation for API exploration and testing.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pradnyanandana/email-scheduler.git
cd email-scheduler
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up the environment variables by creating a `.env` file in the root directory of the project. The `.env` file should contain the following configurations:

```plaintext
DB_DATABASE=db
DB_PASSWORD=pass
DB_USERNAME=user
DB_URI=mysql+pymysql://${DB_USERNAME}:${DB_PASSWORD}@localhost/${DB_DATABASE}

BROKER_URL=redis://localhost:6379/0
RESULT_BACKEND=redis://localhost:6379/0
TIMEZONE=Asia/Singapore
```

**Note**: Before running the application, ensure that you have a MySQL database and a Redis server running locally with the configurations specified in the `.env` file.

4. Start the Celery task worker:

```bash
celery -A database.celeryconfig worker --loglevel=info 
```

5. Start the development server:

```bash
python app.py
```

The application will be running at `http://127.0.0.1:5000/`.

## API Documentation

The API documentation is available through Swagger UI. You can access it at `http://127.0.0.1:5000/api-docs`.

## Endpoints

The Email Scheduler API provides the following endpoints:

- `POST /save_emails`: Save emails for scheduling.
- `GET /save_emails`: Get all scheduled emails with pagination.
- `GET /save_emails/<int:email_id>`: Get a specific scheduled email by ID.
- `DELETE /save_emails/<int:email_id>`: Delete a scheduled email by ID.

## Usage

To schedule an email, make a `POST` request to the `/save_emails` endpoint with the required parameters:

```json
{
  "event_id": 1,
  "email_subject": "Email Subject",
  "email_content": "Email Body",
  "timestamp": "2023-12-15 23:12"
}
```

The email will be saved in the database and automatically sent at the specified timestamp.

To view all scheduled emails, make a `GET` request to the `/save_emails` endpoint. You can use pagination parameters `page` and `page_size` to navigate through the results.

To get a specific scheduled email by ID, make a `GET` request to the `/save_emails/<email_id>` endpoint.

To delete a scheduled email by ID, make a `DELETE` request to the `/save_emails/<email_id>` endpoint.

## Testing

To run the unit tests, use the following command:

```bash
pytest
```