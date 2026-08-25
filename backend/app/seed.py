"""
Idempotent seed script.

Run with: python -m app.seed

Safe to re-run: it checks for existing data by natural key (course title,
user email) before inserting, so running it twice never creates duplicates.
It also fabricates some realistic demo activity (enrollments, completed
lessons, quiz attempts, reviews) for one demo student, specifically so the
recommendation engine has something to blend against out of the box --
useful for a live demo/viva without needing to manually click through the
whole app first.
"""
import random
from datetime import datetime, timedelta

from app.database import Base, engine, SessionLocal
from app import models
from app.auth import hash_password
from app.seed_data import (
    course_python_data, course_ml, course_react, course_fastapi, course_devops, course_ux,
)

ALL_COURSES = [
    course_python_data.COURSE,
    course_ml.COURSE,
    course_react.COURSE,
    course_fastapi.COURSE,
    course_devops.COURSE,
    course_ux.COURSE,
]

INSTRUCTORS = [
    {"email": "priya.shah@waypoint.dev", "full_name": "Priya Shah", "courses": ["Python for Data Analysis", "Machine Learning Foundations"]},
    {"email": "marcus.lee@waypoint.dev", "full_name": "Marcus Lee", "courses": ["Full-Stack Web Development with React", "Modern Backend APIs with FastAPI"]},
    {"email": "jonas.weber@waypoint.dev", "full_name": "Jonas Weber", "courses": ["Cloud & DevOps Essentials"]},
    {"email": "amara.okafor@waypoint.dev", "full_name": "Amara Okafor", "courses": ["UX Design Foundations"]},
]

DEMO_PASSWORD = "waypoint123"


