from sqlalchemy.orm import Session

from app.models.user import User
from app.services.student_service import _student_stats


def progress(db: Session, user: User) -> dict:
    stats = _student_stats(db, user)
    recent = []
    seen = set()
    for a in stats["attempts"]:
        title = a.quiz.lesson.title if a.quiz and a.quiz.lesson else "Quiz"
        key = (a.quiz_id, title)
        if key in seen:
            continue
        seen.add(key)
        recent.append({"quiz": title, "percentage": a.percentage,
                       "attempt_number": a.attempt_number,
                       "created_at": a.created_at.isoformat() if a.created_at else None})
        if len(recent) >= 8:
            break
    return {
        "overall_progress": stats["overall_progress"],
        "average_score": stats["average_score"],
        "lessons_completed": stats["completed"],
        "total_lessons": stats["total_lessons"],
        "quiz_attempts": stats["quiz_attempts"],
        "improvement": stats["improvement"],
        "subject_progress": stats["subject_progress"],
        "recent_quizzes": recent,
    }
