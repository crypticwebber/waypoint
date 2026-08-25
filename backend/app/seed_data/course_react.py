COURSE = {
    "title": "Full-Stack Web Development with React",
    "description": (
        "Build real, interactive user interfaces with React: components, "
        "state, effects, and talking to a backend API. By the end you'll "
        "understand not just React's syntax, but the mental model that makes "
        "it click."
    ),
    "category": "Web Development",
    "tags": ["react", "javascript", "frontend", "hooks", "components", "api"],
    "level": "beginner",
    "duration_hours": 11,
    "color": "#2E7D6B",
    "project_brief": (
        "Build a small 'task board' React app: fetch tasks from a provided "
        "mock API, display them grouped by status, let the user add a new "
        "task and mark one complete, and handle the loading and error states "
        "properly. No task manager tutorial copy-paste allowed -- structure "
        "the components yourself."
    ),
    "modules": [
        {
            "title": "Thinking in components",
            "description": "Why React is built around components, and how to break a UI into them.",
            "lessons": [
                {
                    "title": "What a component actually is",
                    "estimated_minutes": 14,
                    "content": """Forget the framework jargon for a second: a React component is just a
JavaScript function that returns a description of what should appear on
screen. That's the whole idea. It takes some input (called **props**) and
returns markup written in JSX, a syntax extension that lets you write
HTML-like structure directly inside JavaScript.

```jsx
function TaskCard({ title, isDone }) {
  return (
    <div className="task-card">
      <span>{title}</span>
      {isDone && <span className="badge">Done</span>}
    </div>
  );
}
```

Two things to notice immediately. First, `{ title, isDone }` destructures
the props object -- `<TaskCard title="Buy milk" isDone={false} />` is how a
parent would render this. Second, curly braces `{}` inside JSX drop you
back into plain JavaScript -- `{title}` inserts the value, and
`{isDone && <span>...}` is a common idiom for "render this only if the
condition is true," relying on the fact that `false && anything` evaluates
to `false`, which React simply renders as nothing.

Components compose: a `TaskCard` renders inside a `TaskList`, which renders
inside a `Page`. This is the core mental shift from older, imperative DOM
manipulation (`document.getElementById(...).innerHTML = ...`) to React's
declarative style: instead of writing step-by-step instructions for how to
*change* the DOM, you describe what the UI should look like for a given set
of data, and React figures out the DOM changes for you.

The practical skill this module builds -- and the one that separates clean
React code from tangled React code -- is breaking a design into the right
components in the first place, *before* writing any state or logic.""",
                },
                {
                    "title": "Props, and passing data down",
                    "estimated_minutes": 13,
                    "content": """Data flows one direction in React: down, from parent to child, via props.
A component never reaches "up" into its parent to grab data directly --
instead, the parent passes down whatever the child needs.

```jsx
function TaskList({ tasks }) {
  return (
    <ul>
      {tasks.map((task) => (
        <TaskCard key={task.id} title={task.title} isDone={task.isDone} />
      ))}
    </ul>
  );
}
```

That `key={task.id}` is not optional decoration -- React uses `key` to track
which array item is which across re-renders, so it can update, reorder, or
remove the right DOM nodes instead of tearing down and rebuilding the whole
list every time. Using the array index as a key (`key={index}`) works for
static lists but causes real bugs the moment items can be reordered,
inserted, or removed, because the index no longer reliably identifies the
same logical item -- always prefer a stable, unique ID from your data when
one exists.

Props are read-only from the child's perspective -- a component should
never modify its own props directly. If a child needs to change something
that lives in a parent (say, a "mark complete" button inside `TaskCard`),
the parent passes down a *function* as a prop, and the child calls it:

```jsx
function TaskCard({ title, isDone, onToggle }) {
  return (
    <div className="task-card">
      <span>{title}</span>
      <button onClick={onToggle}>{isDone ? "Undo" : "Complete"}</button>
    </div>
  );
}
```

This "pass a callback down, call it up" pattern is how React keeps data
flow predictable even as an app grows: you can always trace where a piece
of data lives and which component is allowed to change it, because the
answer is always "wherever it was defined, passed down from there." """,
                },
                {
                    "title": "Rendering lists and conditionals cleanly",
                    "estimated_minutes": 13,
                    "content": """Two patterns cover nearly every real-world rendering situation you'll hit,
and it's worth having both memorized rather than reinvented each time.

**Lists** use `.map()`, since JSX can render an array of elements directly:

```jsx
<ul>
  {tasks.map((task) => (
    <li key={task.id}>{task.title}</li>
  ))}
</ul>
```

**Conditionals** don't have a dedicated JSX syntax (there's no `<if>` tag),
so you reach for plain JavaScript expressions instead. Three idioms cover
almost every case:

```jsx
{isLoading && <Spinner />}                          // render only if true
{error ? <ErrorBanner message={error} /> : <TaskList tasks={tasks} />}  // either/or
{tasks.length === 0 ? <EmptyState /> : <TaskList tasks={tasks} />}       // empty state
```

That third pattern matters more than it looks in a beginner project:
a real, production-feeling app never leaves a list silently blank when
there's no data -- it tells the user *why* it's blank ("No tasks yet --
add one below") and what to do about it. The same discipline applies to
loading and error states: a bare "Loading..." with no visual structure, or
a blank screen when a fetch fails, is one of the fastest ways a UI reads as
a student project instead of a real product.

A subtle but important rule: never call `.map()` (or do any other
conditional logic) with a Hook inside it -- Hooks like `useState` have to
be called in the exact same order on every render, so they can never live
inside loops, conditions, or nested functions. This becomes very relevant
the moment you start using state, which is the subject of the next
module.""",
                },
            ],
            "quiz": {
                "title": "Components Check",
                "questions": [
                    {
                        "question_text": "Fundamentally, what is a React component?",
                        "options": [
                            "A CSS file",
                            "A JavaScript function that returns JSX describing the UI",
                            "A special HTML tag",
                            "A database table",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Which direction does data flow via props in React?",
                        "options": ["Child to parent", "Parent to child", "Sideways between siblings", "It flows both ways automatically"],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why is using the array index as a list `key` risky?",
                        "options": [
                            "React doesn't allow numeric keys",
                            "It breaks if items are reordered, inserted, or removed",
                            "It makes the app slower in all cases",
                            "It's actually always safe to use",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "How does a child component change something owned by its parent?",
                        "options": [
                            "It modifies the parent's props directly",
                            "It calls a callback function the parent passed down as a prop",
                            "It's not possible in React",
                            "It imports the parent component",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "State and interactivity",
            "description": "useState, event handling, and how React decides when to re-render.",
            "lessons": [
                {
                    "title": "useState: giving a component memory",
                    "estimated_minutes": 15,
                    "content": """Props let data flow in, but a component often needs to track something
that changes over time *on its own* -- whether a checkbox is checked, what
text is in an input, whether a menu is open. That's what `useState` is for:
it gives a component its own local, persistent memory.

```jsx
import { useState } from "react";

function TaskCard({ title }) {
  const [isDone, setIsDone] = useState(false);

  return (
    <div>
      <span>{title}</span>
      <button onClick={() => setIsDone(!isDone)}>
        {isDone ? "Undo" : "Complete"}
      </button>
    </div>
  );
}
```

`useState(false)` returns a pair: the current value (`isDone`) and a
function to update it (`setIsDone`). Calling `setIsDone(...)` does two
things: it updates the stored value, *and* it tells React to re-render this
component (and its children) with the new value. This is the fundamental
loop React runs on: state changes trigger re-renders, re-renders produce
new JSX, React compares it to what's currently on screen, and updates only
the DOM nodes that actually changed.

Critically, calling `setIsDone` does **not** immediately change `isDone`
within the current function call -- state updates are scheduled, and the
component re-runs with the new value on the *next* render. Code written
like `setIsDone(!isDone); console.log(isDone);` will log the *old* value,
which surprises nearly every beginner exactly once.

When a new state value depends on the previous one, pass a function
instead of a value to avoid subtle bugs from stale values, especially when
multiple updates happen close together:

```jsx
setCount((prevCount) => prevCount + 1);
```

This "updater function" form guarantees you're always building on the
latest state, rather than a value that might be stale by the time React
actually applies the update.""",
                },
                {
                    "title": "Handling forms and user input",
                    "estimated_minutes": 14,
                    "content": """Forms are the most common source of interactive state in real apps, and
React has a standard pattern for them: **controlled components**, where the
input's displayed value is driven entirely by state, and every keystroke
updates that state.

```jsx
function AddTaskForm({ onAdd }) {
  const [title, setTitle] = useState("");

  function handleSubmit(event) {
    event.preventDefault();     // stop the browser's default full-page reload
    if (title.trim() === "") return;
    onAdd(title);
    setTitle("");                // clear the input after submitting
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        placeholder="New task"
      />
      <button type="submit">Add</button>
    </form>
  );
}
```

`event.preventDefault()` is easy to forget and produces a confusing bug
when you do: the browser's native form submission triggers a full page
reload, which wipes out all your React state instantly, making it look
like your click handler "did nothing."

Notice the validation (`if (title.trim() === "") return`) happens *before*
calling `onAdd`, not after -- catching invalid input as early as possible,
right where the user action occurred, is what makes an interface feel
responsive and forgiving rather than one that silently accepts bad input
and fails somewhere else later.

This form doesn't own the list of tasks itself -- it receives `onAdd` as a
prop and calls it, following the same "pass a callback down" pattern from
the previous module. The parent component that actually owns the task list
in its state decides what "adding a task" means; the form's only job is
collecting and validating the input.""",
                },
                {
                    "title": "useEffect and fetching data from an API",
                    "estimated_minutes": 15,
                    "content": """Rendering describes *what* the UI looks like for the current state --
but some things (fetching data, subscribing to a timer, reading from
`localStorage`) are **side effects**: they reach outside the component to
interact with the world. `useEffect` is React's tool for running that kind
of code at the right moment, separate from rendering itself.

```jsx
import { useState, useEffect } from "react";

function TaskBoard() {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/tasks")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load tasks");
        return res.json();
      })
      .then((data) => setTasks(data))
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);   // empty dependency array = run once, after the first render

  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner message={error} />;
  return <TaskList tasks={tasks} />;
}
```

The second argument to `useEffect`, the **dependency array**, controls when
the effect re-runs. An empty array `[]` means "run once, right after the
first render, and never again" -- exactly right for an initial data fetch.
If you instead depend on a variable (`[userId]`), the effect re-runs every
time that value changes -- useful when, say, switching users should trigger
a fresh fetch.

Two mistakes account for most `useEffect` bugs beginners hit: forgetting
the dependency array entirely (causing the effect to re-run after *every*
render, potentially triggering an infinite fetch loop if the effect itself
updates state that's also in scope), and omitting a value the effect
actually uses from the dependency array (causing it to silently use a
stale, outdated value). The properly handled loading/error states above
aren't optional polish, either -- a network request that never gets a
loading indicator or an error path is a UI that appears to just freeze or
silently fail the moment the network hiccups.""",
                },
            ],
            "quiz": {
                "title": "State & Interactivity Check",
                "questions": [
                    {
                        "question_text": "What two things does calling a useState setter function do?",
                        "options": [
                            "Nothing until the page is refreshed",
                            "Updates the stored value and schedules a re-render",
                            "Only updates the value, never re-renders",
                            "Deletes the component",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why use the updater-function form setCount(prev => prev + 1) instead of setCount(count + 1)?",
                        "options": [
                            "It's required syntax in all cases",
                            "It guarantees you're building on the latest state, avoiding stale-value bugs",
                            "It's purely stylistic with no real difference",
                            "It makes the component render faster",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What happens if you forget event.preventDefault() in a form's submit handler?",
                        "options": [
                            "Nothing, it's optional",
                            "The browser does a full page reload, wiping React state",
                            "The form silently fails to render",
                            "React throws a compile error",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does an empty dependency array [] mean for useEffect?",
                        "options": [
                            "The effect never runs",
                            "The effect runs after every single render",
                            "The effect runs once, after the first render",
                            "The effect only runs on unmount",
                        ],
                        "correct_index": 2,
                    },
                ],
            },
        },
        {
            "title": "Building a real, connected app",
            "description": "Component structure at scale, routing, and talking to a backend properly.",
            "lessons": [
                {
                    "title": "Lifting state up and structuring a real app",
                    "estimated_minutes": 15,
                    "content": """As soon as two sibling components need to share or coordinate the same
piece of state -- say, a filter dropdown and a task list that both need to
know the current filter -- that state can't live in either child alone.
The fix is **lifting state up**: move it to the nearest common ancestor,
and pass it (and the setter functions to change it) down as props to both
children.

```jsx
function TaskBoard() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");

  const visibleTasks = tasks.filter((task) =>
    filter === "all" ? true : task.status === filter
  );

  return (
    <div>
      <FilterBar filter={filter} onFilterChange={setFilter} />
      <TaskList tasks={visibleTasks} />
    </div>
  );
}
```

Note that `visibleTasks` is computed fresh on every render from `tasks` and
`filter` -- it's *not* stored in its own `useState`. This is a genuinely
important habit: if a value can be calculated directly from existing state,
calculate it during render instead of duplicating it into another state
variable. Storing it separately creates two sources of truth that can drift
out of sync (you'd have to remember to update `visibleTasks` every time
`tasks` *or* `filter` changes) -- deriving it fresh avoids that class of bug
entirely.

As an app grows past a handful of components, resist the urge to keep
piling logic into one giant component. A `TaskBoard` that fetches data,
filters it, renders a form, AND renders the list is doing four jobs. Split
along those natural seams -- a custom hook for the data-fetching logic
(`useTasks()`), and separate presentational components for the form and
list -- and each piece becomes independently readable, testable, and
reusable.""",
                },
                {
                    "title": "Client-side routing with React Router",
                    "estimated_minutes": 14,
                    "content": """A single-page app still needs multiple "pages" -- a catalog view, a detail
view, a dashboard -- without triggering a full browser reload between them
(which would throw away all your React state and feel noticeably slower).
React Router solves this by matching the URL to a component entirely on
the client side.

```jsx
import { BrowserRouter, Routes, Route, Link, useNavigate, useParams } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CourseCatalog />} />
        <Route path="/courses/:courseId" element={<CourseDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

Inside `CourseDetail`, `useParams()` reads the dynamic segment of the URL:

```jsx
function CourseDetail() {
  const { courseId } = useParams();
  // fetch course data using courseId inside a useEffect, as covered earlier
}
```

Navigation happens two ways: declaratively with `<Link to="/courses/3">`
for anything the user clicks (which renders as a real `<a>` tag, so
right-click-to-open-in-new-tab still works correctly, unlike a plain
`onClick` handler would), and imperatively with the `useNavigate()` hook
for navigation triggered by code -- for example, redirecting to a dashboard
immediately after a successful login.

The `path="*"` catch-all route matters more than it seems: without it, a
mistyped or stale URL renders nothing at all, which is a worse experience
than a clear "page not found" message with a way back to somewhere useful
-- the same "never leave the user looking at a blank screen" principle from
loading and error states applies just as much to routing.""",
                },
                {
                    "title": "Talking to a backend the right way",
                    "estimated_minutes": 15,
                    "content": """Every meaningful React app eventually needs to read and write data through
a backend API. A few habits separate a fragile integration from a solid
one.

**Centralize your API calls.** Don't scatter raw `fetch()` calls across
every component -- wrap them in one module so the base URL, auth headers,
and error handling live in exactly one place.

```jsx
// api.js
const BASE_URL = "http://localhost:8000";

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}
```

Every component that needs data now calls `apiFetch("/courses")` instead of
repeating headers and error-handling boilerplate everywhere -- and if the
auth scheme or base URL ever changes, there's exactly one place to update
it.

**Treat every request as having three states**, and render all three:
loading, error, and success -- exactly the pattern from the `useEffect`
lesson, applied consistently across the whole app rather than as a one-off.
A skipped error state isn't a small omission -- it's the difference between
a user seeing "Couldn't load your courses, try again" and a user seeing a
UI that looks broken with no explanation.

**Don't trust client-side validation alone.** Form validation in the
browser is for user experience -- catching mistakes early and giving
immediate feedback -- but the backend must independently validate
everything too, since a request can always be sent directly to the API,
bypassing your UI entirely. This is a security boundary, not just a code
style preference: the frontend's job is to make the common case pleasant,
and the backend's job is to make the system correct regardless of what the
frontend did or didn't check.""",
                },
            ],
            "quiz": {
                "title": "Building a Real App Check",
                "questions": [
                    {
                        "question_text": "What does 'lifting state up' mean?",
                        "options": [
                            "Moving state into a global variable",
                            "Moving shared state to the nearest common ancestor component",
                            "Storing state in the browser's URL",
                            "Deleting unused state variables",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why compute a derived value like visibleTasks during render instead of storing it in its own useState?",
                        "options": [
                            "Storing it is always faster",
                            "Deriving it avoids two sources of truth that could drift out of sync",
                            "useState can't hold arrays",
                            "It has no real effect either way",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does useParams() give you in React Router?",
                        "options": [
                            "The current scroll position",
                            "Dynamic segments of the current URL, like an ID in the path",
                            "The browser's local storage",
                            "A list of all defined routes",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why must a backend validate input even if the frontend already validates it?",
                        "options": [
                            "It doesn't need to if the frontend already checked",
                            "Requests can bypass the frontend entirely, so the backend is the real security boundary",
                            "Backend validation is only for performance",
                            "Frontend validation is always sufficient",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
    ],
}
