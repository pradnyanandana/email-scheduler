from database import db

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email_subject = db.Column(db.String(255))
    email_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Email(id={self.id}, event_id={self.event_id}, email_subject={self.email_subject})>"
