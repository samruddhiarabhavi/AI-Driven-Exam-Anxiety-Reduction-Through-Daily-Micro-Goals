from datetime import datetime, date
from models import db

class StudySession(db.Model):
    __tablename__ = "study_sessions"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    goal_id = db.Column(
        db.Integer,
        db.ForeignKey("daily_goals.id"),
        nullable=True
    )

    session_date = db.Column(db.Date, default=date.today)

    time_spent_minutes = db.Column(db.Integer, default=0)
    questions_attempted = db.Column(db.Integer, default=0)

    correct_answers = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, default=0.0)

    mistakes = db.Column(db.Integer, default=0)
    repeated_topic = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_accuracy(self):
        if self.questions_attempted > 0:
            self.accuracy = round(
                (self.correct_answers / self.questions_attempted) * 100, 2
            )

    def to_dict(self):
        return {
            "date": self.session_date.strftime("%Y-%m-%d"),
            "accuracy": self.accuracy,
            "mistakes": self.mistakes
        }

    def __repr__(self):
        return f"<StudySession {self.session_date}>"
