from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.student_progress import StudentProgress
from app.models.subject import Subject


def subject_progress(db: Session, student_id: int) -> list[dict]:
    """Average progress % per subject for a student."""
    rows = (db.query(Subject, Lesson, StudentProgress)
            .join(Lesson, Lesson.subject_id == Subject.id)
            .outerjoin(StudentProgress,
                       (StudentProgress.lesson_id == Lesson.id) & (StudentProgress.student_id == student_id))
            .all())
    bucket: dict[str, list[float]] = {}
    for subject, _lesson, prog in rows:
        bucket.setdefault(subject.name, []).append(prog.progress_percentage if prog else 0.0)
    return [{"subject": name, "progress": round(sum(v) / len(v), 1)}
            for name, v in bucket.items()]


def completed_count(db: Session, student_id: int) -> int:
    return db.query(StudentProgress).filter(StudentProgress.student_id == student_id,
                                            StudentProgress.completed.is_(True)).count()


def total_lessons(db: Session) -> int:
    return db.query(Lesson).count()


def quiz_attempts(db: Session, student_id: int) -> int:
    return db.query(Attempt).filter(Attempt.student_id == student_id).count()
