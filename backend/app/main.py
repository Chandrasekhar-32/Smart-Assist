"""SmartAssist API - adaptive learning platform (FastAPI + ML module)."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS
from app.routes import (attempt, auth, lesson, progress, quiz,
                        recommendation, student, subject, teacher)
from app.core.security import get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.seed import bootstrap
    bootstrap()  # create tables, train model if missing, seed demo data
    yield


app = FastAPI(
    title="SmartAssist API",
    description="AI-driven multimodal and personalized adaptive learning platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (auth.router, student.router, subject.router, lesson.router,
               quiz.router, attempt.router, recommendation.router,
               progress.router, teacher.router):
    app.include_router(router)

# spec section 15: POST /predict (alias of /api/predict)
app.add_api_route("/predict", recommendation.predict_endpoint,
                  methods=["POST"], tags=["ml"],
                  dependencies=[Depends(get_current_user)])


@app.get("/")
def root():
    return {"name": "SmartAssist API", "status": "running", "docs": "/docs"}
