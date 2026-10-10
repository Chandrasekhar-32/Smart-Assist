from datetime import datetime

from pydantic import BaseModel


class PredictRequest(BaseModel):
    """Payload sent to the internal ML module (POST /predict shape)."""
    score: float
    timeTaken: int
    attempts: int
    lessonDifficulty: str
    previousScore: float
    preferredFormat: str
    progress: float


class PredictResponse(BaseModel):
    recommendedFormat: str
    difficulty: str
    confidence: float
    reason: str


class RecommendationOut(BaseModel):
    id: int
    student_id: int
    lesson_id: int | None = None
    lesson_title: str | None = None
    recommended_format: str
    difficulty: str
    confidence: float
    reason: str
    created_at: datetime | None = None
    resource_id: int | None = None

    model_config = {"from_attributes": True}


class GenerateRequest(BaseModel):
    lesson_id: int | None = None
