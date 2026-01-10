from flask import Blueprint, render_template, jsonify, redirect, url_for
from models.student import Student
from models.goal import DailyGoal
from services.progress_analyzer import confidence_trend

parent_bp = Blueprint("parent", __name__, url_prefix="/parent")


# ---------------- PARENT DASHBOARD PAGE ----------------
@parent_bp.route("/<int:student_id>")
def parent_view(student_id):
    student = Student.query.get(student_id)

    if not student:
        return redirect(url_for("auth.login_page"))

    return render_template(
        "parent.html",
        student_name=student.name,
        student_id=student.id
    )


# ---------------- PARENT API ----------------
@parent_bp.route("/api/<int:student_id>")
def parent_api(student_id):
    student = Student.query.get(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # ---- CONFIDENCE TREND ----
    trend = confidence_trend(student)

    # ---- DAILY GOALS (FOR CONTEXT) ----
    goals = DailyGoal.query.filter_by(
        student_id=student.id,
        is_completed=False
    ).limit(4).all()

    total_study_time = sum(g.time_minutes for g in goals)

    # ---- CONFIDENCE INTERPRETATION ----
    if student.confidence_score >= 75:
        confidence_message = (
            "Your child is feeling confident and emotionally stable."
        )
    elif student.confidence_score >= 50:
        confidence_message = (
            "Your child is moderately confident but may need reassurance."
        )
    else:
        confidence_message = (
            "Your child may be anxious or underconfident. Emotional support is very important now."
        )

    # ---- DAILY ROUTINE GUIDANCE ----
    routine = {
        "wake_up": "6:30 – 7:00 AM",
        "study_blocks": f"{len(goals)} calm sessions (20–30 min each)",
        "breaks": "5–10 min break after every session",
        "lunch": "1:00 – 2:00 PM (no study pressure)",
        "evening_revision": "Light revision only, no new topics",
        "dinner": "7:30 – 8:30 PM",
        "sleep": "Before 11:00 PM (critical for memory)"
    }

    # ---- PARENT SUPPORT TIPS ----
    support_tips = []

    if student.stress_flag:
        support_tips.extend([
            "Your child is under exam stress. Please avoid pressure or comparisons.",
            "Encourage short study sessions instead of long hours.",
            "Reassure them that effort matters more than perfection."
        ])
    else:
        support_tips.append(
            "Your child appears emotionally balanced. Maintain the current routine."
        )

    if student.current_streak < 3:
        support_tips.append(
            "Help your child rebuild consistency. Even 20 minutes of study is enough today."
        )
    else:
        support_tips.append(
            "Acknowledge your child’s consistency — small praise boosts motivation."
        )

    support_tips.append(
        "Ensure your child gets proper sleep; anxiety reduces sharply with rest."
    )

    return jsonify({
        "student_name": student.name,
        "confidence_score": student.confidence_score,
        "confidence_message": confidence_message,
        "streak": student.current_streak,
        "stress": student.stress_flag,
        "trend": trend,
        "today_study_time_minutes": total_study_time,
        "routine_guidance": routine,
        "support_tips": support_tips
    })
