from sqlalchemy.orm import Session, joinedload

from app.models.lesson import Lesson
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.resource import Resource
from app.models.subject import Subject


def list_subjects(db: Session) -> list[Subject]:
    return db.query(Subject).order_by(Subject.id).all()


def get_subject(db: Session, subject_id: int) -> Subject | None:
    return db.query(Subject).options(joinedload(Subject.lessons)).filter(Subject.id == subject_id).first()


def list_lessons(db: Session, subject_id: int) -> list[Lesson]:
    return db.query(Lesson).filter(Lesson.subject_id == subject_id).order_by(Lesson.position).all()


def list_all_lessons(db: Session) -> list[Lesson]:
    return db.query(Lesson).order_by(Lesson.subject_id, Lesson.position).all()


def get_lesson(db: Session, lesson_id: int) -> Lesson | None:
    return db.query(Lesson).options(joinedload(Lesson.subject), joinedload(Lesson.resources)) \
        .filter(Lesson.id == lesson_id).first()


def get_resources(db: Session, lesson_id: int) -> list[Resource]:
    return db.query(Resource).filter(Resource.lesson_id == lesson_id).all()


def find_resource_by_type(db: Session, lesson_id: int, resource_type: str) -> Resource | None:
    return db.query(Resource).filter(Resource.lesson_id == lesson_id,
                                     Resource.type == resource_type).first()


def get_quiz_for_lesson(db: Session, lesson_id: int) -> Quiz | None:
    return db.query(Quiz).options(joinedload(Quiz.questions)) \
        .filter(Quiz.lesson_id == lesson_id).first()


def get_quiz(db: Session, quiz_id: int) -> Quiz | None:
    return db.query(Quiz).options(joinedload(Quiz.questions)) \
        .filter(Quiz.id == quiz_id).first()


def get_question(db: Session, question_id: int) -> Question | None:
    return db.get(Question, question_id)
