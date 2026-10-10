from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.repositories import student_repository, user_repository
from app.schemas.auth import RegisterRequest


def register(db: Session, payload: RegisterRequest) -> dict:
    if user_repository.get_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    role = payload.role.upper() if payload.role.upper() in ("STUDENT", "TEACHER") else "STUDENT"
    user = user_repository.create(db, payload.name, payload.email, hash_password(payload.password), role)
    if role == "STUDENT":
        student_repository.create_profile(db, user.id, payload.age, (payload.preferred_format or "TEXT").upper())
    token = create_access_token(user.id, user.role, user.email)
    return {"access_token": token, "token_type": "bearer", "user": user}


def login(db: Session, email: str, password: str) -> dict:
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(user.id, user.role, user.email)
    return {"access_token": token, "token_type": "bearer", "user": user}
