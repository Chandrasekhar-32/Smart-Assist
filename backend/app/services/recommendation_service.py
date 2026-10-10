"""Bridges quiz performance -> ML predictor -> stored recommendation."""
from sqlalchemy.orm import Session

from app.core.config import TARGET_SCORE
from app.ml.predictor import predict
from app.models.attempt import Attempt
from app.models.lesson import Lesson
from app.models.recommendation import Recommendation
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.repositories import (attempt_repository, lesson_repository,
                               recommendation_repository, student_repository)


def build_features(db: Session, user: User, lesson: Lesson, attempt: Attempt) -> dict:
    """Section 12: minimum performance features sent to the ML service."""
    profile: StudentProfile | None = student_repository.get_profile(db, user.id)
    previous = attempt_repository.list_for_quiz(db, user.id, attempt.quiz_id)
    prev_attempt = next((a for a in previous if a.id != attempt.id), None)
    prev_percentage = prev_attempt.percentage if prev_attempt else (profile and None) or 0.0
    if prev_attempt is None:
        # first attempt: use the student's average of other quizzes as baseline
        others = attempt_repository.list_for_student(db, user.id, limit=10)
        others = [a for a in others if a.quiz_id != attempt.quiz_id]
        prev_percentage = round(sum(a.percentage for a in others) / len(others), 1) if others else 0.0
    progress = student_repository.get_progress(db, user.id, lesson.id)
    return {
        "score": attempt.percentage,
        "time_taken": attempt.time_taken,
        "attempts": attempt.attempt_number,
        "lesson_difficulty": lesson.difficulty,
        "previous_score": prev_percentage,
        "preferred_format": profile.preferred_format if profile else "TEXT",
        "progress": progress.progress_percentage if progress else 0.0,
    }


def generate(db: Session, user: User, lesson: Lesson, attempt: Attempt) -> dict:
    features = build_features(db, user, lesson, attempt)
    result = predict(features)
    resource = lesson_repository.find_resource_by_type(db, lesson.id, result["recommendedFormat"])
    rec = recommendation_repository.create(
        db, user.id, lesson.id, resource.id if resource else None,
        result["recommendedFormat"], result["difficulty"],
        result["confidence"], result["reason"],
    )
    profile = student_repository.get_profile(db, user.id)
    if profile is not None:
        student_repository.update_profile(db, profile, learning_requirement=result["difficulty"])
    return serialize(rec, features=features, source=result.get("source", "ml"))


def serialize(rec: Recommendation, features: dict | None = None,
              source: str | None = None) -> dict:
    from app.ml.explanation import format_label
    return {
        "id": rec.id,
        "student_id": rec.student_id,
        "student_name": rec.student.name if rec.student else None,
        "lesson_id": rec.lesson_id,
        "lesson_title": rec.lesson.title if rec.lesson else None,
        "resource_id": rec.resource_id,
        "recommended_format": rec.recommended_format,
        "recommended_format_label": format_label(rec.recommended_format),
        "difficulty": rec.difficulty,
        "confidence": round(float(rec.confidence), 2),
        "reason": rec.reason,
        "created_at": rec.created_at.isoformat() if rec.created_at else None,
        "target_score": TARGET_SCORE,
        "previous_performance": features.get("previous_score") if features else None,
        "source": source,
    }


def latest_for_student(db: Session, user: User) -> dict | None:
    rec = recommendation_repository.latest_for_student(db, user.id)
    if rec is None:
        return None
    features = None
    if rec.lesson_id:
        attempt = None
        quiz = lesson_repository.get_quiz_for_lesson(db, rec.lesson_id)
        if quiz:
            attempt = attempt_repository.latest_for_quiz(db, user.id, quiz.id)
        if attempt:
            features = build_features(db, user, rec.lesson, attempt)
    return serialize(rec, features=features)


def list_for_student(db: Session, user: User) -> list[dict]:
    return [serialize(r) for r in recommendation_repository.list_for_student(db, user.id)]


def generate_for_latest_attempt(db: Session, user: User, lesson_id: int | None = None) -> dict | None:
    attempts = attempt_repository.list_for_student(db, user.id, limit=5)
    if lesson_id:
        attempts = [a for a in attempts if a.quiz and a.quiz.lesson_id == lesson_id]
    if not attempts:
        return None
    attempt = attempts[0]
    lesson = db.get(Lesson, attempt.quiz.lesson_id)
    if lesson is None:
        return None
    return generate(db, user, lesson, attempt)
