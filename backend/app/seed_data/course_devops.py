COURSE = {
    "title": "Cloud & DevOps Essentials",
    "description": (
        "Understand how modern applications actually get built, packaged, "
        "and run in the cloud: containers, CI/CD pipelines, and the core "
        "cloud infrastructure concepts every developer needs, even if "
        "'DevOps' isn't in their job title."
    ),
    "category": "Cloud & DevOps",
    "tags": ["docker", "ci/cd", "cloud", "linux", "infrastructure", "devops"],
    "level": "intermediate",
    "duration_hours": 9,
    "color": "#5B4B8A",
    "project_brief": (
        "Take a small provided web app, write a Dockerfile for it, run it "
        "locally in a container, then write a CI pipeline configuration "
        "(GitHub Actions) that installs dependencies, runs its test suite, "
        "and builds the Docker image on every push -- failing loudly if any "
        "step breaks."
    ),
    "modules": [
        {
            "title": "Containers: packaging software so it actually runs the same everywhere",
            "description": "Why Docker exists, and how to write a real, correct Dockerfile.",
            "lessons": [
                {
                    "title": "\"It works on my machine\" and why containers exist",
                    "estimated_minutes": 14,
                    "content": """Every developer eventually hits this: code runs fine locally, then breaks
the moment it's deployed, because the production server has a different OS
version, a different Python version, or a missing system library that was
quietly installed on your laptop months ago and forgotten. **Containers**
solve this by packaging an application together with its entire runtime
environment -- system libraries, language runtime, dependencies -- into one
portable unit that behaves identically wherever it runs.

This is different from a virtual machine, and the difference matters
practically: a VM virtualizes an entire operating system, including its own
kernel, which is heavy (gigabytes, minutes to boot). A container shares the
host machine's kernel and only isolates the application layer, which makes
it dramatically lighter (megabytes, sub-second start time) while still
providing strong isolation between what's inside the container and what's
on the host.

**Docker** is the tool that made containers mainstream, built around two
core concepts. An **image** is a read-only, versioned snapshot -- your
application code plus everything it needs to run -- built once from
instructions in a `Dockerfile`. A **container** is a running instance of an
image, the same relationship a class has to an object in object-oriented
programming: you can start many containers from one image, each an
independent, isolated running process.

```bash
docker build -t my-app:1.0 .
docker run -p 8000:8000 my-app:1.0
```

`docker build` reads a `Dockerfile` and produces an image; `docker run`
starts a container from it, mapping port 8000 inside the container to port
8000 on your machine so you can actually reach it. Everything else in this
module is about writing that `Dockerfile` well.""",
                },
                {
                    "title": "Writing a real Dockerfile",
                    "estimated_minutes": 15,
                    "content": """A `Dockerfile` is a sequence of instructions describing how to build an
image, executed top to bottom. Here's a realistic one for a Python API:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Reading it top to bottom: `FROM` picks a base image to build on top of --
`python:3.12-slim` already has Python installed, so you're not starting
from a completely bare OS. `WORKDIR` sets the working directory inside the
image for every instruction after it. `COPY requirements.txt .` copies just
the dependency list first, `RUN pip install` installs from it, and *only
then* does `COPY . .` copy the rest of the application code.

That ordering is deliberate, not arbitrary, and it's the single most
common thing beginners get backwards. Docker caches each instruction's
result as a layer, and reuses cached layers on rebuild as long as nothing
that instruction depends on has changed. If you copied all your code before
installing dependencies, changing a single line of application code would
invalidate the cache for the `pip install` step too, forcing a full
dependency reinstall on every single rebuild -- turning a few-second
rebuild into a multi-minute one. Copying `requirements.txt` alone first
means the (slow) dependency install layer only re-runs when dependencies
actually change.

`CMD` defines the default command that runs when a container starts from
this image. Using `0.0.0.0` instead of `localhost`/`127.0.0.1` as the host
is essential and easy to miss -- binding to `127.0.0.1` inside a container
only accepts connections from *inside* that same container, making the
`-p 8000:8000` port mapping silently useless.""",
                },
                {
                    "title": "Multi-stage builds and .dockerignore",
                    "estimated_minutes": 14,
                    "content": """Two refinements turn a working Dockerfile into a genuinely production-ready
one.

**`.dockerignore`** works exactly like `.gitignore`, but for what
`COPY . .` includes in the image. Without one, your image build context
includes your local virtual environment, `.git` history, `node_modules`,
and any `.env` files with real secrets in them -- bloating the image size
and, in the case of secrets, creating a genuine security leak baked
directly into the image layers.

```
# .dockerignore
venv/
__pycache__/
.git/
.env
node_modules/
*.pyc
```

**Multi-stage builds** address a different problem: the tools you need to
*build* an application (compilers, dev dependencies, build caches) are
often much larger than what you need to *run* it, and shipping them all in
your final production image is wasted size and unnecessary attack surface.

```dockerfile
FROM node:20 AS build
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

The first stage (`build`) has the full Node toolchain and produces static
files. The second stage starts completely fresh from a tiny `nginx:alpine`
base and copies over *only* the built output (`--from=build /app/dist`) --
none of Node, npm, or the source code make it into the final image at all.
The resulting image can be a fraction of the size of a single-stage
equivalent, which matters directly for deployment speed, storage cost, and
the smaller surface area a smaller image presents for security issues.

This pattern -- build in one throwaway environment, ship only the output --
is worth recognizing as a general principle beyond Docker specifically: the
environment that builds your software rarely needs to be the same one that
runs it.""",
                },
            ],
            "quiz": {
                "title": "Containers Check",
                "questions": [
                    {
                        "question_text": "What's the main practical difference between a container and a virtual machine?",
                        "options": [
                            "Containers can't run web servers",
                            "A container shares the host's kernel and isolates only the app layer, making it much lighter than a VM",
                            "There is no real difference",
                            "VMs are always faster to start",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why copy requirements.txt and run pip install BEFORE copying the rest of the application code?",
                        "options": [
                            "It's required syntax",
                            "It lets Docker cache the dependency-install layer, so it only reruns when dependencies actually change",
                            "It has no effect on build speed",
                            "Docker requires dependencies to be installed first",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why bind a server to 0.0.0.0 instead of 127.0.0.1 inside a container?",
                        "options": [
                            "127.0.0.1 only accepts connections from inside the same container, breaking port mapping from outside",
                            "0.0.0.0 is faster",
                            "There's no real difference in a container",
                            "127.0.0.1 is not valid inside Docker",
                        ],
                        "correct_index": 0,
                    },
                    {
                        "question_text": "What's the main benefit of a multi-stage Docker build?",
                        "options": [
                            "It makes the Dockerfile shorter",
                            "The final image ships only the build output, not the full build toolchain, reducing image size and attack surface",
                            "It removes the need for a .dockerignore file",
                            "It's required for Python apps specifically",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Continuous integration and delivery",
            "description": "Automating tests, builds, and deployments so quality is enforced, not hoped for.",
            "lessons": [
                {
                    "title": "What CI/CD actually solves",
                    "estimated_minutes": 14,
                    "content": """Before CI/CD, "does this change break anything?" was answered by a human
manually running tests (or, worse, not running them) before merging code --
a step that gets skipped under deadline pressure precisely when it matters
most. **Continuous Integration (CI)** automates that check: every push
triggers an automated pipeline that installs dependencies, runs the test
suite, and reports pass/fail, with no human able to accidentally skip it.

**Continuous Delivery/Deployment (CD)** extends this to the release step
itself: once code passes CI, it's automatically packaged (built into a
Docker image, for instance) and, for full Continuous *Deployment*, pushed
live without manual intervention. The distinction between Delivery and
Deployment is one word but a real difference in practice: Delivery means
the release is *ready* to ship at the push of a button; Deployment means it
ships automatically, no button required.

The underlying value proposition is the same for both: catching problems
as early and as cheaply as possible. A bug caught by CI on a pull request
costs a few minutes to fix. The same bug caught by a user in production can
cost hours of incident response, plus the damage of it actually breaking
for real users. CI/CD doesn't eliminate bugs -- it changes *when* you find
out about them, and earlier is almost always cheaper.

This isn't exclusively a "DevOps team" concern. Any developer working on a
team benefits directly: a green checkmark on a pull request, generated
automatically, is a much stronger signal to a reviewer (and to the author)
than "I ran the tests locally and they passed," which nobody else can
verify and which silently stops being true the moment the branch drifts
from what was actually tested.""",
                },
                {
                    "title": "A real GitHub Actions pipeline",
                    "estimated_minutes": 16,
                    "content": """GitHub Actions is a common, widely-used way to run CI pipelines, configured
entirely in YAML files under `.github/workflows/`. Here's a realistic
pipeline for a Python API:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=app

      - name: Build Docker image
        run: docker build -t my-app:${{ github.sha }} .
```

Reading this top to bottom: `on:` defines what triggers the pipeline --
here, every push to `main` and every pull request targeting `main`, which
is the standard pattern (test on every PR *before* merge, and again after
merge as a final safety net). `runs-on` picks the machine image the job
executes on. Each `step` either uses a pre-built reusable **action**
(`actions/checkout`, `actions/setup-python` -- the equivalent of a
well-tested library instead of writing that setup logic yourself) or runs
a shell command directly via `run:`.

The steps are ordered deliberately: checkout code, set up the right
language version, install dependencies, run tests, *then* build the image
-- each step depends on the previous one succeeding. If `pytest` fails, the
pipeline stops immediately and the Docker build never runs, which is
exactly the behavior you want: there's no point packaging code you already
know is broken.

`${{ github.sha }}` is one of many built-in variables GitHub Actions
exposes -- tagging the image with the exact commit hash it was built from
makes every built image traceable back to precisely the code that produced
it, which matters enormously the moment you're debugging "which version is
actually running in production right now." """,
                },
                {
                    "title": "Environment variables, secrets, and config across environments",
                    "estimated_minutes": 14,
                    "content": """A single codebase typically runs in at least three different environments
-- local development, a staging/test deployment, and production -- each
needing different configuration: a different database URL, different API
keys, different feature flags. Hardcoding any of these into source code is
a mistake that compounds badly: it forces a code change (and a full
redeploy) just to update a config value, and worse, it means secrets end up
committed to version control, visible to anyone with repo access, forever,
in the commit history.

The standard fix is **environment variables**: configuration is read from
the environment the process runs in, not from the code itself.

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
SECRET_KEY = os.environ["SECRET_KEY"]   # no default -- fail loudly if missing
```

Notice the deliberate difference between these two lines: `DATABASE_URL`
has a sensible local-development default, so a new developer can clone the
repo and run it immediately without extra setup. `SECRET_KEY` has no
default and uses `os.environ[...]` (which raises a `KeyError` if missing)
rather than `.get(...)` -- for a genuine secret, failing loudly and
immediately at startup is far preferable to silently running with a
missing or default value that could be a real security hole in production.

In CI/CD pipelines specifically, secrets (API keys, deployment credentials)
are stored in the platform's dedicated secrets manager (GitHub Actions'
"Repository secrets," for instance) and injected as environment variables
at runtime -- never written directly into the pipeline YAML file, which is
just as visible in version control as application code would be.

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.DEPLOY_API_KEY }}
  run: ./deploy.sh
```

The broader principle this all serves is called the **twelve-factor app**
methodology's "config" rule: strict separation between code (which should
be identical across environments) and configuration (which should vary by
environment) -- one codebase, many deployments, differentiated purely by
what's in the environment around it, not by what's in the code itself.""",
                },
            ],
            "quiz": {
                "title": "CI/CD Check",
                "questions": [
                    {
                        "question_text": "What does Continuous Integration (CI) primarily automate?",
                        "options": [
                            "Writing the application code itself",
                            "Running tests and checks automatically on every push, without relying on a human to remember",
                            "Designing the database schema",
                            "Writing documentation",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What's the practical difference between Continuous Delivery and Continuous Deployment?",
                        "options": [
                            "There is no difference",
                            "Delivery means ready-to-ship on demand; Deployment means it ships automatically with no manual step",
                            "Delivery only applies to mobile apps",
                            "Deployment happens before testing, Delivery happens after",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why use os.environ['SECRET_KEY'] (no default) instead of os.environ.get('SECRET_KEY', 'default')?",
                        "options": [
                            "Both are exactly equivalent",
                            "For a genuine secret, failing loudly if it's missing is safer than silently running with a default",
                            "The bracket syntax is faster",
                            ".get() doesn't exist in Python",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Where should real secrets used in a CI pipeline be stored?",
                        "options": [
                            "Directly in the workflow YAML file",
                            "In the CI platform's dedicated secrets manager, injected as environment variables",
                            "In a comment in the source code",
                            "In the README",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Core cloud infrastructure concepts",
            "description": "The vocabulary and building blocks behind 'the cloud', independent of any one provider.",
            "lessons": [
                {
                    "title": "Compute, storage, and networking -- the three primitives",
                    "estimated_minutes": 15,
                    "content": """However many services a cloud provider offers -- and AWS alone has several
hundred -- almost everything reduces to three underlying primitives, and
understanding them independent of any one vendor's naming makes every
provider's dashboard easier to navigate.

**Compute** is somewhere your code actually runs. A **virtual machine**
(EC2 on AWS, Compute Engine on GCP) is the most flexible and most
hands-on option -- you manage the OS, patches, and scaling yourself. A
**container platform** (ECS, Cloud Run, Kubernetes) runs your Docker images
directly, handling more of the underlying machine management for you.
**Serverless functions** (Lambda, Cloud Functions) run a single function in
response to an event and scale to zero when idle -- you don't manage a
server at all, and you pay only for actual execution time, not idle
capacity.

**Storage** covers where data lives outside your running application.
**Object storage** (S3, Cloud Storage) holds files -- images, backups,
static assets -- accessed by key, not organized as a traditional
filesystem. A **managed database** (RDS, Cloud SQL) runs a real database
engine (Postgres, MySQL) with the provider handling backups, patching, and
failover for you, versus running the same database yourself on a VM.

**Networking** connects everything together and controls what can reach
what. A **load balancer** distributes incoming traffic across multiple
compute instances, both for scaling (one machine can't handle all the
traffic) and for reliability (if one instance goes down, traffic
automatically routes to the healthy ones). A **VPC** (Virtual Private
Cloud) is an isolated network you define, controlling exactly which
resources can talk to each other and which are reachable from the public
internet at all -- your database, in almost every real setup, should not
be.

Nearly every cloud architecture diagram you'll ever look at is some
combination of these three categories, wired together -- recognizing which
primitive a given box represents is most of what's needed to actually read
one.""",
                },
                {
                    "title": "Scaling, redundancy, and why single points of failure matter",
                    "estimated_minutes": 14,
                    "content": """**Scaling** means handling more load, and it comes in two forms with real
tradeoffs. **Vertical scaling** means making one machine bigger (more CPU,
more RAM) -- simple, but with a hard ceiling (there's a biggest machine you
can rent) and a real availability problem, since that one machine is a
**single point of failure**: if it goes down, everything goes down.
**Horizontal scaling** means adding more machines and distributing load
across them (via a load balancer, from the previous lesson) -- more
complex to set up, but with no hard ceiling and no single point of failure,
since the system keeps running (at reduced capacity) if any one instance
fails.

Modern cloud-native applications default to horizontal scaling wherever
practical, which has a direct design consequence worth internalizing: an
application instance should be **stateless**. If a user's session data is
stored only in that one server's memory, and the load balancer routes
their next request to a *different* instance, that session data is simply
gone. The fix is externalizing state -- session data in a shared cache or
database, uploaded files in object storage, not on a specific instance's
local disk -- so any instance can handle any request, and instances can be
added, removed, or restarted freely without losing anything.

**Redundancy** applies this same "no single point of failure" thinking to
every layer, not just compute: a managed database with automated failover
to a standby replica, data replicated across multiple physical data centers
("availability zones"), a CDN serving static content from many geographic
locations instead of one. The underlying question behind good
infrastructure design is always the same one, asked repeatedly at every
layer: "if this one thing fails right now, what happens?" -- and a good
answer is "the system keeps working, possibly a little slower," not "the
whole application goes down."

This is also, not coincidentally, exactly why the "stateless, twelve-factor"
config discipline from the previous module matters beyond just
convenience -- a stateless app is what actually *makes* horizontal scaling
and redundancy possible in the first place.""",
                },
                {
                    "title": "Observability: knowing what's actually happening in production",
                    "estimated_minutes": 14,
                    "content": """Once an application is running in the cloud, across multiple instances,
you lose the simplest debugging tool a local developer has: just looking at
the terminal it's running in. **Observability** is the practice of
building systems that let you understand what's actually happening inside
a running application from the outside, and it rests on three pillars.

**Logs** are timestamped records of discrete events -- "user 42 logged in,"
"payment failed with error X." Structured logging (emitting logs as JSON
with consistent fields, rather than free-form text) matters enormously at
scale, because it lets you *query* logs ("show me every failed payment for
user 42 in the last hour") rather than grep through walls of text by eye.

**Metrics** are numeric measurements aggregated over time -- requests per
second, average response latency, error rate, CPU usage. Unlike logs
(which record individual events), metrics are built for trends and
alerting: "error rate has been above 5% for the last 10 minutes" is a
metric-based alert that can wake someone up automatically, long before a
human happens to notice a spike buried in a log stream.

**Traces** follow a single request as it moves through multiple services --
essential once an application is split into several communicating pieces
(a common "microservices" pattern), where a slow user-facing request might
actually be caused by a slow downstream call three services away, something
neither logs nor metrics alone make easy to pinpoint.

The practical habit this builds, useful even on a single-server student
project: instrument your application *before* something breaks, not after.
A well-placed log line at every major decision point and error path costs
almost nothing to add while you're already writing that code, and turns "I
have no idea why this failed" into "here's exactly what happened, in
order" the moment something actually does go wrong in front of a real
user.""",
                },
            ],
            "quiz": {
                "title": "Cloud Infrastructure Check",
                "questions": [
                    {
                        "question_text": "Which cloud compute option scales to zero and charges only for actual execution time?",
                        "options": ["A virtual machine", "A container platform", "Serverless functions", "A load balancer"],
                        "correct_index": 2,
                    },
                    {
                        "question_text": "What is the main downside of vertical scaling (making one machine bigger)?",
                        "options": [
                            "It's always more expensive than horizontal scaling",
                            "There's a hard ceiling, and the single machine remains a single point of failure",
                            "It requires containers",
                            "It cannot be automated",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why should an application instance be stateless in a horizontally-scaled system?",
                        "options": [
                            "Stateless apps use less code",
                            "So any instance can handle any request, since a load balancer may route to a different instance next time",
                            "Statelessness is required by all cloud providers",
                            "It has no real benefit",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Which observability pillar is best suited for automated alerting on trends like 'error rate above 5%'?",
                        "options": ["Logs", "Metrics", "Traces", "Backups"],
                        "correct_index": 1,
                    },
                ],
            },
        },
    ],
}
