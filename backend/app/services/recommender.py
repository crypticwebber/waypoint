"""
Waypoint's recommendation engine.

WHY A HYBRID, AND WHY TF-IDF
-----------------------------
A brand-new user has no behavior to learn from ("cold start"), but they DO
tell us three structured things at signup (interests, skill level, goal) and
optionally a free-text sentence about what they want to learn. Once they
start actually taking courses, their real engagement is a much stronger
signal than anything they self-reported. Rather than hard-switching between
"onboarding mode" and "behavioral mode" -- which would cause recommendations
to visibly jump the moment someone finishes their first lesson -- we score
every course on BOTH signals and blend them with a weight that shifts
smoothly as the user accumulates history.

Both signals are represented in the SAME vector space: every course is
turned into one bag-of-words TF-IDF document built from its title,
description, tags and category. That's what lets us compare a user's free-
text answer ("I want to get good at cloud infrastructure") against a
course's blurb, and *also* compare a course a user has 80%-completed against
every other course in the catalog, using the exact same cosine-similarity
math. One vectorizer, one vector space, two different query vectors.

ONBOARDING SCORE (cold start) -- weighted sum of three signals:
  - category match   (did they tick this course's category as an interest?)
  - level match       (does the course level match their stated skill level?)
  - free-text TF-IDF similarity (cosine similarity between their free-text
    answer and the course's TF-IDF document)
  Weights renormalize if the user skipped the free-text field, so a user who
  only filled in interests/level still gets a meaningful score instead of
  being penalized for the missing signal.

BEHAVIORAL SCORE (warm state) -- classic content-based recommender:
  - build one "taste vector" per user = the TF-IDF vectors of every course
    they've engaged with, averaged and weighted by how much of each course
    they've completed (a course they finished says more about their taste
    than one they clicked into and abandoned at 5%)
  - score every other course by cosine similarity to that taste vector

BLENDING
  behavioral_weight = min(MAX_BEHAVIORAL_WEIGHT, ENGAGEMENT_SCALE * engagement)
  where `engagement` is the sum of completion fractions across enrollments.
  This weight is capped at MAX_BEHAVIORAL_WEIGHT (< 1.0) specifically so a
  user's stated onboarding preferences never fully disappear, even after
  years of activity -- someone's stated *goal* should keep mattering.

  final_score = (1 - behavioral_weight) * onboarding_score
              +      behavioral_weight  * behavioral_score

REASONS
  We track which signal contributed the most to a course's final score and
  generate the human-readable reason from THAT signal specifically, rather
  than a generic "recommended for you" label -- e.g. "Matches your interest
  in Web Development" (category), "Matches what you told us you want to
  learn" (free text), or "Because you completed Python for Data Analysis"
  (behavioral, naming the specific course that drove the similarity).
"""
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app import models
from app.services.progress import course_progress_pct

# --- tunable constants, named so the "why" is visible in one place ---
ONBOARDING_WEIGHTS = {"category": 0.5, "level": 0.2, "text": 0.3}
MAX_BEHAVIORAL_WEIGHT = 0.8   # onboarding signal always keeps >= 20% weight
ENGAGEMENT_SCALE = 0.35       # how fast behavioral weight ramps up with use
LEVEL_ORDER = ["beginner", "intermediate", "advanced"]


@dataclass
class ScoredCourse:
    course: models.Course
    score: float
    reason: str
    source: str


def _course_document(course: models.Course) -> str:
    """Flatten a course into the bag-of-words document used for TF-IDF."""
    tag_text = " ".join(course.tags or [])
    # title and category are repeated to give them a little extra weight
    # relative to the (longer) free-form description.
    return f"{course.title} {course.title} {course.category} {course.category} {tag_text} {course.description}"


def _level_similarity(user_level: str | None, course_level: str) -> float:
    if not user_level:
        return 0.0
    if user_level == course_level:
        return 1.0
    try:
        dist = abs(LEVEL_ORDER.index(user_level) - LEVEL_ORDER.index(course_level))
    except ValueError:
        return 0.0
    return max(0.0, 1.0 - 0.5 * dist)  # adjacent level still gets partial credit


