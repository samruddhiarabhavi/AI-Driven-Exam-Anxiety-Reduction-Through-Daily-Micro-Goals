from datetime import datetime, date
from models import db

class DailyGoal(db.Model):
    __tablename__ = "daily_goals"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100))
    chapter = db.Column(db.String(100))
    topic = db.Column(db.String(100))

    time_minutes = db.Column(db.Integer, default=20)
    difficulty = db.Column(db.String(20), default="easy")

    is_completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.Date, default=date.today)
    completed_at = db.Column(db.DateTime)

    questions_attempted = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, default=0.0)
    mistakes = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def mark_completed(self, attempted=0, accuracy=0.0, mistakes=0):
        self.is_completed = True
        self.completed_at = datetime.utcnow()
        self.questions_attempted = attempted
        self.accuracy = accuracy
        self.mistakes = mistakes

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "time": self.time_minutes,
            "completed": self.is_completed,
            "difficulty": self.difficulty
        }

    def __repr__(self):
        return f"<DailyGoal {self.title}>"
