from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user, require_instructor
from app.database import get_db
from app.services.progress import course_progress_pct
from app.services.serializers import course_card

router = APIRouter(prefix="/instructor", tags=["instructor"])


def _own_course_or_404(db: Session, course_id: int, instructor: models.User) -> models.Course:
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.instructor_id != instructor.id:
        raise HTTPException(status_code=403, detail="You don't own this course")
    return course


@router.get(
    "/courses", response_model=list[schemas.InstructorCourseStats],
    summary="Instructor dashboard: my courses with enrollment, average quiz score, completion rate",
)
def my_courses(db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    courses = db.query(models.Course).filter(models.Course.instructor_id == instructor.id).all()
    out = []
    for course in courses:
        enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == course.id).all()
        enrolled_count = len(enrollments)

        quiz_ids = [q.id for m in course.modules for q in ([m.quiz] if m.quiz else [])]
        avg_score = None
        if quiz_ids:
            avg_score_row = db.query(func.avg(models.QuizAttempt.score)).filter(
                models.QuizAttempt.quiz_id.in_(quiz_ids)
            ).scalar()
            avg_score = round(avg_score_row, 1) if avg_score_row else None

        completed = sum(
            1 for e in enrollments if course_progress_pct(db, e.user_id, course.id) >= 100.0
        )
        completion_rate = round(100.0 * completed / enrolled_count, 1) if enrolled_count else 0.0

        out.append(schemas.InstructorCourseStats(
            course=course_card(db, course), enrolled_count=enrolled_count,
            avg_quiz_score=avg_score, completion_rate=completion_rate,
        ))
    return out


@router.get(
    "/courses/{course_id}/roster", response_model=list[schemas.RosterEntry],
    summary="Per-student roster and progress for a course I teach",
)
def roster(course_id: int, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    course = _own_course_or_404(db, course_id, instructor)
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.course_id == course.id).all()
    return [
        schemas.RosterEntry(
            user_id=e.user_id, full_name=e.user.full_name, email=e.user.email,
            progress_pct=course_progress_pct(db, e.user_id, course.id), enrolled_at=e.enrolled_at,
        ) for e in enrollments
    ]


# ---------- course / module / lesson / quiz CRUD ----------

@router.post("/courses", response_model=schemas.CourseCardOut, status_code=201, summary="Create a course")
def create_course(payload: schemas.CourseCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    course = models.Course(**payload.model_dump(), instructor_id=instructor.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course_card(db, course)


@router.put("/courses/{course_id}", response_model=schemas.CourseCardOut, summary="Edit a course")
def update_course(course_id: int, payload: schemas.CourseCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    course = _own_course_or_404(db, course_id, instructor)
    for field, value in payload.model_dump().items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course_card(db, course)


@router.delete("/courses/{course_id}", status_code=204, summary="Delete a course")
def delete_course(course_id: int, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    course = _own_course_or_404(db, course_id, instructor)
    db.delete(course)
    db.commit()


@router.post("/courses/{course_id}/modules", response_model=schemas.ModuleOut, status_code=201, summary="Add a module")
def create_module(course_id: int, payload: schemas.ModuleCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    _own_course_or_404(db, course_id, instructor)
    module = models.Module(course_id=course_id, **payload.model_dump())
    db.add(module)
    db.commit()
    db.refresh(module)
    return schemas.ModuleOut(id=module.id, title=module.title, description=module.description, order=module.order, lessons=[], quiz=None)


@router.put("/modules/{module_id}", response_model=schemas.ModuleOut, summary="Edit a module")
def update_module(module_id: int, payload: schemas.ModuleCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    _own_course_or_404(db, module.course_id, instructor)
    for field, value in payload.model_dump().items():
        setattr(module, field, value)
    db.commit()
    db.refresh(module)
    return schemas.ModuleOut(
        id=module.id, title=module.title, description=module.description, order=module.order,
        lessons=[schemas.LessonOut.model_validate(l) for l in module.lessons], quiz=None,
    )


@router.delete("/modules/{module_id}", status_code=204, summary="Delete a module")
def delete_module(module_id: int, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    _own_course_or_404(db, module.course_id, instructor)
    db.delete(module)
    db.commit()


@router.post("/modules/{module_id}/lessons", response_model=schemas.LessonOut, status_code=201, summary="Add a lesson")
def create_lesson(module_id: int, payload: schemas.LessonCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    _own_course_or_404(db, module.course_id, instructor)
    lesson = models.Lesson(module_id=module_id, **payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.put("/lessons/{lesson_id}", response_model=schemas.LessonOut, summary="Edit a lesson")
def update_lesson(lesson_id: int, payload: schemas.LessonCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    _own_course_or_404(db, lesson.module.course_id, instructor)
    for field, value in payload.model_dump().items():
        setattr(lesson, field, value)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/lessons/{lesson_id}", status_code=204, summary="Delete a lesson")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    _own_course_or_404(db, lesson.module.course_id, instructor)
    db.delete(lesson)
    db.commit()


@router.post("/modules/{module_id}/quiz", response_model=schemas.QuizOut, status_code=201, summary="Create (or replace) a module's quiz shell")
def create_quiz(module_id: int, title: str, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    _own_course_or_404(db, module.course_id, instructor)
    if module.quiz:
        return schemas.QuizOut(id=module.quiz.id, title=module.quiz.title, questions=[schemas.QuizQuestionAdminOut.model_validate(q) for q in module.quiz.questions])
    quiz = models.Quiz(module_id=module_id, title=title)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return schemas.QuizOut(id=quiz.id, title=quiz.title, questions=[])


@router.post("/quizzes/{quiz_id}/questions", response_model=schemas.QuizQuestionAdminOut, status_code=201, summary="Add a quiz question")
def add_question(quiz_id: int, payload: schemas.QuizQuestionCreate, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    _own_course_or_404(db, quiz.module.course_id, instructor)
    question = models.QuizQuestion(quiz_id=quiz_id, **payload.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.delete("/questions/{question_id}", status_code=204, summary="Delete a quiz question")
def delete_question(question_id: int, db: Session = Depends(get_db), instructor: models.User = Depends(require_instructor)):
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    _own_course_or_404(db, question.quiz.module.course_id, instructor)
    db.delete(question)
    db.commit()
