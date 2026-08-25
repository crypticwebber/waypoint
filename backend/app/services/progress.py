"""
All "how far along is this user" logic lives here so it's computed exactly
one way, everywhere. Nothing here is a stored/mutable column -- it's derived
fresh from LessonProgress and QuizAttempt rows on every call, which is what
the spec asks for (percent complete is DERIVED, not a manually-set slider).
"""
from sqlalchemy.orm import Session

from app import models
from app.config import QUIZ_PASS_THRESHOLD


def course_lesson_ids(db: Session, course_id: int) -> list[int]:
    return [
        lid for (lid,) in
        db.query(models.Lesson.id)
        .join(models.Module, models.Lesson.module_id == models.Module.id)
        .filter(models.Module.course_id == course_id)
        .all()
    ]


def completed_lesson_ids(db: Session, user_id: int, lesson_ids: list[int]) -> set[int]:
    if not lesson_ids:
        return set()
    rows = (
        db.query(models.LessonProgress.lesson_id)
        .filter(models.LessonProgress.user_id == user_id,
                models.LessonProgress.lesson_id.in_(lesson_ids))
        .all()
    )
    return {r[0] for r in rows}


def course_progress_pct(db: Session, user_id: int, course_id: int) -> float:
    lesson_ids = course_lesson_ids(db, course_id)
    if not lesson_ids:
        return 0.0
    done = completed_lesson_ids(db, user_id, lesson_ids)
    return round(100.0 * len(done) / len(lesson_ids), 1)


def next_incomplete_lesson(db: Session, user_id: int, course_id: int):
    """Return the first lesson (in module/lesson order) the user hasn't completed."""
    lessons = (
        db.query(models.Lesson)
        .join(models.Module, models.Lesson.module_id == models.Module.id)
        .filter(models.Module.course_id == course_id)
        .order_by(models.Module.order, models.Lesson.order)
        .all()
    )
    if not lessons:
        return None
    done = completed_lesson_ids(db, user_id, [l.id for l in lessons])
    for lesson in lessons:
        if lesson.id not in done:
            return lesson
    return lessons[-1]  # everything done -> point at the last lesson


def quiz_best_score(db: Session, user_id: int, quiz_id: int):
    attempts = (
        db.query(models.QuizAttempt)
        .filter(models.QuizAttempt.user_id == user_id, models.QuizAttempt.quiz_id == quiz_id)
        .all()
    )
    if not attempts:
        return None, 0
    return max(a.score for a in attempts), len(attempts)


def all_module_quizzes_passed(db: Session, user_id: int, course_id: int) -> bool:
    modules = db.query(models.Module).filter(models.Module.course_id == course_id).all()
    for module in modules:
        quiz = db.query(models.Quiz).filter(models.Quiz.module_id == module.id).first()
        if not quiz:
            continue  # no quiz on this module -> nothing to pass
        if not quiz.questions:
            continue
        best, _ = quiz_best_score(db, user_id, quiz.id)
        if best is None or best < QUIZ_PASS_THRESHOLD:
            return False
    return True


def maybe_issue_certificate(db: Session, user_id: int, course_id: int):
    """
    Issue a certificate iff: 100% of lessons complete AND every module quiz
    (that has questions) has a best score >= QUIZ_PASS_THRESHOLD.
    Idempotent -- safe to call after every lesson completion / quiz submit.
    """
    existing = (
        db.query(models.Certificate)
        .filter(models.Certificate.user_id == user_id, models.Certificate.course_id == course_id)
        .first()
    )
    if existing:
        return existing

    if course_progress_pct(db, user_id, course_id) < 100.0:
        return None
    if not all_module_quizzes_passed(db, user_id, course_id):
        return None

    cert = models.Certificate(user_id=user_id, course_id=course_id)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert
