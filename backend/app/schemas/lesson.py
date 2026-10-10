from pydantic import BaseModel


class SubjectOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    lesson_count: int = 0
    progress: float = 0.0

    model_config = {"from_attributes": True}


class LessonCard(BaseModel):
    id: int
    title: str
    description: str | None = None
    difficulty: str
    progress: float = 0.0
    status: str = "Not Started"  # Not Started | In Progress | Completed
    subject_id: int
    subject_name: str | None = None

    model_config = {"from_attributes": True}


class ResourceOut(BaseModel):
    id: int
    type: str
    title: str
    content: str | None = None
    media_url: str | None = None

    model_config = {"from_attributes": True}


class LessonDetail(BaseModel):
    id: int
    title: str
    description: str | None = None
    difficulty: str
    subject_id: int
    subject_name: str
    resources: list[ResourceOut] = []
    quiz_id: int | None = None
    progress: float = 0.0
    recommended_resource: dict | None = None

    model_config = {"from_attributes": True}


class QuestionOut(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    model_config = {"from_attributes": True}


class QuizOut(BaseModel):
    id: int
    lesson_id: int
    title: str
    questions: list[QuestionOut] = []

    model_config = {"from_attributes": True}
