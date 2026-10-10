"""Database initialisation and demo seed (phase 2 of the project plan).

Creates tables, inserts 3 subjects / 15 lessons / resources / quizzes /
questions, demo users, sample performance data and ML recommendations.
"""
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.base import Base
from app.database.connection import engine, SessionLocal
from app.ml.train import train as train_model
from app.models import (Attempt, Question, Quiz, Recommendation, Resource,
                        StudentProgress, Subject, User)
from app.models.lesson import Lesson
from app.repositories import attempt_repository, student_repository, user_repository
from app.services import recommendation_service
from app.seed_content import SUBJECTS as MATH_EN
from app.seed_content_cs import SUBJECTS as CS

CONTENT = MATH_EN + CS

DEMO_STUDENTS = [
    # name, email, age, preferred_format, performance rows: (lesson, pct, minutes, attempts)
    ("Chandrasekhar", "student@smartassist.edu", 21, "TEXT",
     [("Binary Numbers", 40, 15, 3), ("Data Structures", 62, 11, 2),
      ("Parts of Speech", 82, 6, 1), ("Algebra Basics", 58, 12, 2)]),
    ("Rahul", "rahul@smartassist.edu", 20, "VISUAL",
     [("Binary Numbers", 85, 5, 1), ("Algebra Basics", 78, 7, 1),
      ("Fractions and Decimals", 74, 8, 1)]),
    ("Priya", "priya@smartassist.edu", 22, "AUDIO",
     [("Tenses", 71, 9, 1), ("Fractions and Decimals", 68, 8, 2),
      ("Vocabulary Building", 80, 6, 1)]),
    ("Arun", "arun@smartassist.edu", 20, "SIMPLIFIED_TEXT",
     [("Linear Equations", 45, 14, 3), ("Programming Loops", 52, 13, 2),
      ("Database Basics", 40, 16, 3), ("Tenses", 66, 10, 2)]),
]


def init_db():
    Base.metadata.create_all(bind=engine)


def _seed_content(db: Session):
    for subject_data in CONTENT:
        subject = Subject(name=subject_data["name"], description=subject_data["description"])
        db.add(subject)
        db.flush()
        for position, lesson_data in enumerate(subject_data["lessons"], start=1):
            lesson = Lesson(subject_id=subject.id, title=lesson_data["title"],
                            description=lesson_data["description"],
                            difficulty=lesson_data["difficulty"], position=position)
            db.add(lesson)
            db.flush()
            for rtype, title, content in lesson_data["resources"]:
                db.add(Resource(lesson_id=lesson.id, type=rtype, title=title, content=content))
            quiz = Quiz(lesson_id=lesson.id, title=f"{lesson.title} Quiz")
            db.add(quiz)
            db.flush()
            for question, a, b, c, d, correct in lesson_data["questions"]:
                db.add(Question(quiz_id=quiz.id, question=question, option_a=a,
                                option_b=b, option_c=c, option_d=d, correct_answer=correct))
    db.commit()


def _seed_users(db: Session):
    if user_repository.get_by_email(db, "teacher@smartassist.edu") is None:
        user_repository.create(db, "Dr. Meena Sharma", "teacher@smartassist.edu",
                               hash_password("teacher123"), "TEACHER")
    for name, email, age, pref, _rows in DEMO_STUDENTS:
        if user_repository.get_by_email(db, email) is None:
            user = user_repository.create(db, name, email, hash_password("student123"), "STUDENT")
            student_repository.create_profile(db, user.id, age, pref)


def _seed_performance(db: Session):
    """Create attempts, progress and ML recommendations for the demo students."""
    from app.models.quiz import Quiz
    from app.models.lesson import Lesson as LessonModel

    for _name, email, _age, _pref, rows in DEMO_STUDENTS:
        student = user_repository.get_by_email(db, email)
        if student is None:
            continue
        has_attempts = attempt_repository.list_for_student(db, student.id, limit=1)
        if has_attempts:
            continue
        for title, percentage, minutes, attempts in rows:
            lesson = db.query(LessonModel).filter(LessonModel.title == title).first()
            if lesson is None:
                continue
            quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson.id).first()
            total = db.query(Question).filter_by(quiz_id=quiz.id).count()
            # simulate the attempt history: first attempt low, improving to `percentage`
            first = max(20, percentage - 20 * (attempts - 1))
            step = (percentage - first) / max(1, attempts - 1) if attempts > 1 else 0
            for i in range(attempts):
                pct = round(first + step * i, 1) if attempts > 1 else percentage
                score = max(0, min(total, round(pct / 100 * total)))
                att = attempt_repository.create(db, student.id, quiz.id, score,
                                                round(score / total * 100, 1),
                                                minutes * 60, i + 1)
                pct_final = att.percentage
                if pct_final >= 70:
                    student_repository.set_progress(db, student.id, lesson.id, 100.0, completed=True)
                else:
                    student_repository.set_progress(db, student.id, lesson.id, pct_final)
            # a couple of lessons opened but not quizzed yet
            recommendation_service.generate_for_latest_attempt(db, student, lesson.id)
        # mark one extra lesson as opened (progress 15%)
        from app.repositories import lesson_repository
        for lesson in lesson_repository.list_all_lessons(db):
            prog = student_repository.get_progress(db, student.id, lesson.id)
            if prog is None:
                student_repository.set_progress(db, student.id, lesson.id, 15.0)
                break


def seed_if_empty():
    db: Session = SessionLocal()
    try:
        subjects = db.query(Subject).count()
        if subjects == 0:
            _seed_content(db)
        _seed_users(db)
        db.commit()
        _seed_performance(db)
    finally:
        db.close()


def bootstrap():
    """Full startup: tables -> model (train if missing) -> seed."""
    init_db()
    from app.ml.predictor import load_model
    if load_model() is None:
        train_model()
    seed_if_empty()
