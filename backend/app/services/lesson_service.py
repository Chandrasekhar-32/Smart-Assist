from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.user import User
from app.repositories import (lesson_repository, recommendation_repository,
                               student_repository)


def subjects(db: Session, user: User | None) -> list[dict]:
    out = []
    for subject in lesson_repository.list_subjects(db):
        lessons = lesson_repository.list_lessons(db, subject.id)
        progress = 0.0
        if user and user.role == "STUDENT" and lessons:
            values = []
            for lesson in lessons:
                row = student_repository.get_progress(db, user.id, lesson.id)
                values.append(row.progress_percentage if row else 0.0)
            progress = round(sum(values) / len(values), 1)
        out.append({"id": subject.id, "name": subject.name,
                    "description": subject.description, "lesson_count": len(lessons),
                    "progress": progress})
    return out


def lessons_for_subject(db: Session, user: User, subject_id: int) -> list[dict]:
    if lesson_repository.get_subject(db, subject_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    out = []
    for lesson in lesson_repository.list_lessons(db, subject_id):
        row = student_repository.get_progress(db, user.id, lesson.id)
        pct = row.progress_percentage if row else 0.0
        completed = bool(row and row.completed)
        out.append({
            "id": lesson.id, "title": lesson.title, "description": lesson.description,
            "difficulty": lesson.difficulty, "progress": pct,
            "status": "Completed" if completed else ("In Progress" if pct > 0 else "Not Started"),
            "subject_id": subject_id,
            "subject_name": lesson.subject.name if lesson.subject else None,
        })
    return out


def lesson_detail(db: Session, user: User, lesson_id: int) -> dict:
    lesson = lesson_repository.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    row = student_repository.get_progress(db, user.id, lesson.id)
    quiz = lesson_repository.get_quiz_for_lesson(db, lesson.id)

    recommended = None
    rec = recommendation_repository.for_lesson(db, user.id, lesson.id)
    if rec:
        from app.services.recommendation_service import serialize
        recommended = serialize(rec)

    return {
        "id": lesson.id, "title": lesson.title, "description": lesson.description,
        "difficulty": lesson.difficulty,
        "subject_id": lesson.subject_id,
        "subject_name": lesson.subject.name if lesson.subject else "",
        "resources": [{"id": r.id, "type": r.type, "title": r.title,
                       "content": r.content, "media_url": r.media_url}
                      for r in lesson.resources],
        "quiz_id": quiz.id if quiz else None,
        "progress": row.progress_percentage if row else 0.0,
        "completed": bool(row and row.completed),
        "recommended_resource": recommended,
    }


def resources(db: Session, user: User, lesson_id: int) -> list[dict]:
    lesson = lesson_repository.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return [{"id": r.id, "type": r.type, "title": r.title,
             "content": r.content, "media_url": r.media_url} for r in lesson.resources]


def mark_viewed(db: Session, user: User, lesson_id: int) -> dict:
    lesson = lesson_repository.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    row = student_repository.set_progress(db, user.id, lesson.id, 15.0)
    return {"lesson_id": lesson_id, "progress": row.progress_percentage}
