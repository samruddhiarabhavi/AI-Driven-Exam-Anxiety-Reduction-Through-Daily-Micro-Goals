# services/micro_goal_engine.py

import random
from models.goal import DailyGoal
from models import db

def generate_micro_goals(student, syllabus):
    """
    Generates 2–4 realistic daily micro-goals by grouping syllabus topics.
    
    Args:
        student: Student model instance
        syllabus: List of topics from parser, each a dict {"subject", "chapter", "topic"}
    
    Returns:
        List of DailyGoal objects created for today
    """

    if not syllabus or not student:
        return []

    goals = []

    # ---- GROUP SYLLABUS BY SUBJECT + CHAPTER ----
    grouped = {}
    for item in syllabus:
        key = (item.get("subject", "General"), item.get("chapter", "General"))
        grouped.setdefault(key, []).append(item.get("topic", "Unknown"))

    grouped_items = list(grouped.items())
    random.shuffle(grouped_items)

    # ---- PICK 1–2 CHAPTERS FOR TODAY ----
    selected_chapters = grouped_items[:2]

    # ---- CREATE REVISION GOALS ----
    for (subject, chapter), topics in selected_chapters:
        # Assign time based on number of topics
        time = 20 if len(topics) <= 4 else 30

        title = f"Revise {subject} – {chapter} overview"

        goal = DailyGoal(
            student_id=student.id,
            title=title,
            time_minutes=time,
            goal_type="revision"  # optional column, add if needed in model
        )
        goals.append(goal)

    # ---- CREATE PRACTICE OR MISTAKE-FIX GOAL ----
    last_accuracy = getattr(student, "last_accuracy", None)

    if last_accuracy is not None and last_accuracy < 70:
        # Low performance → mistake revision
        goal = DailyGoal(
            student_id=student.id,
            title="Revise 5 mistakes from last test",
            time_minutes=15,
            goal_type="mistake-fix"
        )
    else:
        # Normal → practice questions
        goal = DailyGoal(
            student_id=student.id,
            title="Solve 5 medium practice questions",
            time_minutes=25,
            goal_type="practice"
        )
    goals.append(goal)

    # ---- LIMIT TOTAL GOALS TO 4 ----
    goals = goals[:4]

    # ---- SAVE TO DATABASE ----
    if goals:
        db.session.add_all(goals)
        db.session.commit()

    return goals
