from sqlalchemy.orm import Session

from app.models.student_profile import StudentProfile
from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower().strip()).first()


def get(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def create(db: Session, name: str, email: str, password_hash: str, role: str) -> User:
    user = User(name=name, email=email.lower().strip(), password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_students(db: Session) -> list[User]:
    return db.query(User).filter(User.role == "STUDENT").order_by(User.name).all()
