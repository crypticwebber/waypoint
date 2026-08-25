from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from app.services.serializers import course_card, course_detail

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "", response_model=list[schemas.CourseCardOut],
    summary="Browse the course catalog",
    description="Supports free-text search across title/tags/description, category and "
                "level filters, and page/page_size pagination.",
)
def list_courses(
    q: Optional[str] = Query(None, description="Search title, description and tags"),
    category: Optional[str] = None,
    level: Optional[models.SkillLevel] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(models.Course)
    if category:
        query = query.filter(models.Course.category == category)
    if level:
        query = query.filter(models.Course.level == level)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            models.Course.title.ilike(like),
            models.Course.description.ilike(like),
        ))
    courses = query.order_by(models.Course.created_at.desc()).all()

    if q:
        # tags are JSON, filter in Python since SQLite JSON `LIKE` is unreliable
        like_lower = q.lower()
        courses = [c for c in courses if like_lower in c.title.lower()
                   or like_lower in c.description.lower()
                   or any(like_lower in t.lower() for t in (c.tags or []))]

    start = (page - 1) * page_size
    page_items = courses[start:start + page_size]
    return [course_card(db, c) for c in page_items]


@router.get(
    "/categories", response_model=list[str],
    summary="List all distinct course categories",
)
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(models.Course.category).distinct().all()
    return sorted({r[0] for r in rows})


@router.get(
    "/{course_id}", response_model=schemas.CourseDetailOut,
    summary="Get full course detail: syllabus, quizzes, and this user's progress",
)
def get_course(course_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_detail(db, course, current_user)
