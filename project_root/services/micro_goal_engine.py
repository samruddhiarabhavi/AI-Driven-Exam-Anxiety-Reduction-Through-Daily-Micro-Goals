import random
from models.goal import DailyGoal
from models import db


def generate_micro_goals(student, syllabus):
    """
    Generates 2–4 realistic daily goals by grouping syllabus topics.
    """

    goals = []

    # ---- GROUP SYLLABUS BY SUBJECT + CHAPTER ----
    grouped = {}
    for item in syllabus:
        key = (item["subject"], item["chapter"])
        grouped.setdefault(key, []).append(item["topic"])

    grouped_items = list(grouped.items())
    random.shuffle(grouped_items)

    # ---- PICK ONLY 1–2 CHAPTERS FOR TODAY ----
    selected_chapters = grouped_items[:2]

    # ---- REVISION GOALS (GROUPED) ----
    for (subject, chapter), topics in selected_chapters:
        time = 20 if len(topics) <= 4 else 30

        title = f"Revise {subject} – {chapter} overview"

        goals.append(
            DailyGoal(
                student_id=student.id,
                title=title,
                time_minutes=time,
                goal_type="revision",
            )
        )

    # ---- PRACTICE / MISTAKE GOAL ----
    if student.last_accuracy and student.last_accuracy < 70:
        goals.append(
            DailyGoal(
                student_id=student.id,
                title="Revise 5 mistakes from last test",
                time_minutes=15,
                goal_type="mistake-fix",
            )
        )
    else:
        goals.append(
            DailyGoal(
                student_id=student.id,
                title="Solve 5 medium practice questions",
                time_minutes=25,
                goal_type="practice",
            )
        )

    # ---- LIMIT TOTAL GOALS TO 4 ----
    goals = goals[:4]

    # ---- SAVE GOALS ----
    db.session.add_all(goals)
    db.session.commit()

    return goals
