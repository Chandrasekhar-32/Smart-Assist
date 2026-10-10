from pydantic import BaseModel


class StudentRow(BaseModel):
    id: int
    name: str
    email: str
    avg_score: float
    progress: float
    attempts: int
    status: str  # Good | Needs Support


class TeacherDashboard(BaseModel):
    total_students: int
    average_score: float
    needing_support: int
    recommendations_generated: int
    students: list[StudentRow] = []


class StudentDetails(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None
    preferred_format: str
    overall_score: float
    progress: float
    attempts: int
    avg_time_minutes: float
    recent_performance: list[dict] = []
    current_recommendation: dict | None = None
    history: list[dict] = []
