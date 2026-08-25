from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from app.services.recommender import RecommendationEngine
from app.services.serializers import course_card

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get(
    "/me", response_model=list[schemas.RecommendationOut],
    summary="Get personalized course recommendations",
    description="Blends the onboarding survey (category interest, skill level, free-text "
                "TF-IDF similarity) with behavioral content-based similarity from enrolled "
                "courses, weighted by how much history the user has. A brand-new user gets "
                "100% onboarding-driven picks; the blend shifts towards behavior as they "
                "engage with the platform, capped so onboarding preferences never fully "
                "disappear. See app/services/recommender.py for the full algorithm.",
)
def get_recommendations(
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    courses = db.query(models.Course).all()
    engine = RecommendationEngine(courses)

    enrollments = db.query(models.Enrollment).filter(models.Enrollment.user_id == current_user.id).all()
    enrolled_ids = {e.course_id for e in enrollments}

    scored = engine.recommend(db, current_user, current_user.preferences, enrolled_ids, limit=limit)

    return [
        schemas.RecommendationOut(
            course=course_card(db, s.course), reason=s.reason, score=s.score, source=s.source,
        ) for s in scored
    ]
