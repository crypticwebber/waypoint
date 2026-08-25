from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from app.services.progress import maybe_issue_certificate

router = APIRouter(tags=["learning"])


@router.post(
    "/courses/{course_id}/enroll", response_model=schemas.EnrollmentOut, status_code=201,
    summary="Enroll in a course",
)
def enroll(course_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == current_user.id, models.Enrollment.course_id == course_id
    ).first()
    if existing:
        return existing

    enrollment = models.Enrollment(user_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.post(
    "/lessons/{lesson_id}/complete", response_model=schemas.CertificateOut | None,
    summary="Mark a lesson complete",
    description="Idempotent. Also checks certificate eligibility (100% lessons + all "
                "module quizzes passed) and auto-issues a certificate if the course just "
                "became complete, returning it if so (null otherwise).",
)
def complete_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    existing = db.query(models.LessonProgress).filter(
        models.LessonProgress.user_id == current_user.id, models.LessonProgress.lesson_id == lesson_id
    ).first()
    if not existing:
        db.add(models.LessonProgress(user_id=current_user.id, lesson_id=lesson_id))
        db.commit()

    module = lesson.module
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == current_user.id, models.Enrollment.course_id == module.course_id
    ).first()
    if enrollment:
        enrollment.last_accessed = datetime.utcnow()
        db.commit()

    cert = maybe_issue_certificate(db, current_user.id, module.course_id)
    if cert:
        return schemas.CertificateOut(
            id=cert.id, course_id=cert.course_id, course_title=module.course.title,
            issued_at=cert.issued_at, certificate_code=cert.certificate_code,
        )
    return None


@router.post(
    "/quizzes/{quiz_id}/attempts", response_model=schemas.QuizAttemptOut, status_code=201,
    summary="Submit a quiz attempt",
    description="Scores immediately and stores the attempt (retakes are always allowed; "
                "the best score across all attempts is what counts towards a certificate).",
)
def submit_quiz(quiz_id: int, payload: schemas.QuizSubmission, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if len(payload.answers) != len(quiz.questions):
        raise HTTPException(status_code=400, detail=f"Expected {len(quiz.questions)} answers, got {len(payload.answers)}")

    correct = sum(
        1 for q, given in zip(quiz.questions, payload.answers) if given == q.correct_index
    )
    score = round(100.0 * correct / len(quiz.questions), 1) if quiz.questions else 0.0

    attempt = models.QuizAttempt(user_id=current_user.id, quiz_id=quiz_id, score=score, answers=payload.answers)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # A passed quiz can also complete certificate eligibility.
    maybe_issue_certificate(db, current_user.id, quiz.module.course_id)

    return attempt


@router.get(
    "/quizzes/{quiz_id}/attempts", response_model=list[schemas.QuizAttemptOut],
    summary="Get this user's attempt history for a quiz, most recent first",
)
def quiz_attempt_history(quiz_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.QuizAttempt)
        .filter(models.QuizAttempt.user_id == current_user.id, models.QuizAttempt.quiz_id == quiz_id)
        .order_by(models.QuizAttempt.taken_at.desc())
        .all()
    )
