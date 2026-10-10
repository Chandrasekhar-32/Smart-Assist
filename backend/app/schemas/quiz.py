from pydantic import BaseModel


class AnswerIn(BaseModel):
    question_id: int
    answer: str  # A | B | C | D


class QuizSubmitRequest(BaseModel):
    answers: list[AnswerIn]
    time_taken: int = 0  # seconds


class QuizResult(BaseModel):
    attempt_id: int
    quiz_id: int
    lesson_id: int
    score: int
    total: int
    percentage: float
    time_taken: int
    attempt_number: int
    performance: str
    improved: bool
    previous_percentage: float | None = None
    recommendation: dict | None = None
