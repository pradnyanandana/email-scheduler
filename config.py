import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get('BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('RESULT_BACKEND')
    CELERY_TIMEZONE = os.environ.get('TIMEZONE')
