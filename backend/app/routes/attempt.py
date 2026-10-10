from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_student
from app.database.connection import get_db
from app.models.user import User
from app.repositories import attempt_repository

router = APIRouter(prefix="/api/attempts", tags=["attempts"])


@router.get("")
def my_attempts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    rows = attempt_repository.list_for_student(db, user.id)
    return [{
        "id": a.id, "quiz_id": a.quiz_id,
        "lesson": a.quiz.lesson.title if a.quiz and a.quiz.lesson else "Quiz",
        "score": a.score, "percentage": a.percentage,
        "time_taken": a.time_taken, "attempt_number": a.attempt_number,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    } for a in rows]
