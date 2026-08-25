from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from app.services.progress import course_progress_pct, next_incomplete_lesson
from app.services.serializers import course_card

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=schemas.DashboardStats, summary="At-a-glance learner stats")
def stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.user_id == current_user.id).all()
    completed = sum(1 for e in enrollments if course_progress_pct(db, current_user.id, e.course_id) >= 100.0)
    lessons_completed = db.query(func.count(models.LessonProgress.id)).filter(
        models.LessonProgress.user_id == current_user.id
    ).scalar() or 0
    certs = db.query(func.count(models.Certificate.id)).filter(
        models.Certificate.user_id == current_user.id
    ).scalar() or 0

    avg_score_row = db.query(func.avg(models.QuizAttempt.score)).filter(
        models.QuizAttempt.user_id == current_user.id
    ).scalar()

    return schemas.DashboardStats(
        courses_enrolled=len(enrollments),
        courses_completed=completed,
        lessons_completed=lessons_completed,
        certificates_earned=certs,
        avg_quiz_score=round(avg_score_row, 1) if avg_score_row else None,
    )


@router.get(
    "/continue-learning", response_model=list[schemas.ContinueLearningItem],
    summary="Courses in progress, resumable at the next incomplete lesson",
)
def continue_learning(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    enrollments = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.user_id == current_user.id)
        .order_by(models.Enrollment.last_accessed.desc())
        .all()
    )
    items = []
    for e in enrollments:
        pct = course_progress_pct(db, current_user.id, e.course_id)
        if pct >= 100.0:
            continue
        lesson = next_incomplete_lesson(db, current_user.id, e.course_id)
        items.append(schemas.ContinueLearningItem(
            course=course_card(db, e.course),
            next_lesson=schemas.LessonOut.model_validate(lesson) if lesson else None,
            progress_pct=pct,
        ))
    return items


@router.get(
    "/completed", response_model=list[schemas.CourseCardOut],
    summary="Courses this user has finished",
)
def completed_courses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.user_id == current_user.id).all()
    done = [e.course for e in enrollments if course_progress_pct(db, current_user.id, e.course_id) >= 100.0]
    return [course_card(db, c) for c in done]
