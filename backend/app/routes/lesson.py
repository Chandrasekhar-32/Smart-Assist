from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_student
from app.database.connection import get_db
from app.models.user import User
from app.services import lesson_service

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


@router.get("/{lesson_id}")
def lesson_detail(lesson_id: int, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    return lesson_service.lesson_detail(db, user, lesson_id)


@router.get("/{lesson_id}/resources")
def lesson_resources(lesson_id: int, user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    return lesson_service.resources(db, user, lesson_id)


@router.post("/{lesson_id}/view")
def mark_viewed(lesson_id: int, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    require_student(user)
    return lesson_service.mark_viewed(db, user, lesson_id)
