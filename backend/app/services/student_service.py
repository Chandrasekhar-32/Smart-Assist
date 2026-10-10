from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.quiz import Quiz
from app.models.user import User
from app.repositories import (attempt_repository, lesson_repository,
                               progress_repository, recommendation_repository,
                               student_repository, user_repository)
from app.schemas.student import ProfileUpdate
from app.services import recommendation_service


def profile_dict(db: Session, user: User) -> dict:
    profile = student_repository.get_profile(db, user.id)
    return {
        "id": profile.id if profile else 0,
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "age": profile.age if profile else None,
        "preferred_format": profile.preferred_format if profile else "TEXT",
        "learning_requirement": profile.learning_requirement if profile else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def update_profile(db: Session, user: User, payload: ProfileUpdate) -> dict:
    if payload.name:
        user.name = payload.name
        db.commit()
    profile = student_repository.get_profile(db, user.id)
    if profile is None:
        profile = student_repository.create_profile(
            db, user.id, payload.age, (payload.preferred_format or "TEXT").upper())
    else:
        student_repository.update_profile(
            db, profile,
            age=payload.age,
            preferred_format=payload.preferred_format.upper() if payload.preferred_format else None,
            learning_requirement=payload.learning_requirement.upper() if payload.learning_requirement else None,
        )
    return profile_dict(db, user)


def _student_stats(db: Session, user: User) -> dict:
    attempts = attempt_repository.list_for_student(db, user.id, limit=200)
    avg_score = round(sum(a.percentage for a in attempts) / len(attempts), 1) if attempts else 0.0
    subj = progress_repository.subject_progress(db, user.id)
    overall = round(sum(s["progress"] for s in subj) / len(subj), 1) if subj else 0.0
    completed = progress_repository.completed_count(db, user.id)
    total = progress_repository.total_lessons(db)

    # improvement: average gain of latest attempt over first attempt per quiz
    gains = []
    quiz_ids = {a.quiz_id for a in attempts}
    for qid in quiz_ids:
        history = attempt_repository.list_for_quiz(db, user.id, qid)
        if len(history) >= 2:
            gains.append(history[-1].percentage - history[0].percentage)
    improvement = round(sum(gains) / len(gains), 1) if gains else 0.0
    return {
        "attempts": attempts,
        "average_score": avg_score,
        "overall_progress": overall,
        "completed": completed,
        "total_lessons": total,
        "quiz_attempts": len(attempts),
        "improvement": improvement,
        "subject_progress": subj,
    }


def dashboard(db: Session, user: User) -> dict:
    stats = _student_stats(db, user)

    # continue learning: most recently updated in-progress lesson
    rows = student_repository.all_progress(db, user.id)
    rows = [r for r in rows if not r.completed and r.progress_percentage > 0]
    continue_learning = None
    if rows:
        row = sorted(rows, key=lambda r: r.updated_at or r.id, reverse=True)[0]
        lesson = lesson_repository.get_lesson(db, row.lesson_id)
        if lesson:
            continue_learning = {
                "id": lesson.id, "title": lesson.title,
                "subject": lesson.subject.name if lesson.subject else "",
                "progress": row.progress_percentage,
            }
    if continue_learning is None:
        lesson = lesson_repository.list_all_lessons(db)[0]
        continue_learning = {"id": lesson.id, "title": lesson.title,
                             "subject": lesson.subject.name if lesson.subject else "",
                             "progress": 0.0}

    recent = []
    for a in stats["attempts"][:5]:
        title = a.quiz.lesson.title if a.quiz and a.quiz.lesson else "Quiz"
        n = attempt_repository.count_for_quiz(db, user.id, a.quiz_id)
        recent.append({"lesson": title, "percentage": a.percentage, "attempts": n,
                       "created_at": a.created_at.isoformat() if a.created_at else None})

    return {
        "welcome_name": user.name.split(" ")[0],
        "lessons_completed": stats["completed"],
        "total_lessons": stats["total_lessons"],
        "average_score": stats["average_score"],
        "progress": stats["overall_progress"],
        "quiz_attempts": stats["quiz_attempts"],
        "improvement": stats["improvement"],
        "continue_learning": continue_learning,
        "recommendation": recommendation_service.latest_for_student(db, user),
        "recent_performance": recent,
        "subject_progress": stats["subject_progress"],
    }


def my_lessons(db: Session, user: User) -> list[dict]:
    out = []
    for lesson in lesson_repository.list_all_lessons(db):
        prog = student_repository.get_progress(db, user.id, lesson.id)
        pct = prog.progress_percentage if prog else 0.0
        out.append({
            "id": lesson.id, "title": lesson.title, "description": lesson.description,
            "difficulty": lesson.difficulty, "progress": pct,
            "completed": bool(prog and prog.completed),
            "status": "Completed" if (prog and prog.completed) else ("In Progress" if pct > 0 else "Not Started"),
            "subject_id": lesson.subject_id,
            "subject_name": lesson.subject.name if lesson.subject else None,
        })
    return out


# ---------------- Teacher views (section 19-20) ----------------

def _student_row(db: Session, student: User) -> dict:
    stats = _student_stats(db, student)
    avg, prog = stats["average_score"], stats["overall_progress"]
    if avg < 50 or (prog < 40 and avg < 60):
        status = "Needs Support"
    elif avg < 65:
        status = "Average"
    else:
        status = "Good"
    return {"id": student.id, "name": student.name, "email": student.email,
            "avg_score": avg, "progress": prog, "attempts": stats["quiz_attempts"],
            "status": status}


def teacher_dashboard(db: Session) -> dict:
    students = user_repository.list_students(db)
    rows = [_student_row(db, s) for s in students]
    total = len(rows)
    avg_score = round(sum(r["avg_score"] for r in rows) / total, 1) if total else 0.0
    support = sum(1 for r in rows if r["status"] == "Needs Support")
    from app.repositories import recommendation_repository
    return {
        "total_students": total,
        "average_score": avg_score,
        "needing_support": support,
        "recommendations_generated": recommendation_repository.count_all(db),
        "students": rows,
    }


def teacher_student_details(db: Session, student_id: int) -> dict | None:
    student = user_repository.get(db, student_id)
    if student is None or student.role != "STUDENT":
        return None
    stats = _student_stats(db, student)
    profile = student_repository.get_profile(db, student.id)
    times = [a.time_taken for a in stats["attempts"]]
    avg_time = round((sum(times) / len(times)) / 60, 1) if times else 0.0

    recent = []
    for a in stats["attempts"][:8]:
        n = attempt_repository.count_for_quiz(db, student.id, a.quiz_id)
        recent.append({"lesson": a.quiz.lesson.title if a.quiz and a.quiz.lesson else "Quiz",
                       "percentage": a.percentage, "attempts": n,
                       "created_at": a.created_at.isoformat() if a.created_at else None})

    rec = recommendation_repository.latest_for_student(db, student.id)
    current_rec = recommendation_service.serialize(rec) if rec else None
    history = [recommendation_service.serialize(r)
               for r in recommendation_repository.list_for_student(db, student.id, limit=10)]

    return {
        "id": student.id, "name": student.name, "email": student.email,
        "age": profile.age if profile else None,
        "preferred_format": profile.preferred_format if profile else "TEXT",
        "overall_score": stats["average_score"],
        "progress": stats["overall_progress"],
        "attempts": stats["quiz_attempts"],
        "avg_time_minutes": avg_time,
        "recent_performance": recent,
        "current_recommendation": current_rec,
        "history": history,
    }
