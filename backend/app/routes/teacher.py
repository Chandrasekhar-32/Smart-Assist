from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_teacher
from app.database.connection import get_db
from app.models.user import User
from app.repositories import attempt_repository, recommendation_repository
from app.services import recommendation_service, student_service

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_teacher(user)
    return student_service.teacher_dashboard(db)


@router.get("/students")
def students(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_teacher(user)
    return student_service.teacher_dashboard(db)["students"]


@router.get("/students/{student_id}")
def student_details(student_id: int, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    require_teacher(user)
    details = student_service.teacher_student_details(db, student_id)
    if details is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return details


@router.get("/students/{student_id}/performance")
def student_performance(student_id: int, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    require_teacher(user)
    details = student_service.teacher_student_details(db, student_id)
    if details is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student_id": student_id,
            "recent_performance": details["recent_performance"],
            "history": details["history"]}


@router.get("/recommendations")
def recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_teacher(user)
    return [recommendation_service.serialize(r)
            for r in recommendation_repository.list_all(db, limit=100)]


@router.get("/attempts")
def all_attempts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_teacher(user)
    rows = attempt_repository.list_all(db, limit=200)
    return [{
        "id": a.id, "student": a.student.name if a.student else "",
        "lesson": a.quiz.lesson.title if a.quiz and a.quiz.lesson else "Quiz",
        "score": a.score, "percentage": a.percentage,
        "time_taken": a.time_taken, "attempt_number": a.attempt_number,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    } for a in rows]
