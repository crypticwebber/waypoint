"""
Central configuration for the Waypoint API.

Everything is deliberately file-based (SQLite) and dependency-free so the
whole platform runs with nothing but `pip install` -- no Redis, no broker,
no external services.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'waypoint.db')}"

# In a real deployment this would come from the environment. For a capstone
# project a fixed dev secret is fine, but we still isolate it in one place
# so it's obvious where you'd wire in a real secret manager.
JWT_SECRET_KEY = os.environ.get("WAYPOINT_JWT_SECRET", "waypoint-dev-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days -- convenient for demoing

# Minimum passing score (%) on a module quiz for it to count towards
# certificate eligibility.
QUIZ_PASS_THRESHOLD = 70

# Minimum course completion (%) before a learner is allowed to leave a review.
REVIEW_PROGRESS_THRESHOLD = 20

ALLOWED_ORIGINS = os.environ.get("WAYPOINT_ALLOWED_ORIGINS", "*").split(",")