def get_or_create_user(db, email, full_name, role, password=DEMO_PASSWORD):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user
    user = models.User(email=email, full_name=full_name, role=role, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_course(db, course_dict, instructor):
    existing = db.query(models.Course).filter(models.Course.title == course_dict["title"]).first()
    if existing:
        return existing

    course = models.Course(
        title=course_dict["title"],
        description=course_dict["description"],
        category=course_dict["category"],
        tags=course_dict["tags"],
        level=course_dict["level"],
        instructor_id=instructor.id,
        duration_hours=course_dict["duration_hours"],
        color=course_dict["color"],
        project_brief=course_dict.get("project_brief"),
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    for m_order, module_dict in enumerate(course_dict["modules"]):
        module = models.Module(
            course_id=course.id, title=module_dict["title"],
            description=module_dict.get("description"), order=m_order,
        )
        db.add(module)
        db.commit()
        db.refresh(module)

        for l_order, lesson_dict in enumerate(module_dict["lessons"]):
            lesson = models.Lesson(
                module_id=module.id, title=lesson_dict["title"], content=lesson_dict["content"],
                order=l_order, estimated_minutes=lesson_dict.get("estimated_minutes", 10),
            )
            db.add(lesson)

        quiz_dict = module_dict.get("quiz")
        if quiz_dict:
            quiz = models.Quiz(module_id=module.id, title=quiz_dict["title"])
            db.add(quiz)
            db.commit()
            db.refresh(quiz)
            for q in quiz_dict["questions"]:
                db.add(models.QuizQuestion(
                    quiz_id=quiz.id, question_text=q["question_text"],
                    options=q["options"], correct_index=q["correct_index"],
                ))
        db.commit()

    return course


def fabricate_demo_activity(db, student, courses_by_title):
    """Give the demo student realistic history so behavioral recommendations
    have something real to work with immediately."""
    # Enroll them in two related Data Science courses at different progress levels.
    targets = [
        (courses_by_title["Python for Data Analysis"], 1.0),   # fully complete
        (courses_by_title["Machine Learning Foundations"], 0.4),  # partial
    ]
    for course, target_fraction in targets:
        enrollment = db.query(models.Enrollment).filter(
            models.Enrollment.user_id == student.id, models.Enrollment.course_id == course.id
        ).first()
        if enrollment:
            continue
        enrollment = models.Enrollment(
            user_id=student.id, course_id=course.id,
            enrolled_at=datetime.utcnow() - timedelta(days=20),
            last_accessed=datetime.utcnow() - timedelta(days=1),
        )
        db.add(enrollment)
        db.commit()

        all_lessons = [l for mod in course.modules for l in mod.lessons]
        n_complete = round(len(all_lessons) * target_fraction)
        for lesson in all_lessons[:n_complete]:
            db.add(models.LessonProgress(user_id=student.id, lesson_id=lesson.id))
        db.commit()

        # Pass the quizzes for fully-completed modules.
        for mod in course.modules:
            if not mod.quiz or not mod.quiz.questions:
                continue
            mod_lessons = mod.lessons
            if all(l in all_lessons[:n_complete] for l in mod_lessons):
                answers = [q.correct_index for q in mod.quiz.questions]  # perfect score
                score = 100.0
                db.add(models.QuizAttempt(user_id=student.id, quiz_id=mod.quiz.id, score=score, answers=answers))
        db.commit()

        if target_fraction >= 1.0:
            from app.services.progress import maybe_issue_certificate
            maybe_issue_certificate(db, student.id, course.id)
            existing_review = db.query(models.Review).filter(
                models.Review.user_id == student.id, models.Review.course_id == course.id
            ).first()
            if not existing_review:
                db.add(models.Review(
                    user_id=student.id, course_id=course.id, rating=5,
                    comment="Clear explanations and the pacing was exactly right for a beginner. The data-cleaning module alone was worth it.",
                ))
                db.commit()


def seed_other_students_light_activity(db, students, courses_by_title):
    """Give a couple of other demo students a review each, so course cards
    aren't showing zero ratings across the board."""
    sample_reviews = [
        ("Full-Stack Web Development with React", 5, "Finally a React course that explains *why*, not just *how*. The useEffect lesson clicked for me."),
        ("Modern Backend APIs with FastAPI", 4, "Solid, practical course. Would love even more on testing, but the auth section alone was worth it."),
        ("Cloud & DevOps Essentials", 5, "Explained Docker better than three YouTube tutorials combined. Multi-stage builds finally make sense."),
        ("UX Design Foundations", 5, "Changed how I run interviews at work, not just how I design screens."),
    ]
    for i, (title, rating, comment) in enumerate(sample_reviews):
        if i >= len(students):
            break
        student = students[i]
        course = courses_by_title[title]
        existing = db.query(models.Enrollment).filter(
            models.Enrollment.user_id == student.id, models.Enrollment.course_id == course.id
        ).first()
        if not existing:
            db.add(models.Enrollment(user_id=student.id, course_id=course.id))
            db.commit()
            # complete a couple of lessons so the review threshold is met
            lessons = [l for mod in course.modules for l in mod.lessons][:3]
            for lesson in lessons:
                db.add(models.LessonProgress(user_id=student.id, lesson_id=lesson.id))
            db.commit()
        existing_review = db.query(models.Review).filter(
            models.Review.user_id == student.id, models.Review.course_id == course.id
        ).first()
        if not existing_review:
            db.add(models.Review(user_id=student.id, course_id=course.id, rating=rating, comment=comment))
            db.commit()


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        instructors = {}
        for inst in INSTRUCTORS:
            instructors[inst["email"]] = get_or_create_user(db, inst["email"], inst["full_name"], models.Role.instructor)

        courses_by_title = {}
        for inst in INSTRUCTORS:
            instructor = instructors[inst["email"]]
            for course_dict in ALL_COURSES:
                if course_dict["title"] in inst["courses"]:
                    courses_by_title[course_dict["title"]] = seed_course(db, course_dict, instructor)

        demo_student = get_or_create_user(db, "alex.demo@waypoint.dev", "Alex Demo", models.Role.student)
        if demo_student.preferences is None:
            prefs = models.UserPreferences(
                user_id=demo_student.id,
                interests=["Data Science", "Cloud & DevOps"],
                skill_level=models.SkillLevel.beginner,
                goal=models.Goal.career_change,
                free_text_interest="I want to get better at analyzing data and eventually move into machine learning",
            )
            db.add(prefs)
            db.commit()

        fabricate_demo_activity(db, demo_student, courses_by_title)

        other_students = []
        for i, name in enumerate(["Jordan Ruiz", "Sam Okafor", "Taylor Kim", "Morgan Diaz"]):
            email = f"demo.student{i+1}@waypoint.dev"
            other_students.append(get_or_create_user(db, email, name, models.Role.student))
        seed_other_students_light_activity(db, other_students, courses_by_title)

        print("Seed complete.")
        print(f"  {len(courses_by_title)} courses, {len(instructors)} instructors")
        print(f"  Demo student login: alex.demo@waypoint.dev / {DEMO_PASSWORD}")
        print(f"  Instructor login example: priya.shah@waypoint.dev / {DEMO_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
