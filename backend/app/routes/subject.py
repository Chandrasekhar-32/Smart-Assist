from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.services import lesson_service

router = APIRouter(prefix="/api/subjects", tags=["subjects"])


@router.get("")
def list_subjects(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return lesson_service.subjects(db, user)


@router.get("/{subject_id}/lessons")
def subject_lessons(subject_id: int, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    return lesson_service.lessons_for_subject(db, user, subject_id)
