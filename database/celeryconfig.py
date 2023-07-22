import os

from dotenv import load_dotenv
from celery import Celery

load_dotenv()

celery = Celery(__name__, broker=os.environ.get('BROKER_URL'), backend=os.environ.get('RESULT_BACKEND'), include=['service.email'])