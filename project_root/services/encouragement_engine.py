from models.message import EncouragementMessage
from models.student import db

def generate_encouragement(student):
    """
    Template-driven, data-based messages
    """

    if student.stress_flag:
        message = (
            "You’ve been trying hard. It’s okay to slow down today — "
            "short, calm revision will help more than pushing."
        )
        msg_type = "well-being"

    elif student.current_streak >= 5:
        message = (
            f"You maintained a {student.current_streak}-day study streak. "
            "This kind of consistency builds strong confidence."
        )
        msg_type = "encouragement"

    elif student.avg_accuracy > 0:
        message = (
            f"Your average accuracy is improving. "
            "Focus on understanding mistakes — you’re moving in the right direction."
        )
        msg_type = "encouragement"

    else:
        message = (
            "Starting small is a win. Complete one micro-goal today and build from there."
        )
        msg_type = "encouragement"

    encouragement = EncouragementMessage(
        student_id=student.id,
        message_text=message,
        message_type=msg_type,
        language=student.preferred_language,
        confidence_snapshot=student.confidence_score,
        stress_flag_snapshot=student.stress_flag
    )

    db.session.add(encouragement)
    db.session.commit()

    return encouragement.message_text
