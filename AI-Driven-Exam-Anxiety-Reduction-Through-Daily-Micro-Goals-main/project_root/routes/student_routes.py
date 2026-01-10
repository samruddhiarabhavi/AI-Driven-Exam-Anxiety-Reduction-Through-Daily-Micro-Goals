from flask import (
    Blueprint, render_template, jsonify,
    session, redirect, url_for, request
)
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

from models import db
from models.student import Student
from models.goal import DailyGoal
from models.session import StudySession

from services.progress_analyzer import analyze_progress, confidence_trend
from services.encouragement_engine import generate_encouragement
from services.syllabus_parser import parse_syllabus_file

student_bp = Blueprint("student", __name__, url_prefix="/student")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HELPER ----------------
def get_logged_student():
    student_id = session.get("student_id")
    if not student_id:
        return None
    return Student.query.get(student_id)


def generate_timetable(goals, wake_time="06:30", sleep_time="22:30"):
    """
    Generates realistic timetable with breaks & meals
    """
    schedule = []
    current = datetime.strptime(wake_time, "%H:%M")

    def add_block(title, minutes):
        nonlocal current
        start = current.strftime("%H:%M")
        current += timedelta(minutes=minutes)
        end = current.strftime("%H:%M")
        schedule.append({"title": title, "start": start, "end": end})

    # Morning routine
    add_block("Wake up & freshen up", 30)
    add_block("Breakfast", 20)

    # Study blocks
    for goal in goals:
        add_block(goal.title, goal.time_minutes)
        add_block("Short break", 10)

    # Lunch
    add_block("Lunch & rest", 40)

    # Light revision
    add_block("Light revision / practice", 30)

    # Dinner
    add_block("Dinner & relax", 40)

    # Wind down
    add_block("Free time / family time", 30)

    # Sleep
    schedule.append({"title": "Sleep", "start": current.strftime("%H:%M"), "end": sleep_time})

    return schedule


# ---------------- DASHBOARD PAGE ----------------
@student_bp.route("/dashboard")
def dashboard():
    student = get_logged_student()
    if not student:
        return redirect(url_for("auth.login_page"))
    return render_template("index.html")


# ---------------- DASHBOARD DATA ----------------
@student_bp.route("/api/dashboard-data")
def dashboard_data():
    student = get_logged_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    analyze_progress(student)
    student.update_confidence()
    student.detect_stress()
    db.session.commit()

    goals = DailyGoal.query.filter_by(
        student_id=student.id,
        is_completed=False
    ).order_by(DailyGoal.created_at.desc()).all()

    timetable = generate_timetable(
        goals,
        wake_time=student.wake_time,
        sleep_time=student.sleep_time
    )

    return jsonify({
        "name": student.name,
        "confidence": student.confidence_score,
        "streak": student.current_streak,
        "stress": student.stress_flag,
        "encouragement": generate_encouragement(student),
        "trend": confidence_trend(student),
        "timetable": timetable,
        "goals": [
            {"id": g.id, "title": g.title, "time": g.time_minutes, "completed": g.is_completed}
            for g in goals
        ],
        "parent_summary": {
            "daily_study_time": sum(g.time_minutes for g in goals),
            "sleep_time": student.sleep_time,
            "wake_time": student.wake_time,
            "stress_flag": student.stress_flag
        }
    })


# ---------------- SYLLABUS UPLOAD ----------------
@student_bp.route("/api/upload-syllabus", methods=["POST"])
def upload_syllabus():
    student = get_logged_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    available_hours = int(request.form.get("available_hours", student.study_hours))
    wake_time = request.form.get("wake_time", student.wake_time)
    sleep_time = request.form.get("sleep_time", student.sleep_time)

    student.wake_time = wake_time
    student.sleep_time = sleep_time
    student.study_hours = available_hours
    db.session.commit()

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    topics = parse_syllabus_file(file_path)
    if not topics:
        return jsonify({"error": "No syllabus topics detected"}), 400

    # Clear previous goals
    DailyGoal.query.filter_by(student_id=student.id).delete()

    # Create simple goals per topic
    created_goals = []
    max_minutes = available_hours * 60
    used_minutes = 0

    for t in topics:
        if used_minutes >= max_minutes:
            break

        goal = DailyGoal(
            student_id=student.id,
            title=f"{t.get('subject', 'General')} – {t.get('chapter', 'General')} – {t.get('topic')}",
            subject=t.get("subject", "General"),
            chapter=t.get("chapter", "General"),
            topic=t.get("topic"),
            time_minutes=30  # default per topic
        )
        used_minutes += goal.time_minutes
        db.session.add(goal)
        created_goals.append(goal)

    db.session.commit()

    return jsonify({
        "message": f"Smart timetable generated for {available_hours} hour(s)",
        "goals_created": len(created_goals)
    })


# ---------------- STUDY HISTORY ----------------
@student_bp.route("/api/history-data")
def history_data():
    student = get_logged_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    sessions = StudySession.query.filter_by(
        student_id=student.id
    ).order_by(StudySession.session_date.asc()).all()

    return jsonify([
        {
            "date": s.session_date.strftime("%Y-%m-%d"),
            "accuracy": s.accuracy,
            "attempts": s.questions_attempted,
            "topic": s.repeated_topic
        }
        for s in sessions
    ])
