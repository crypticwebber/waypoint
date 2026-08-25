# Waypoint

A skills-learning platform (think Coursera-tier, capstone-scoped): onboarding-driven
recommendations, real hand-written course content, module quizzes, auto-issued PDF
certificates, and an instructor authoring studio -- built as FastAPI + SQLite on the
backend and React + Tailwind on the frontend, with zero external services (no Redis,
no Celery, no Docker requirement).

## Architecture

```
waypoint/
├── backend/                 FastAPI + SQLAlchemy + SQLite
│   ├── app/
│   │   ├── main.py              FastAPI app, router registration, CORS
│   │   ├── config.py            All tunable constants in one place
│   │   ├── database.py          SQLAlchemy engine/session
│   │   ├── models.py            ORM models (full data model, see below)
│   │   ├── schemas.py           Pydantic request/response schemas
│   │   ├── auth.py              JWT + bcrypt, get_current_user dependency
│   │   ├── seed.py               Idempotent seed script
│   │   ├── seed_data/            Hand-written content, one file per course
│   │   ├── services/
│   │   │   ├── progress.py       Derives completion %, best quiz score, cert eligibility
│   │   │   ├── recommender.py    The hybrid recommendation engine (see below)
│   │   │   └── serializers.py    ORM -> response-schema helpers with derived fields
│   │   └── routers/              auth, preferences, courses, learning, reviews,
│   │                              certificates, recommendations, dashboard, instructor
│   └── tests/
│       └── test_core.py          Auth flow + recommendation engine tests (pytest)
│
└── frontend/                 React 19 + Vite + Tailwind + React Router + axios
    └── src/
        ├── api/                   Centralized axios client + one function per endpoint
        ├── context/               Auth context, toast notification context
        ├── components/           Nav, CourseCard, RouteLine (signature visual),
        │                          CourseSidebar, loading/empty/error states
        ├── pages/                 One file per route (see Pages below)
        └── hooks/useFetch.js      Shared loading/error/refetch data-fetching hook
```

### Data model

`User` → `UserPreferences` (1:1, the onboarding survey answers) · `Course` →
`Module` → `Lesson` (ordered tree) · `Enrollment` (user↔course) · `LessonProgress`
(user↔lesson, existence = completed) · `Quiz` (1:1 with `Module`) → `QuizQuestion` →
`QuizAttempt` (full history kept, best score derived) · `Review` (user↔course) ·
`Certificate` (auto-issued, unique code).

**Course completion % and quiz "best score" are never stored as a mutable field.**
They're derived at query time from `LessonProgress` / `QuizAttempt` rows
(`app/services/progress.py`) specifically so they can never drift out of sync with
what actually happened.

### Pages (frontend)

Landing → Register → Onboarding (4-step survey) → Dashboard (stats, continue
learning, recommendations, completed) → Catalog (search/filter/pagination) →
Course Detail (syllabus, project brief, reviews, enroll) → Lesson Reader (markdown
content, sidebar with progress, mark-complete) → Quiz (scored, retakes, history) →
Certificates (view + authenticated PDF download). Instructor: Studio (course list +
stats + create), Course Editor (modules/lessons/quiz CRUD), Roster (per-student
progress).

## Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed               # idempotent -- safe to re-run
uvicorn app.main:app --reload --port 8000
```

API docs (with real descriptions on every route): `http://localhost:8000/docs`

Demo logins (password `waypoint123` for all):
- Student with real history: `alex.demo@waypoint.dev`
- Instructor: `priya.shah@waypoint.dev` (also `marcus.lee@`, `jonas.weber@`, `amara.okafor@waypoint.dev`)

Run tests: `pytest -v` (from `backend/`, with the venv active)

### Frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173, expects the API at localhost:8000
```

`npm run build` produces a production bundle in `frontend/dist/`.

## How the recommendation engine works

This is the feature most likely to come up in a viva, so here's the full picture.

**The problem it solves:** a brand-new user has no behavioral history to learn
from, but a returning user's actual engagement is a far stronger signal than
anything they self-reported at signup. Naively switching between "onboarding mode"
and "behavioral mode" would cause visible, jarring jumps in recommendations the
moment someone finishes their first lesson. Waypoint scores every course on
**both** signals continuously and blends them with a weight that shifts smoothly
as the user accumulates history.

**One shared vector space.** Every course is turned into a TF-IDF document from
its title, category, tags, and description (`_course_document()` in
`recommender.py`). This is what lets the same math compare a user's free-text
onboarding answer against course descriptions, *and* compare a course someone's
80%-completed against the rest of the catalog -- one vectorizer, one vector space,
two different query vectors.

**Onboarding score** (cold start) is a weighted sum of three signals:
- **Category match** -- did the user tick this course's category as an interest?
- **Level match** -- does the course level match their stated skill level (with
  partial credit for an adjacent level)?
- **Free-text similarity** -- cosine similarity between their free-text answer and
  the course's TF-IDF document.

If the user skipped the free-text field, that weight is redistributed
proportionally to the other two, so a partially-filled survey still produces a
meaningful score instead of being penalized for a missing signal.

**Behavioral score** (warm state) is a classic content-based recommender: build
one "taste vector" per user by averaging the TF-IDF vectors of every course
they've engaged with, weighted by how much of each they've completed (a finished
course says more about taste than one abandoned at 5%), then score every other
course by cosine similarity to that taste vector.

**Blending.** `behavioral_weight = min(0.8, 0.35 * engagement)`, where engagement
is the sum of completion fractions across all enrollments. This weight is
deliberately capped below 1.0 so a user's stated onboarding preferences **never
fully disappear**, no matter how much history they build up -- someone's stated
goal should keep mattering. A brand-new user (`engagement = 0`) gets
`behavioral_weight = 0`, i.e. 100% onboarding-driven recommendations, satisfying
the "cold start = pure onboarding" requirement exactly.

**Reasons are signal-specific, not generic.** For each recommended course,
Waypoint compares how much the onboarding signal vs. the behavioral signal
actually contributed to its final score and generates the human-readable reason
from whichever one dominated -- `"Matches your interest in Web Development"`,
`"Fits your beginner skill level"`, `"Matches what you told us you want to
learn"`, or `"Because you engaged with Python for Data Analysis"` (naming the
specific enrolled course the recommendation is closest to). Nothing is a generic
"Recommended for you" label.

All of this is exposed as a single `GET /recommendations/me` -- the frontend never
needs to know whether it's looking at a cold-start or blended response; the
blending happens entirely server-side.

## Known scope trims

Given the size of the full spec, a few things were deliberately trimmed and are
worth naming rather than leaving implicit:
- Each of the 6 courses ships 3 modules × 3 lessons (9 lessons/course, 54 total)
  rather than the stretch target of 15-20 lessons/course, to keep every lesson
  genuinely well-written rather than padded.
- The frontend bundle isn't code-split (single ~520KB JS chunk) -- fine at this
  scale, but a real production deploy would lazy-load routes.
- Frontend automated tests were deprioritized in favor of backend tests (auth +
  recommender), per the spec's "at minimum" wording; a good next addition would be
  a handful of React Testing Library smoke tests for the onboarding flow and quiz
  submission.
