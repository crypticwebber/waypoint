from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.config import REVIEW_PROGRESS_THRESHOLD
from app.database import get_db
from app.services.progress import course_progress_pct

router = APIRouter(prefix="/courses/{course_id}/reviews", tags=["reviews"])


@router.get("", response_model=list[schemas.ReviewOut], summary="List reviews for a course")
def list_reviews(course_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.course_id == course_id).order_by(models.Review.created_at.desc()).all()
    return [
        schemas.ReviewOut(
            id=r.id, user_id=r.user_id, user_name=r.user.full_name,
            rating=r.rating, comment=r.comment, created_at=r.created_at,
        ) for r in reviews
    ]


@router.post(
    "", response_model=schemas.ReviewOut, status_code=201,
    summary="Leave a review",
    description=f"Requires at least {REVIEW_PROGRESS_THRESHOLD}% progress in the course "
                "so reviews come from learners who've actually engaged with the material.",
)
def create_review(course_id: int, payload: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    progress = course_progress_pct(db, current_user.id, course_id)
    if progress < REVIEW_PROGRESS_THRESHOLD:
        raise HTTPException(
            status_code=403,
            detail=f"Complete at least {REVIEW_PROGRESS_THRESHOLD}% of the course before leaving a review",
        )

    existing = db.query(models.Review).filter(
        models.Review.user_id == current_user.id, models.Review.course_id == course_id
    ).first()
    if existing:
        existing.rating = payload.rating
        existing.comment = payload.comment
        db.commit()
        db.refresh(existing)
        review = existing
    else:
        review = models.Review(user_id=current_user.id, course_id=course_id, rating=payload.rating, comment=payload.comment)
        db.add(review)
        db.commit()
        db.refresh(review)

    return schemas.ReviewOut(
        id=review.id, user_id=review.user_id, user_name=current_user.full_name,
        rating=review.rating, comment=review.comment, created_at=review.created_at,
    )
