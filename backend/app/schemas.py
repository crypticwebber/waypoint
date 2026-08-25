from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models import Role, SkillLevel, Goal


# ---------- Auth / Users ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1)
    role: Role = Role.student


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: Role
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Onboarding ----------

class PreferencesIn(BaseModel):
    interests: list[str] = Field(default_factory=list)
    skill_level: Optional[SkillLevel] = None
    goal: Optional[Goal] = None
    free_text_interest: Optional[str] = None


class PreferencesOut(PreferencesIn):
    model_config = ConfigDict(from_attributes=True)


# ---------- Courses ----------

class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    order: int
    estimated_minutes: int


class LessonDetailOut(LessonOut):
    content: str
    completed: bool = False


class QuizQuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    question_text: str
    options: list[str]


class QuizQuestionAdminOut(QuizQuestionOut):
    correct_index: int


class QuizOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    questions: list[QuizQuestionOut]
    best_score: Optional[float] = None
    attempt_count: int = 0


class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    order: int
    lessons: list[LessonOut]
    quiz: Optional[QuizOut] = None
    completed_lessons: int = 0


class CourseCardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    category: str
    tags: list[str]
    level: SkillLevel
    duration_hours: float
    color: str
    instructor_name: str = ""
    avg_rating: Optional[float] = None
    review_count: int = 0
    enrolled_count: int = 0


class CourseDetailOut(CourseCardOut):
    project_brief: Optional[str] = None
    modules: list[ModuleOut] = []
    is_enrolled: bool = False
    progress_pct: float = 0.0


class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    tags: list[str] = Field(default_factory=list)
    level: SkillLevel
    duration_hours: float = 0
    color: str = "#E8A33D"
    project_brief: Optional[str] = None


class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0


class LessonCreate(BaseModel):
    title: str
    content: str
    order: int = 0
    estimated_minutes: int = 10


class QuizQuestionCreate(BaseModel):
    question_text: str
    options: list[str]
    correct_index: int


# ---------- Enrollment / Progress ----------

class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int
    enrolled_at: datetime
    last_accessed: datetime


class QuizSubmission(BaseModel):
    answers: list[int]


class QuizAttemptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    score: float
    taken_at: datetime


# ---------- Reviews ----------

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    user_name: str = ""
    rating: int
    comment: Optional[str]
    created_at: datetime


# ---------- Certificates ----------

class CertificateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int
    course_title: str = ""
    issued_at: datetime
    certificate_code: str


# ---------- Recommendations ----------

class RecommendationOut(BaseModel):
    course: CourseCardOut
    reason: str
    score: float
    source: str  # "onboarding" | "behavioral" | "blend"


# ---------- Dashboard ----------

class DashboardStats(BaseModel):
    courses_enrolled: int
    courses_completed: int
    lessons_completed: int
    certificates_earned: int
    avg_quiz_score: Optional[float] = None


class ContinueLearningItem(BaseModel):
    course: CourseCardOut
    next_lesson: Optional[LessonOut] = None
    progress_pct: float = 0.0


# ---------- Instructor ----------

class RosterEntry(BaseModel):
    user_id: int
    full_name: str
    email: str
    progress_pct: float
    enrolled_at: datetime


class InstructorCourseStats(BaseModel):
    course: CourseCardOut
    enrolled_count: int
    avg_quiz_score: Optional[float]
    completion_rate: float
