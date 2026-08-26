from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401 -- ensures models are registered before create_all
from app.config import ALLOWED_ORIGINS
from app.routers import auth, preferences, courses, learning, reviews, certificates, recommendations, dashboard, instructor
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Waypoint API",
    description=(
        "Backend for Waypoint, a skills-learning platform. Onboarding-driven "
        "recommendations blend a cold-start survey signal with a behavioral "
        "content-based recommender -- see /recommendations/me and "
        "app/services/recommender.py for the algorithm."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(preferences.router)
app.include_router(courses.router)
app.include_router(learning.router)
app.include_router(reviews.router)
app.include_router(certificates.router)
app.include_router(recommendations.router)
app.include_router(dashboard.router)
app.include_router(instructor.router)


@app.get("/", tags=["health"], summary="Health check")
def root():
    return {"status": "ok", "service": "waypoint-api"}
