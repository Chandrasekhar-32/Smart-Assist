from sqlalchemy.orm import Session, joinedload

from app.models.attempt import Attempt
from app.models.quiz import Quiz
from app.models.user import User


def create(db: Session, student_id: int, quiz_id: int, score: int, percentage: float,
           time_taken: int, attempt_number: int) -> Attempt:
    attempt = Attempt(student_id=student_id, quiz_id=quiz_id, score=score,
                      percentage=percentage, time_taken=time_taken,
                      attempt_number=attempt_number)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def count_for_quiz(db: Session, student_id: int, quiz_id: int) -> int:
    return db.query(Attempt).filter(Attempt.student_id == student_id,
                                    Attempt.quiz_id == quiz_id).count()


def list_for_quiz(db: Session, student_id: int, quiz_id: int) -> list[Attempt]:
    return db.query(Attempt).filter(Attempt.student_id == student_id,
                                    Attempt.quiz_id == quiz_id) \
        .order_by(Attempt.attempt_number).all()


def latest_for_quiz(db: Session, student_id: int, quiz_id: int) -> Attempt | None:
    return db.query(Attempt).filter(Attempt.student_id == student_id,
                                    Attempt.quiz_id == quiz_id) \
        .order_by(Attempt.attempt_number.desc()).first()


def list_for_student(db: Session, student_id: int, limit: int = 50) -> list[Attempt]:
    return db.query(Attempt).options(joinedload(Attempt.quiz).joinedload(Quiz.lesson)) \
        .filter(Attempt.student_id == student_id) \
        .order_by(Attempt.created_at.desc(), Attempt.id.desc()).limit(limit).all()


def list_all(db: Session, limit: int = 200) -> list[Attempt]:
    return db.query(Attempt).options(joinedload(Attempt.quiz).joinedload(Quiz.lesson),
                                     joinedload(Attempt.student)) \
        .order_by(Attempt.created_at.desc(), Attempt.id.desc()).limit(limit).all()
