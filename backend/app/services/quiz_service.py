from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.quiz import Quiz
from app.models.user import User
from app.repositories import attempt_repository, lesson_repository, student_repository
from app.schemas.quiz import QuizSubmitRequest
from app.services import recommendation_service


def performance_label(percentage: float) -> str:
    if percentage >= 80:
        return "Good"
    if percentage >= 60:
        return "Average"
    if percentage >= 50:
        return "Below Average"
    return "Needs Practice"


def get_quiz(db: Session, quiz_id: int) -> Quiz:
    quiz = lesson_repository.get_quiz(db, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    return quiz


def quiz_payload(quiz: Quiz) -> dict:
    return {
        "id": quiz.id,
        "lesson_id": quiz.lesson_id,
        "title": quiz.title,
        # correct answers are never sent to the client
        "questions": [{"id": q.id, "question": q.question, "option_a": q.option_a,
                       "option_b": q.option_b, "option_c": q.option_c,
                       "option_d": q.option_d} for q in quiz.questions],
    }


def submit(db: Session, user: User, quiz_id: int, payload: QuizSubmitRequest) -> dict:
    quiz = get_quiz(db, quiz_id)
    questions = quiz.questions
    if not questions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz has no questions")

    answers = {a.question_id: (a.answer or "").upper()[:1] for a in payload.answers}
    score = 0
    for q in questions:
        if answers.get(q.id) == q.correct_answer:
            score += 1
    total = len(questions)
    percentage = round(score / total * 100, 1)

    previous = attempt_repository.latest_for_quiz(db, user.id, quiz.id)
    previous_percentage = previous.percentage if previous else None
    attempt_number = attempt_repository.count_for_quiz(db, user.id, quiz.id) + 1

    attempt = attempt_repository.create(db, user.id, quiz.id, score, percentage,
                                        int(payload.time_taken or 0), attempt_number)

    # progress: >=70% completes the lesson, otherwise record the reached level
    lesson = quiz.lesson if quiz else None
    if lesson:
        if percentage >= 70:
            student_repository.set_progress(db, user.id, lesson.id, 100.0, completed=True)
        else:
            student_repository.set_progress(db, user.id, lesson.id, percentage, completed=False)

    recommendation = None
    if lesson:
        recommendation = recommendation_service.generate(db, user, lesson, attempt)

    return {
        "attempt_id": attempt.id,
        "quiz_id": quiz.id,
        "lesson_id": quiz.lesson_id,
        "score": score,
        "total": total,
        "percentage": percentage,
        "time_taken": attempt.time_taken,
        "attempt_number": attempt_number,
        "performance": performance_label(percentage),
        "improved": previous_percentage is not None and percentage > previous_percentage,
        "previous_percentage": previous_percentage,
        "recommendation": recommendation,
    }
