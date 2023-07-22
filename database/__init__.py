import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from database.models import Base

load_dotenv()

engine = create_engine(os.environ.get('DB_URI'))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()