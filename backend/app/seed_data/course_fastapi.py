COURSE = {
    "title": "Modern Backend APIs with FastAPI",
    "description": (
        "Design and build a real REST API with FastAPI: request validation, "
        "a proper database layer, authentication, and the kind of "
        "error-handling and documentation that makes an API pleasant for "
        "someone else to build against."
    ),
    "category": "Web Development",
    "tags": ["fastapi", "python", "rest api", "sqlalchemy", "backend", "authentication"],
    "level": "intermediate",
    "duration_hours": 10,
    "color": "#3E6B99",
    "project_brief": (
        "Design and build a small 'bookmarks' API: users can register, log "
        "in, and create/list/delete their own bookmarks (url, title, tags). "
        "Enforce that a user can only see and delete their own bookmarks, "
        "validate input properly, and document every endpoint so someone "
        "unfamiliar with your code could use /docs to integrate against it "
        "without asking you a single question."
    ),
    "modules": [
        {
            "title": "Routes, validation, and the request/response cycle",
            "description": "How FastAPI turns a Python function into a documented, validated HTTP endpoint.",
            "lessons": [
                {
                    "title": "Your first endpoint, and why FastAPI feels different",
                    "estimated_minutes": 14,
                    "content": """A REST API's job is simple to state: receive an HTTP request, do
something, return an HTTP response. What makes FastAPI worth learning
specifically is that it derives an enormous amount of value -- validation,
serialization, and interactive documentation -- from nothing more than
regular Python type hints.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int):
    return {"id": bookmark_id, "url": "https://example.com"}
```

That `bookmark_id: int` type hint isn't just documentation for humans --
FastAPI actually enforces it. A request to `/bookmarks/abc` is
automatically rejected with a clear 422 error before your function body
even runs, because `"abc"` can't be parsed as an `int`. You didn't write a
single line of validation code; the type hint *is* the validation.

The four HTTP methods map directly to decorators: `@app.get` for reading,
`@app.post` for creating, `@app.put` (or `@app.patch`) for updating, and
`@app.delete` for removing. Sticking to this convention (rather than, say,
using `GET` for an action that changes data) matters beyond style -- browsers,
caches, and proxies all assume `GET` requests are safe to repeat and cache,
and violating that assumption causes real, hard-to-debug production bugs.

Run any FastAPI app with `uvicorn main:app --reload` and visit `/docs` --
you get a fully interactive API explorer, generated automatically from your
route definitions, with zero extra code. This single feature is a large
part of why FastAPI has become a default choice for new Python APIs: the
documentation can't drift out of sync with the code, because it *is* the
code.""",
                },
                {
                    "title": "Request bodies with Pydantic",
                    "estimated_minutes": 15,
                    "content": """Path parameters (like `bookmark_id` above) and query parameters cover
simple cases, but creating a resource usually needs a structured request
body. FastAPI pairs with Pydantic for this: define a class describing the
shape you expect, and FastAPI validates every incoming request against it
automatically.

```python
from pydantic import BaseModel, HttpUrl, Field

class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str = Field(min_length=1, max_length=200)
    tags: list[str] = []

@app.post("/bookmarks")
def create_bookmark(payload: BookmarkCreate):
    return {"url": str(payload.url), "title": payload.title, "tags": payload.tags}
```

If a client POSTs `{"title": ""}` (missing `url`, and a `title` that
violates `min_length=1`), FastAPI returns a 422 response listing *exactly*
which fields failed and why -- before `create_bookmark` ever executes. This
is a genuinely important shift in where validation logic lives: instead of
a function full of `if not data.get("url"): return error(...)` checks, the
shape of correct data is declared once, and enforced everywhere that
declaration is used.

`HttpUrl` is one of Pydantic's built-in specialized types -- beyond
catching "is this a string," it actually validates the string looks like a
real URL, catching a whole category of bad input for free. Reaching for
these specific types (`EmailStr`, `HttpUrl`, `PositiveInt`, and so on)
instead of a plain `str` or `int` wherever they fit is a habit that
noticeably reduces how much manual validation code an API needs.

Separate schemas for input vs. output is a pattern worth adopting early: a
`BookmarkCreate` schema (what the client sends) is rarely identical to a
`BookmarkOut` schema (what you return) -- the output often includes fields
like `id` and `created_at` that a client should never be allowed to set
themselves on creation.""",
                },
                {
                    "title": "Status codes and error responses that actually help",
                    "estimated_minutes": 14,
                    "content": """Returning the right HTTP status code is a form of communication with
whoever (or whatever) is calling your API -- a client program often
branches its behavior based on the status code alone, before it even reads
the response body.

```python
from fastapi import HTTPException, status

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int):
    bookmark = find_bookmark(bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
    return bookmark

@app.post("/bookmarks", status_code=status.HTTP_201_CREATED)
def create_bookmark(payload: BookmarkCreate):
    ...
```

A few codes are worth knowing cold, because they cover the overwhelming
majority of real API responses: `200` (success), `201` (created --
explicitly set with `status_code=201`, since FastAPI defaults `POST` to
`200`), `204` (success, no body -- typical for `DELETE`), `400` (the
request itself is malformed), `401` (not authenticated -- we don't know who
you are), `403` (authenticated, but not allowed to do this), `404` (not
found), and `422` (validation failed -- FastAPI's automatic response for
bad request bodies).

The distinction between 401 and 403 trips people up constantly, and it's
worth being precise: 401 means "I don't know who you are" (missing or
invalid credentials), while 403 means "I know exactly who you are, and
you're not allowed to do this" (a logged-in user trying to delete someone
else's bookmark, for instance). Returning 404 in cases like that second one
is also a legitimate, common choice -- it avoids confirming a resource
exists at all to someone who isn't authorized to see it, which matters more
than it sounds for anything containing private user data.

`HTTPException`'s `detail` field should be genuinely useful, not generic --
"Bookmark not found" tells a client something actionable; "Error" or "Bad
request" does not. A well-designed API's error responses are effectively
part of its documentation.""",
                },
            ],
            "quiz": {
                "title": "Routes & Validation Check",
                "questions": [
                    {
                        "question_text": "What actually enforces that bookmark_id must be an integer in @app.get('/bookmarks/{bookmark_id}') def get_bookmark(bookmark_id: int)?",
                        "options": [
                            "A separate validation function you must write",
                            "The Python type hint itself, interpreted by FastAPI",
                            "Nothing -- it's just documentation",
                            "A database constraint",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What generates FastAPI's interactive /docs page?",
                        "options": [
                            "A manually written HTML file",
                            "Automatically, from your route and Pydantic model definitions",
                            "A separate paid service",
                            "It has to be built with a different framework",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What is the key difference between HTTP 401 and 403?",
                        "options": [
                            "There is no real difference",
                            "401 means unauthenticated; 403 means authenticated but not authorized",
                            "401 is for GET requests, 403 is for POST requests",
                            "403 always means the server crashed",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why define separate BookmarkCreate and BookmarkOut schemas?",
                        "options": [
                            "FastAPI requires two schemas for every route",
                            "Input and output shapes often differ, e.g. output includes server-set fields like id",
                            "It has no real benefit, just convention",
                            "To make the /docs page longer",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "A real database layer",
            "description": "SQLAlchemy models, sessions, and dependency injection done properly.",
            "lessons": [
                {
                    "title": "SQLAlchemy models and the ORM mental model",
                    "estimated_minutes": 15,
                    "content": """An ORM (Object-Relational Mapper) lets you work with database rows as
Python objects instead of writing raw SQL strings for every query.
SQLAlchemy is the standard choice in the FastAPI ecosystem, and it centers
on defining your tables as Python classes:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
```

Each class attribute maps to a column; each instance of the class maps to a
row. `Base.metadata.create_all(bind=engine)` reads every model that
inherits from `Base` and creates the corresponding tables -- so for a new
project, defining the model *is* defining the schema.

The key object you interact with day-to-day is a **Session** -- it tracks
which objects you've loaded, queued for insertion, or marked for deletion,
and translates all of it into the right SQL when you call `.commit()`.

```python
new_bookmark = Bookmark(url="https://example.com", title="Example", user_id=1)
db.add(new_bookmark)
db.commit()
db.refresh(new_bookmark)   # loads back any DB-generated values, like the new id
```

`db.refresh()` matters because `new_bookmark.id` doesn't exist yet at the
moment you call `db.add()` -- the database assigns it during the insert.
Forgetting to refresh is a common source of confusing bugs where an object
looks complete in your code but is missing the very id a client needs to
reference it afterward.""",
                },
                {
                    "title": "Sessions as a dependency, done the FastAPI way",
                    "estimated_minutes": 14,
                    "content": """Every request needs its own database session -- sharing one session across
concurrent requests causes hard-to-debug data corruption, since the session
tracks in-progress, uncommitted state. FastAPI's **dependency injection**
system (`Depends`) is the idiomatic way to hand each request a fresh
session and guarantee it's cleaned up afterward, regardless of whether the
request succeeds or raises an exception.

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/bookmarks")
def list_bookmarks(db: Session = Depends(get_db)):
    return db.query(Bookmark).all()
```

The `yield` (instead of `return`) is what makes this work as a proper
setup/teardown dependency: FastAPI runs everything before `yield` first,
hands the yielded session to your route function, waits for the route to
finish, and then runs everything after `yield` -- the `db.close()` -- no
matter what happened in between, including an exception. This pattern
(often called a "context manager" style dependency) is worth recognizing
anywhere you see `yield` inside a FastAPI dependency function.

The other major benefit of `Depends` shows up in testing: because
`get_db` is just a regular function referenced by the route, FastAPI lets
you *override* it in tests (`app.dependency_overrides[get_db] = ...`) to
point at an isolated test database, without touching a single line of
route code. This is the mechanism that makes it realistic to write fast,
isolated tests against real database logic instead of mocking everything
by hand.""",
                },
                {
                    "title": "Querying, filtering, and relationships",
                    "estimated_minutes": 15,
                    "content": """Beyond `db.query(Model).all()`, most real endpoints need filtering, and
SQLAlchemy's query builder reads close to how you'd describe the request in
English.

```python
db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()

db.query(Bookmark).filter(
    Bookmark.user_id == current_user.id,
    Bookmark.title.ilike(f"%{search}%"),
).offset((page - 1) * page_size).limit(page_size).all()
```

That filter-by-`user_id` line deserves special attention: in a multi-user
API, nearly every query that touches user-owned data needs a `user_id`
filter, applied server-side, not left to the client to request correctly.
Forgetting it is a genuine security bug (any logged-in user could read or
delete anyone else's bookmarks by guessing IDs), not just a minor
correctness slip -- it's worth treating "does this query scope to the
current user?" as a mandatory checklist item on every endpoint that
touches per-user data.

Relationships between tables are declared once on the model and then
traversed as regular Python attributes, without writing a JOIN by hand:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="bookmarks")
```

Now `bookmark.user.email` works directly, and SQLAlchemy handles the JOIN
underneath. Watch for the **N+1 query problem** as apps grow: looping over
100 bookmarks and accessing `.user.email` on each one can silently issue
100 separate queries, one per bookmark, if you're not careful. `joinedload`
(imported from `sqlalchemy.orm`) tells SQLAlchemy to fetch the related rows
in the same query up front, collapsing that back down to one -- a fix worth
knowing about even before you hit the performance problem it solves.""",
                },
            ],
            "quiz": {
                "title": "Database Layer Check",
                "questions": [
                    {
                        "question_text": "What does db.refresh(new_bookmark) do after db.commit()?",
                        "options": [
                            "Deletes the object from the database",
                            "Loads back database-generated values like the new id",
                            "Re-runs validation on the object",
                            "Closes the session",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why does get_db() use `yield` instead of `return`?",
                        "options": [
                            "yield is required syntax for all FastAPI functions",
                            "It lets FastAPI guarantee cleanup (db.close()) runs after the request finishes",
                            "yield is faster than return",
                            "There's no real difference",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why is forgetting a user_id filter on a per-user query a security bug, not just a minor slip?",
                        "options": [
                            "It isn't really a security concern",
                            "It could let any logged-in user read or modify another user's data",
                            "It only affects performance, not security",
                            "SQLAlchemy adds the filter automatically regardless",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What problem does joinedload help avoid?",
                        "options": [
                            "SQL injection",
                            "The N+1 query problem from accessing relationships in a loop",
                            "Password hashing",
                            "JWT token expiration",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Authentication and shipping a real API",
            "description": "JWT auth, protecting routes, and the last details that make an API production-ready.",
            "lessons": [
                {
                    "title": "Password hashing and JWT authentication",
                    "estimated_minutes": 16,
                    "content": """Storing a user's actual password anywhere -- even briefly, even in
memory longer than necessary -- is never acceptable. Passwords are
**hashed** before storage: run through a one-way function so the original
can't be recovered even if the database leaks, and hashed again at login
time to compare against the stored hash, never the plaintext.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash(plain_password)
is_valid = pwd_context.verify(plain_password, hashed)
```

bcrypt is deliberately slow (by design, tunable via a cost factor) -- that
slowness is the whole point, since it makes brute-forcing a stolen hash
database far more expensive for an attacker, at a cost of a few
milliseconds per legitimate login that no real user will ever notice.

Once you've verified a password, you need a way for the client to prove
"I already logged in" on every subsequent request, without resending
credentials every time. A JWT (JSON Web Token) is a signed, self-contained
token that encodes a claim (typically the user's id) plus an expiration
time, and the server can verify its authenticity without a database lookup,
just by checking the signature.

```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: int):
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

The signature -- generated using `SECRET_KEY`, which must never be
committed to source control or exposed to the client -- is what prevents a
client from forging or tampering with a token; changing even one character
of the payload invalidates the signature, and the server rejects it. This
is why a leaked `SECRET_KEY` is a complete authentication bypass: anyone
who has it can mint valid tokens for any user id they choose.""",
                },
                {
                    "title": "Protecting routes with dependencies",
                    "estimated_minutes": 14,
                    "content": """With login working, the next step is making certain routes require a
valid token, and giving the route function easy access to *which* user is
making the request. FastAPI's dependency system handles both in one clean
pattern, reusing the same `Depends` mechanism from the database session
lesson.

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (JWTError, KeyError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.get("/bookmarks/me")
def my_bookmarks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()
```

Every protected route just adds `current_user: User = Depends(get_current_user)`
as a parameter -- FastAPI resolves the whole chain (extract the token from
the `Authorization` header, decode it, look up the user, or reject the
request with 401) before your route body runs a single line. This is
dependency injection paying off directly: the authentication logic is
written exactly once and reused everywhere, instead of copy-pasted into
every route that needs it.

For role-based restrictions (say, only instructors can create courses),
the same pattern composes naturally -- a second dependency that calls
`get_current_user` and then checks a role, raising 403 if it doesn't match,
keeps that authorization logic just as centralized as the authentication
check underneath it.""",
                },
                {
                    "title": "The last mile: CORS, pagination, and real documentation",
                    "estimated_minutes": 15,
                    "content": """A handful of details separate an API that technically works from one
that's actually pleasant and safe to build a real frontend against.

**CORS.** Browsers block a webpage from calling an API on a different
origin (domain/port) by default, as a security measure. During
development, your React app on `localhost:5173` and your API on
`localhost:8000` count as different origins, so you need to explicitly opt
in:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

In production, `allow_origins` should list your actual frontend's domain
specifically, not `["*"]` -- a wildcard origin combined with credentialed
requests is a real security misconfiguration, not just a style preference.

**Pagination.** Any endpoint returning a list that can grow -- a course
catalog, a user's bookmarks -- needs `page`/`page_size` query parameters
from day one, not bolted on later once the table has 50,000 rows and every
request starts timing out:

```python
@app.get("/bookmarks")
def list_bookmarks(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    return db.query(Bookmark).offset(offset).limit(page_size).all()
```

**Real documentation.** FastAPI's automatic `/docs` page is only as useful
as the descriptions you give it. A `summary` and `description` on every
route, and a docstring-style explanation of non-obvious parameters, is the
difference between a `/docs` page a new developer can actually integrate
against unassisted, and one that just lists bare endpoint names:

```python
@app.get(
    "/bookmarks",
    summary="List my bookmarks",
    description="Returns the current user's bookmarks, paginated and ordered "
                "by most recently created first.",
)
def list_bookmarks(...): ...
```

None of these three are optional polish for a "real" API in the way a demo
project might treat them -- they're the actual difference between an API
someone else can safely build against, and one they'll be afraid to touch.""",
                },
            ],
            "quiz": {
                "title": "Auth & Production-Readiness Check",
                "questions": [
                    {
                        "question_text": "Why is bcrypt deliberately slow?",
                        "options": [
                            "It's a bug that hasn't been fixed",
                            "The slowness makes brute-forcing stolen password hashes far more expensive",
                            "Slow hashing improves database performance",
                            "It has no real purpose",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What happens if a JWT's SECRET_KEY leaks?",
                        "options": [
                            "Nothing significant, tokens still expire normally",
                            "An attacker can forge valid tokens for any user id",
                            "Only read access is compromised, never write access",
                            "The API automatically rotates the key",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why is allow_origins=['*'] risky in production?",
                        "options": [
                            "It's actually always the safest option",
                            "Combined with credentialed requests, a wildcard origin is a real security misconfiguration",
                            "It slows down every request significantly",
                            "FastAPI doesn't allow wildcards at all",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "When should pagination be added to a list endpoint?",
                        "options": [
                            "Only after performance problems appear in production",
                            "From day one, for any list that can grow",
                            "Never -- clients should just fetch everything",
                            "Only for endpoints instructors use",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
    ],
}
