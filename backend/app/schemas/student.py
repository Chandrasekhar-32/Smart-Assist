from pydantic import BaseModel, Field


class ProfileOut(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    age: int | None = None
    preferred_format: str
    learning_requirement: str | None = None

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    preferred_format: str | None = None
    learning_requirement: str | None = None


class StatCard(BaseModel):
    label: str
    value: str


class RecentQuiz(BaseModel):
    lesson: str
    percentage: float
    attempts: int
    created_at: str | None = None


class DashboardOut(BaseModel):
    welcome_name: str
    lessons_completed: int
    total_lessons: int
    average_score: float
    progress: float
    quiz_attempts: int
    improvement: float
    continue_learning: dict | None = None
    recommendation: dict | None = None
    recent_performance: list[RecentQuiz] = []
    subject_progress: list[dict] = []
