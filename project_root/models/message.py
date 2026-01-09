from datetime import datetime
from models import db

class EncouragementMessage(db.Model):
    __tablename__ = "encouragement_messages"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    message_text = db.Column(db.String(300), nullable=False)
    message_type = db.Column(db.String(50), default="encouragement")
    language = db.Column(db.String(20), default="en")

    confidence_snapshot = db.Column(db.Integer)
    stress_flag_snapshot = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "message": self.message_text,
            "type": self.message_type,
            "language": self.language
        }

    def __repr__(self):
        return f"<EncouragementMessage {self.message_type}>"