class RecommendationEngine:
    """
    One instance is built per request from the current catalog. Rebuilding
    the TF-IDF matrix on every call keeps things simple and is completely
    fine at this scale (a few dozen courses) -- no caching/background
    workers needed, matching the project's "recompute on request" design.
    """

    def __init__(self, courses: list[models.Course]):
        self.courses = courses
        self.index_by_id = {c.id: i for i, c in enumerate(courses)}
        documents = [_course_document(c) for c in courses]
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=2000)
        self.matrix = self.vectorizer.fit_transform(documents) if documents else None

    def _text_similarities(self, text: str) -> np.ndarray:
        if not text or not text.strip() or self.matrix is None:
            return np.zeros(len(self.courses))
        query_vec = self.vectorizer.transform([text])
        return cosine_similarity(query_vec, self.matrix).flatten()

    def onboarding_scores(self, prefs: models.UserPreferences | None) -> tuple[np.ndarray, list[str]]:
        """Returns (scores per course, dominant-signal label per course)."""
        n = len(self.courses)
        if prefs is None:
            return np.zeros(n), ["none"] * n

        interests = set(prefs.interests or [])
        has_text = bool(prefs.free_text_interest and prefs.free_text_interest.strip())

        weights = dict(ONBOARDING_WEIGHTS)
        if not has_text:
            # redistribute the text weight proportionally to the other two signals
            leftover = weights.pop("text")
            total = weights["category"] + weights["level"]
            for k in weights:
                weights[k] += leftover * (weights[k] / total)

        text_sims = self._text_similarities(prefs.free_text_interest or "")

        scores = np.zeros(n)
        dominant = []
        for i, course in enumerate(self.courses):
            category_score = 1.0 if course.category in interests else 0.0
            level_score = _level_similarity(
                prefs.skill_level.value if prefs.skill_level else None, course.level.value
            )
            text_score = text_sims[i] if has_text else 0.0

            contributions = {
                "category": weights.get("category", 0) * category_score,
                "level": weights.get("level", 0) * level_score,
                "text": weights.get("text", 0) * text_score,
            }
            scores[i] = sum(contributions.values())
            dominant.append(max(contributions, key=contributions.get))
        return scores, dominant

    def behavioral_scores(self, db: Session, user_id: int, enrolled_course_ids: set[int]) -> tuple[np.ndarray, list[int | None]]:
        """
        Returns (scores per course, id of the enrolled course each score is
        'closest to' -- used to build the "Because you completed X" reason).
        """
        n = len(self.courses)
        if self.matrix is None or not enrolled_course_ids:
            return np.zeros(n), [None] * n

        taste_vector = None
        total_weight = 0.0
        weighted_rows = []
        engaged_indices = []
        for course_id in enrolled_course_ids:
            idx = self.index_by_id.get(course_id)
            if idx is None:
                continue
            progress = course_progress_pct(db, user_id, course_id) / 100.0
            weight = 0.15 + progress  # even 0%-progress enrollments count a little
            weighted_rows.append(self.matrix[idx].toarray()[0] * weight)
            total_weight += weight
            engaged_indices.append(idx)

        if not weighted_rows or total_weight == 0:
            return np.zeros(n), [None] * n

        taste_vector = np.sum(weighted_rows, axis=0) / total_weight
        sims = cosine_similarity([taste_vector], self.matrix).flatten()

        # For explanation purposes, find which single enrolled course each
        # candidate is most similar to.
        closest_course_id = [None] * n
        engaged_matrix = self.matrix[engaged_indices]
        engaged_ids = [self.courses[i].id for i in engaged_indices]
        per_engaged_sims = cosine_similarity(self.matrix, engaged_matrix)
        for i in range(n):
            best_j = int(np.argmax(per_engaged_sims[i]))
            closest_course_id[i] = engaged_ids[best_j]

        return sims, closest_course_id

    def recommend(
        self,
        db: Session,
        user: models.User,
        prefs: models.UserPreferences | None,
        enrolled_course_ids: set[int],
        limit: int = 8,
    ) -> list[ScoredCourse]:
        onboarding_scores, onboarding_dominant = self.onboarding_scores(prefs)
        behavioral_scores, closest_course_id = self.behavioral_scores(db, user.id, enrolled_course_ids)

        # Engagement = sum of completion fractions across enrollments, so a
        # user with two courses at 50% "counts" the same as one finished.
        engagement = 0.0
        for cid in enrolled_course_ids:
            engagement += course_progress_pct(db, user.id, cid) / 100.0
        behavioral_weight = min(MAX_BEHAVIORAL_WEIGHT, ENGAGEMENT_SCALE * engagement)
        onboarding_weight = 1.0 - behavioral_weight

        results = []
        course_by_id = {c.id: c for c in self.courses}
        for i, course in enumerate(self.courses):
            if course.id in enrolled_course_ids:
                continue  # don't recommend what they're already taking

            final = onboarding_weight * onboarding_scores[i] + behavioral_weight * behavioral_scores[i]

            # Decide which signal to explain with: whichever contributed more
            # to this specific course's score.
            onboarding_contribution = onboarding_weight * onboarding_scores[i]
            behavioral_contribution = behavioral_weight * behavioral_scores[i]

            if behavioral_contribution > onboarding_contribution and behavioral_contribution > 0:
                source = "behavioral"
                ref_course = course_by_id.get(closest_course_id[i])
                reason = f"Because you engaged with {ref_course.title}" if ref_course else "Based on your course activity"
            else:
                source = "onboarding" if behavioral_weight < 1.0 else "blend"
                signal = onboarding_dominant[i]
                if signal == "category":
                    reason = f"Matches your interest in {course.category}"
                elif signal == "level":
                    reason = f"Fits your {prefs.skill_level.value if prefs and prefs.skill_level else 'stated'} skill level"
                elif signal == "text":
                    reason = "Matches what you told us you want to learn"
                else:
                    reason = "Popular starting point on Waypoint"

            results.append(ScoredCourse(course=course, score=round(float(final), 4), reason=reason, source=source))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]
