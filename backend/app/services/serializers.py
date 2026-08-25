"""Shared helpers for turning ORM objects into API schemas with derived fields
(avg rating, enrolled count, per-user progress) that don't live on the model."""
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.services.progress import (
    course_progress_pct, completed_lesson_ids, course_lesson_ids, quiz_best_score,
)


def course_card(db: Session, course: models.Course) -> schemas.CourseCardOut:
    rating_row = (
        db.query(func.avg(models.Review.rating), func.count(models.Review.id))
        .filter(models.Review.course_id == course.id)
        .first()
    )
    avg_rating, review_count = rating_row
    enrolled_count = db.query(func.count(models.Enrollment.id)).filter(
        models.Enrollment.course_id == course.id
    ).scalar()

    return schemas.CourseCardOut(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        tags=course.tags or [],
        level=course.level,
        duration_hours=course.duration_hours,
        color=course.color,
        instructor_name=course.instructor.full_name if course.instructor else "",
        avg_rating=round(avg_rating, 2) if avg_rating else None,
        review_count=review_count or 0,
        enrolled_count=enrolled_count or 0,
    )


def course_detail(db: Session, course: models.Course, user: models.User | None) -> schemas.CourseDetailOut:
    card = course_card(db, course)

    lesson_ids = course_lesson_ids(db, course.id)
    done_ids = completed_lesson_ids(db, user.id, lesson_ids) if user else set()

    modules_out = []
    for module in course.modules:
        lessons_out = [schemas.LessonOut.model_validate(l) for l in module.lessons]
        completed_count = sum(1 for l in module.lessons if l.id in done_ids)

        quiz_out = None
        if module.quiz:
            best, attempt_count = (None, 0)
            if user:
                best, attempt_count = quiz_best_score(db, user.id, module.quiz.id)
            quiz_out = schemas.QuizOut(
                id=module.quiz.id,
                title=module.quiz.title,
                questions=[schemas.QuizQuestionOut.model_validate(q) for q in module.quiz.questions],
                best_score=best,
                attempt_count=attempt_count,
            )

        modules_out.append(schemas.ModuleOut(
            id=module.id, title=module.title, description=module.description,
            order=module.order, lessons=lessons_out, quiz=quiz_out,
            completed_lessons=completed_count,
        ))

    is_enrolled = False
    progress_pct = 0.0
    if user:
        enrollment = db.query(models.Enrollment).filter(
            models.Enrollment.user_id == user.id, models.Enrollment.course_id == course.id
        ).first()
        is_enrolled = enrollment is not None
        if is_enrolled:
            progress_pct = course_progress_pct(db, user.id, course.id)

    return schemas.CourseDetailOut(
        **card.model_dump(),
        project_brief=course.project_brief,
        modules=modules_out,
        is_enrolled=is_enrolled,
        progress_pct=progress_pct,
    )
