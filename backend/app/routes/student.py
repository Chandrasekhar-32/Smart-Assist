from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_student
from app.database.connection import get_db
from app.models.user import User
from app.schemas.student import ProfileOut, ProfileUpdate
from app.services import student_service

router = APIRouter(prefix="/api/student", tags=["student"])


@router.get("/profile")
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return student_service.profile_dict(db, user)


@router.put("/profile")
def update_profile(payload: ProfileUpdate, user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    require_student(user)
    return student_service.update_profile(db, user, payload)


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return student_service.dashboard(db, user)


@router.get("/lessons")
def my_lessons(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return student_service.my_lessons(db, user)
