from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_student
from app.database.connection import get_db
from app.models.user import User
from app.services import progress_service

router = APIRouter(prefix="/api/student", tags=["progress"])


@router.get("/progress")
def progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return progress_service.progress(db, user)
