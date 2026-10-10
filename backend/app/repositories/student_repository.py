from sqlalchemy.orm import Session

from app.models.student_profile import StudentProfile
from app.models.student_progress import StudentProgress
from app.models.user import User


def get_profile(db: Session, user_id: int) -> StudentProfile | None:
    return db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()


def create_profile(db: Session, user_id: int, age: int | None, preferred_format: str,
                   learning_requirement: str | None = None) -> StudentProfile:
    profile = StudentProfile(user_id=user_id, age=age, preferred_format=preferred_format,
                             learning_requirement=learning_requirement)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: StudentProfile, **fields) -> StudentProfile:
    for key, value in fields.items():
        if value is not None:
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


def get_progress(db: Session, student_id: int, lesson_id: int) -> StudentProgress | None:
    return db.query(StudentProgress).filter(
        StudentProgress.student_id == student_id,
        StudentProgress.lesson_id == lesson_id,
    ).first()


def set_progress(db: Session, student_id: int, lesson_id: int, value: float,
                 completed: bool | None = None) -> StudentProgress:
    """Raise progress to `value` (never lowers it) and upsert the row."""
    row = get_progress(db, student_id, lesson_id)
    if row is None:
        row = StudentProgress(student_id=student_id, lesson_id=lesson_id,
                              progress_percentage=max(0.0, min(100.0, value)))
        if completed is not None:
            row.completed = completed
        db.add(row)
    else:
        row.progress_percentage = max(row.progress_percentage, max(0.0, min(100.0, value)))
        if completed:
            row.completed = True
    db.commit()
    db.refresh(row)
    return row


def all_progress(db: Session, student_id: int) -> list[StudentProgress]:
    return db.query(StudentProgress).filter(StudentProgress.student_id == student_id).all()
