from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_student
from app.database.connection import get_db
from app.models.user import User
from app.schemas.quiz import QuizSubmitRequest
from app.services import quiz_service

router = APIRouter(prefix="/api/quizzes", tags=["quiz"])


@router.get("/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db),
             user: User = Depends(get_current_user)):
    return quiz_service.quiz_payload(quiz_service.get_quiz(db, quiz_id))


@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: int, payload: QuizSubmitRequest,
                user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return quiz_service.submit(db, user, quiz_id, payload)
