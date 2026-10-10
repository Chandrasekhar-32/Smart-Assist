from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_student
from app.database.connection import get_db
from app.ml.predictor import predict
from app.models.user import User
from app.repositories import recommendation_repository
from app.schemas.recommendation import GenerateRequest, PredictRequest
from app.services import recommendation_service

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/recommendations")
def list_recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return recommendation_service.list_for_student(db, user)


@router.post("/recommendations/generate")
def generate_recommendation(payload: GenerateRequest | None = None,
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    require_student(user)
    rec = recommendation_service.generate_for_latest_attempt(
        db, user, payload.lesson_id if payload else None)
    if rec is None:
        raise HTTPException(status_code=400, detail="No quiz attempts found yet")
    return rec


@router.get("/recommendations/latest")
def latest_recommendation(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_student(user)
    return recommendation_service.latest_for_student(db, user)


@router.post("/predict")
def predict_endpoint(payload: PredictRequest, user: User = Depends(get_current_user)):
    """Direct access to the internal ML module (spec section 15)."""
    return predict(payload.model_dump())
