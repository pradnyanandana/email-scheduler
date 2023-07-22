from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    email_subject = Column(String(255))
    email_content = Column(Text)
    timestamp = Column(DateTime)

    recipients = relationship('EmailRecipient', backref='email', lazy=True)

    def __repr__(self):
        return f"<Email(id={self.id}, event_id={self.event_id}, email_subject={self.email_subject})>"
    
class EmailRecipient(Base):
    __tablename__ = 'email_recipients'

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=False)
    recipient_email = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<EmailRecipient {self.recipient_email}>"
