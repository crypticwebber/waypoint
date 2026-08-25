"""
SQLAlchemy ORM models.

Design notes:
- Course completion % and quiz "best score" are DERIVED at query time from
  LessonProgress / QuizAttempt rows rather than stored as a mutable field.
  This avoids the classic bug where a cached progress number drifts out of
  sync with reality. See app/services/progress.py for the derivation logic.
- JSON-ish list/dict fields (Course.tags, UserPreferences.interests,
  QuizQuestion.options, QuizAttempt.answers) are stored as SQLite JSON
  columns -- SQLAlchemy handles the (de)serialization for us.
"""
import enum
import secrets
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Float, Enum, JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Role(str, enum.Enum):
    student = "student"
    instructor = "instructor"


class SkillLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Goal(str, enum.Enum):
    career_change = "career_change"
    upskilling = "upskilling"
    academic = "academic"
    personal_interest = "personal_interest"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.student, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    preferences = relationship("UserPreferences", uselist=False, back_populates="user", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")
    lesson_progress = relationship("LessonProgress", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")
    courses_taught = relationship("Course", back_populates="instructor")


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    interests = Column(JSON, default=list)  # list[str] of category names
    skill_level = Column(Enum(SkillLevel), nullable=True)
    goal = Column(Enum(Goal), nullable=True)
    free_text_interest = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, index=True, nullable=False)
    tags = Column(JSON, default=list)  # list[str]
    level = Column(Enum(SkillLevel), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duration_hours = Column(Float, default=0)
    color = Column(String, default="#E8A33D")  # accent used for the course card
    project_brief = Column(Text, nullable=True)  # end-of-course hands-on project
    created_at = Column(DateTime, default=datetime.utcnow)

    instructor = relationship("User", back_populates="courses_taught")
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan", order_by="Module.order")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="course", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order")
    quiz = relationship("Quiz", uselist=False, back_populates="module", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # markdown
    order = Column(Integer, default=0)
    estimated_minutes = Column(Integer, default=10)

    module = relationship("Module", back_populates="lessons")
    progress_entries = relationship("LessonProgress", back_populates="lesson", cascade="all, delete-orphan")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress_entries")


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), unique=True, nullable=False)
    title = Column(String, nullable=False)

    module = relationship("Module", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # list[str]
    correct_index = Column(Integer, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)  # percentage 0-100
    answers = Column(JSON, nullable=False)  # list[int] chosen option indices
    taken_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_review"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    course = relationship("Course", back_populates="reviews")


class Certificate(Base):
    __tablename__ = "certificates"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_cert"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    certificate_code = Column(String, unique=True, default=lambda: secrets.token_hex(8).upper())

    user = relationship("User", back_populates="certificates")
    course = relationship("Course")
