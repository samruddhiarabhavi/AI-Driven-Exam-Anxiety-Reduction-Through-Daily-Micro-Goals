from models.session import StudySession
from models.student import db

def analyze_progress(student):
    sessions = StudySession.query.filter_by(student_id=student.id).all()

    if not sessions:
        return

    total_attempts = sum(s.questions_attempted for s in sessions)
    avg_accuracy = (
        sum(s.accuracy for s in sessions) / len(sessions)
    )

    # Update student stats
    student.total_attempts = total_attempts
    student.avg_accuracy = round(avg_accuracy, 2)

    # Repeated mistakes
    repeated = {}
    for s in sessions:
        if s.repeated_topic:
            repeated[s.repeated_topic] = repeated.get(s.repeated_topic, 0) + 1

    student.repeated_mistakes = max(repeated.values()) if repeated else 0

    # Update confidence & stress
    student.update_confidence()
    student.detect_stress()

    db.session.commit()


def confidence_trend(student, limit=5):
    sessions = (
        StudySession.query
        .filter_by(student_id=student.id)
        .order_by(StudySession.session_date.desc())
        .limit(limit)
        .all()
    )

    sessions.reverse()
    return {
        "labels": [s.session_date.strftime("%a") for s in sessions],
        "values": [s.accuracy for s in sessions]
    }
