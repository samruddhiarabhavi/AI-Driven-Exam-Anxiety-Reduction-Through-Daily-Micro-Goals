from datetime import datetime
from models import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    # ---------- BASIC INFO ----------
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # ---------- DAILY ROUTINE (FOR TIMETABLE) ----------
    wake_time = db.Column(db.String(10), default="06:30")
    sleep_time = db.Column(db.String(10), default="22:30")
    study_hours = db.Column(db.Integer, default=6)  # hours/day

    # ---------- STUDY METRICS ----------
    confidence_score = db.Column(db.Integer, default=50)
    current_streak = db.Column(db.Integer, default=0)
    days_active = db.Column(db.Integer, default=0)

    # ---------- PERFORMANCE ----------
    avg_accuracy = db.Column(db.Float, default=0.0)
    total_attempts = db.Column(db.Integer, default=0)
    repeated_mistakes = db.Column(db.Integer, default=0)

    # ---------- STRESS ----------
    stress_flag = db.Column(db.Boolean, default=False)
    last_active_date = db.Column(db.Date, default=datetime.utcnow)

    # ---------- SETTINGS ----------
    preferred_language = db.Column(db.String(20), default="en")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- METHODS ----------
    def update_streak(self, studied_today: bool):
        if studied_today:
            self.current_streak += 1
            self.days_active += 1
        else:
            self.current_streak = 0

    def update_confidence(self):
        accuracy_component = min(self.avg_accuracy, 100) * 0.5
        streak_component = min(self.current_streak * 5, 30)
        effort_component = min(self.total_attempts / 10, 20)
        self.confidence_score = int(
            min(accuracy_component + streak_component + effort_component, 100)
        )

    def detect_stress(self):
        self.stress_flag = (
            self.total_attempts < 5 or
            self.repeated_mistakes > 10 or
            self.current_streak == 0
        )

    def to_dashboard_dict(self):
        return {
            "name": self.name,
            "confidence": self.confidence_score,
            "streak": self.current_streak,
            "stress_flag": self.stress_flag,
            "wake_time": self.wake_time,
            "sleep_time": self.sleep_time,
            "study_hours": self.study_hours
        }

    def __repr__(self):
        return f"<Student {self.name}>"
