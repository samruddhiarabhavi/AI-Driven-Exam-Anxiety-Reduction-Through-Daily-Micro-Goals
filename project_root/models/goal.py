from datetime import datetime, date
from models import db

class DailyGoal(db.Model):
    __tablename__ = "daily_goals"

    # ---------------- PRIMARY KEYS ----------------
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    # ---------------- GOAL CONTENT ----------------
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), default="General")
    chapter = db.Column(db.String(100), default="General")
    topic = db.Column(db.String(100), default="General")

    # ---------------- PLANNING ----------------
    time_minutes = db.Column(db.Integer, default=20)
    difficulty = db.Column(db.String(20), default="easy")

    # ---------------- COMPLETION & SKIP ----------------
    is_completed = db.Column(db.Boolean, default=False)
    is_skipped = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    skipped_at = db.Column(db.DateTime)

    # ---------------- PERFORMANCE TRACKING ----------------
    questions_attempted = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, default=0.0)
    mistakes = db.Column(db.Integer, default=0)

    # ---------------- HELPERS ----------------
    def mark_completed(self, attempted=0, accuracy=0.0, mistakes=0):
        """
        Mark goal as completed.
        Resets skip flag and updates performance metrics.
        """
        self.is_completed = True
        self.is_skipped = False
        self.completed_at = datetime.utcnow()
        self.questions_attempted = attempted
        self.accuracy = accuracy
        self.mistakes = mistakes

    def mark_skipped(self):
        """
        Mark goal as skipped.
        Does not penalize student metrics.
        """
        self.is_skipped = True
        self.is_completed = False
        self.skipped_at = datetime.utcnow()

    # ---------------- SERIALIZATION ----------------
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "chapter": self.chapter,
            "topic": self.topic,
            "time": self.time_minutes,
            "difficulty": self.difficulty,
            "completed": self.is_completed,
            "skipped": self.is_skipped,
            "questions_attempted": self.questions_attempted,
            "accuracy": self.accuracy,
            "mistakes": self.mistakes,
            "created_date": self.created_date.strftime("%Y-%m-%d"),
            "completed_at": self.completed_at.strftime("%Y-%m-%d %H:%M:%S") if self.completed_at else None,
            "skipped_at": self.skipped_at.strftime("%Y-%m-%d %H:%M:%S") if self.skipped_at else None
        }

    # ---------------- REPRESENTATION ----------------
    def __repr__(self):
        state = "✓" if self.is_completed else "↷" if self.is_skipped else "•"
        return f"<DailyGoal {state} {self.title}>"
