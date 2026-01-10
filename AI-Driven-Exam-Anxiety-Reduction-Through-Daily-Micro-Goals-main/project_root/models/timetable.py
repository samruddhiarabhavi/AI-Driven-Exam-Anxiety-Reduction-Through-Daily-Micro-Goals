from models import db
from datetime import datetime

class TimetableHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    timetable_json = db.Column(db.Text)
