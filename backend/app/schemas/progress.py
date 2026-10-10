from pydantic import BaseModel


class SubjectProgress(BaseModel):
    subject: str
    progress: float


class ProgressOut(BaseModel):
    overall_progress: float
    average_score: float
    lessons_completed: int
    total_lessons: int
    quiz_attempts: int
    improvement: float
    subject_progress: list[SubjectProgress] = []
    recent_quizzes: list[dict] = []
