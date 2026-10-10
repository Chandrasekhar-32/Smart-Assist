from sqlalchemy.orm import Session, joinedload

from app.models.recommendation import Recommendation


def create(db: Session, student_id: int, lesson_id: int | None, resource_id: int | None,
           recommended_format: str, difficulty: str, confidence: float, reason: str) -> Recommendation:
    rec = Recommendation(student_id=student_id, lesson_id=lesson_id, resource_id=resource_id,
                         recommended_format=recommended_format, difficulty=difficulty,
                         confidence=confidence, reason=reason)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def latest_for_student(db: Session, student_id: int) -> Recommendation | None:
    return db.query(Recommendation) \
        .options(joinedload(Recommendation.lesson), joinedload(Recommendation.resource)) \
        .filter(Recommendation.student_id == student_id) \
        .order_by(Recommendation.id.desc()).first()


def for_lesson(db: Session, student_id: int, lesson_id: int) -> Recommendation | None:
    return db.query(Recommendation) \
        .options(joinedload(Recommendation.lesson), joinedload(Recommendation.resource)) \
        .filter(Recommendation.student_id == student_id, Recommendation.lesson_id == lesson_id) \
        .order_by(Recommendation.id.desc()).first()


def list_for_student(db: Session, student_id: int, limit: int = 20) -> list[Recommendation]:
    return db.query(Recommendation) \
        .options(joinedload(Recommendation.lesson), joinedload(Recommendation.resource)) \
        .filter(Recommendation.student_id == student_id) \
        .order_by(Recommendation.id.desc()).limit(limit).all()


def list_all(db: Session, limit: int = 100) -> list[Recommendation]:
    return db.query(Recommendation) \
        .options(joinedload(Recommendation.lesson), joinedload(Recommendation.student)) \
        .order_by(Recommendation.id.desc()).limit(limit).all()


def count_all(db: Session) -> int:
    return db.query(Recommendation).count()
