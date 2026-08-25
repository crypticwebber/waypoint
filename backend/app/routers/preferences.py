from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/preferences", tags=["onboarding"])


@router.put(
    "/me", response_model=schemas.PreferencesOut,
    summary="Save onboarding survey answers",
    description="Upserts the current user's interests / skill level / goal / free-text "
                "answer. This is the cold-start signal the recommendation engine uses "
                "before the user has any enrollment history.",
)
def upsert_preferences(
    payload: schemas.PreferencesIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    prefs = current_user.preferences
    if prefs is None:
        prefs = models.UserPreferences(user_id=current_user.id)
        db.add(prefs)

    prefs.interests = payload.interests
    prefs.skill_level = payload.skill_level
    prefs.goal = payload.goal
    prefs.free_text_interest = payload.free_text_interest
    db.commit()
    db.refresh(prefs)
    return prefs


@router.get(
    "/me", response_model=schemas.PreferencesOut,
    summary="Get the current user's onboarding answers",
)
def get_preferences(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    prefs = current_user.preferences
    if prefs is None:
        return schemas.PreferencesOut(interests=[], skill_level=None, goal=None, free_text_interest=None)
    return prefs
