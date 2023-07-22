from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    email_subject = Column(String(255))
    email_content = Column(Text)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f"<Email(id={self.id}, event_id={self.event_id}, email_subject={self.email_subject})>"
