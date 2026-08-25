"""
Automated tests covering, at minimum per the project spec:
  1. The auth flow (register, login, invalid credentials, protected routes)
  2. The recommendation engine logic (cold start, blending, weight capping)

Run with: pytest -v  (from the backend/ directory)

Uses an isolated in-memory SQLite database per test run via dependency
override, so these tests never touch the real waypoint.db seeded for the
demo.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models
from app.services.recommender import RecommendationEngine

# ---------- isolated test database ----------
# StaticPool keeps a single shared connection alive for the in-memory SQLite
# DB across the whole test -- without it, each new connection (which
# TestClient's requests trigger) would get its OWN blank :memory: database.

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ---------- auth flow ----------

def test_register_creates_user_and_returns_token():
    response = client.post("/auth/register", json={
        "email": "test@example.com", "password": "supersecure1", "full_name": "Test User",
    })
    assert response.status_code == 201
    body = response.json()
    assert "access_token" in body
    assert body["user"]["email"] == "test@example.com"
    assert body["user"]["role"] == "student"


def test_register_rejects_duplicate_email():
    client.post("/auth/register", json={
        "email": "dup@example.com", "password": "supersecure1", "full_name": "First",
    })
    response = client.post("/auth/register", json={
        "email": "dup@example.com", "password": "anotherpass1", "full_name": "Second",
    })
    assert response.status_code == 400


def test_login_succeeds_with_correct_credentials():
    client.post("/auth/register", json={
        "email": "login@example.com", "password": "correctpass1", "full_name": "Login Test",
    })
    response = client.post("/auth/login", json={"email": "login@example.com", "password": "correctpass1"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_rejects_wrong_password():
    client.post("/auth/register", json={
        "email": "wrongpass@example.com", "password": "correctpass1", "full_name": "Test",
    })
    response = client.post("/auth/login", json={"email": "wrongpass@example.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_protected_route_rejects_missing_token():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_protected_route_accepts_valid_token():
    register_response = client.post("/auth/register", json={
        "email": "me@example.com", "password": "supersecure1", "full_name": "Me",
    })
    token = register_response.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


# ---------- recommendation engine ----------

def _make_course(id, title, category, level, description="", tags=None):
    return models.Course(
        id=id, title=title, description=description, category=category,
        level=level, instructor_id=1, tags=tags or [], duration_hours=5, color="#000",
    )


def test_cold_start_uses_only_onboarding_signal_when_no_enrollments():
    courses = [
        _make_course(1, "Intro to Python", "Data Science", models.SkillLevel.beginner, "Learn python basics"),
        _make_course(2, "Advanced Cooking", "Design", models.SkillLevel.advanced, "Culinary arts"),
    ]
    engine_obj = RecommendationEngine(courses)
    prefs = models.UserPreferences(
        interests=["Data Science"], skill_level=models.SkillLevel.beginner, free_text_interest=None,
    )
    scores, dominant = engine_obj.onboarding_scores(prefs)
    # the matching-category, matching-level course should score strictly higher
    assert scores[0] > scores[1]
    assert dominant[0] == "category"


def test_behavioral_weight_is_zero_with_no_enrollment_history():
    db = TestSessionLocal()
    courses = [_make_course(1, "A", "Data Science", models.SkillLevel.beginner)]
    engine_obj = RecommendationEngine(courses)
    user = models.User(id=1, email="x@x.com", hashed_password="x", full_name="X")
    scores, _ = engine_obj.behavioral_scores(db, user_id=1, enrolled_course_ids=set())
    assert (scores == 0).all()
    db.close()


def test_recommendation_reasons_are_specific_not_generic():
    courses = [
        _make_course(1, "Intro to Python", "Data Science", models.SkillLevel.beginner, "Learn python basics for data work"),
        _make_course(2, "React Basics", "Web Development", models.SkillLevel.beginner, "Learn react components"),
    ]
    engine_obj = RecommendationEngine(courses)
    db = TestSessionLocal()
    user = models.User(id=1, email="x@x.com", hashed_password="x", full_name="X")
    prefs = models.UserPreferences(interests=["Data Science"], skill_level=models.SkillLevel.beginner)
    results = engine_obj.recommend(db, user, prefs, enrolled_course_ids=set(), limit=5)
    assert len(results) == 2
    top = results[0]
    assert top.course.title == "Intro to Python"
    assert "Data Science" in top.reason  # specific to the matched category, not generic
    db.close()


def test_max_behavioral_weight_never_reaches_full_override_of_onboarding():
    """Even with very high engagement, onboarding_weight should stay > 0,
    matching the spec requirement that stated preferences never fully vanish."""
    from app.services.recommender import MAX_BEHAVIORAL_WEIGHT
    assert MAX_BEHAVIORAL_WEIGHT < 1.0


def test_enrolled_courses_are_excluded_from_recommendations():
    courses = [
        _make_course(1, "Course A", "Data Science", models.SkillLevel.beginner),
        _make_course(2, "Course B", "Data Science", models.SkillLevel.beginner),
    ]
    engine_obj = RecommendationEngine(courses)
    db = TestSessionLocal()
    user = models.User(id=1, email="x@x.com", hashed_password="x", full_name="X")
    prefs = models.UserPreferences(interests=["Data Science"], skill_level=models.SkillLevel.beginner)
    results = engine_obj.recommend(db, user, prefs, enrolled_course_ids={1}, limit=5)
    assert all(r.course.id != 1 for r in results)
    db.close()
