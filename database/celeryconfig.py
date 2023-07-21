import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(__name__, broker=os.environ.get('BROKER_URL'), backend=os.environ.get('RESULT_BACKEND'))
