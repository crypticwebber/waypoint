COURSE = {
    "title": "Python for Data Analysis",
    "description": (
        "Learn to wrangle, clean, and analyze real-world datasets using Python, "
        "pandas, and NumPy. You'll go from reading a messy CSV to producing a "
        "clean, chart-ready dataset, building the exact workflow used by data "
        "analysts every day."
    ),
    "category": "Data Science",
    "tags": ["python", "pandas", "numpy", "data cleaning", "csv", "dataframes"],
    "level": "beginner",
    "duration_hours": 9,
    "color": "#E8A33D",
    "project_brief": (
        "You are handed a raw CSV export of a fictional bike-share system's "
        "trip logs: inconsistent date formats, missing station names, and a "
        "handful of physically impossible trip durations. Clean the dataset, "
        "compute average trip duration by day of week and by station, and "
        "produce a short written summary of your three most interesting "
        "findings, each backed by a number you calculated."
    ),
    "modules": [
        {
            "title": "Getting comfortable with pandas",
            "description": "The DataFrame and Series objects that everything else in this course builds on.",
            "lessons": [
                {
                    "title": "Why pandas, and what a DataFrame actually is",
                    "estimated_minutes": 14,
                    "content": """Most real data analysis starts the same way: you have a table -- rows and
columns, like a spreadsheet -- and you need to filter it, transform it, and
summarize it. Python's built-in lists and dictionaries can technically do
this, but they get painful fast: there's no concept of "a column," no fast
way to filter every row where a condition holds, and no built-in way to
handle missing values. pandas exists to fix exactly this.

A pandas **DataFrame** is a 2-dimensional table: rows have an index, columns
have names and each column has its own data type. A single column pulled out
of a DataFrame is a **Series** -- a 1-dimensional labeled array. Nearly
everything you do in pandas is either "operate on a Series" or "operate on a
DataFrame," so it's worth internalizing the difference early.

```python
import pandas as pd

data = {
    "station": ["Elm St", "Elm St", "Oak Ave", "Oak Ave"],
    "duration_min": [12, 45, 8, 300],
    "rider_type": ["member", "casual", "member", "casual"],
}
df = pd.DataFrame(data)
print(df.dtypes)        # one dtype per column
print(df["duration_min"])   # this is a Series
print(type(df["duration_min"]))  # <class 'pandas.core.series.Series'>
```

Notice that `duration_min` contains a 300 -- five hours on a bike share trip
is almost certainly a data error, not a real trip. Spotting values like that
is the whole game of data cleaning, and it's why we don't just trust a
dataset the moment it loads. Over this module you'll load real files,
inspect them systematically, and start building the habit of asking "does
this number make sense?" before you use it in a calculation.""",
                },
                {
                    "title": "Reading, inspecting, and selecting data",
                    "estimated_minutes": 16,
                    "content": """Real datasets almost never arrive as a Python dict -- they arrive as CSV,
Excel, or JSON files, often with quirks. `pd.read_csv()` is your entry
point, and it has dozens of options for exactly this reason:

```python
df = pd.read_csv("trips.csv", parse_dates=["start_time", "end_time"])
```

Once loaded, don't jump straight into analysis -- inspect first. Three
methods will tell you almost everything you need to know:

```python
df.shape        # (num_rows, num_columns)
df.info()       # column names, dtypes, and non-null counts in one view
df.head(10)     # first 10 rows, so you can eyeball the actual values
df.describe()   # count, mean, std, min/max, quartiles for numeric columns
```

`df.info()` is the most underrated of these -- the "non-null count" column
tells you immediately which columns have missing data, before you've
written a single cleaning step.

Selecting data uses two accessors you should memorize the difference
between: **`.loc`** selects by label (row index / column name), and
**`.iloc`** selects by integer position, regardless of what the labels are.

```python
df.loc[0, "station"]        # value at index label 0, column "station"
df.iloc[0, 0]                # value at row position 0, column position 0
df.loc[df["duration_min"] > 60]   # boolean filtering -- every row where True
```

That last line is the pattern you'll use constantly: a comparison on a
column produces a boolean Series, and passing that boolean Series into
`.loc[]` (or just `df[...]`) keeps only the rows where it's `True`. Chaining
these boolean masks together with `&` (and) and `|` (or) -- each condition
wrapped in parentheses -- is how you build arbitrarily specific filters
without ever writing a `for` loop over rows.""",
                },
                {
                    "title": "Adding, transforming, and dropping columns",
                    "estimated_minutes": 15,
                    "content": """Columns in pandas are created by assignment, and operations on a Series are
**vectorized** -- they apply to every element at once, without an explicit
loop, which is both far faster and far more readable than looping in
Python.

```python
df["duration_hr"] = df["duration_min"] / 60

df["is_long_trip"] = df["duration_min"] > 60

df["station_upper"] = df["station"].str.upper()
```

The `.str` accessor unlocks vectorized string operations (`.str.upper()`,
`.str.strip()`, `.str.contains()`, `.str.split()`), and `.dt` does the same
for datetime columns (`.dt.day_name()`, `.dt.hour`, `.dt.date`). You'll use
both heavily once you start cleaning messy real-world text and timestamp
columns.

For more complex row-by-row logic that doesn't reduce to simple arithmetic,
`.apply()` runs a function across every value in a Series (or every row of
a DataFrame, with `axis=1`):

```python
def classify_duration(minutes):
    if minutes < 10:
        return "short"
    elif minutes < 45:
        return "medium"
    return "long"

df["trip_category"] = df["duration_min"].apply(classify_duration)
```

`.apply()` is flexible but slower than a purely vectorized operation, so
the practical rule is: reach for direct arithmetic or `.str`/`.dt` methods
first, and use `.apply()` when the logic genuinely can't be expressed that
way (like the multi-branch classification above).

Dropping columns you don't need keeps a DataFrame manageable:

```python
df = df.drop(columns=["station_upper"])
```

Note that most pandas operations return a **new** DataFrame rather than
modifying in place -- that's why we reassign `df = df.drop(...)`. This is
deliberate: it makes bugs from accidental in-place mutation much rarer.""",
                },
            ],
            "quiz": {
                "title": "pandas Fundamentals Check",
                "questions": [
                    {
                        "question_text": "What object do you get when you select a single column from a DataFrame, e.g. df['duration_min']?",
                        "options": ["A Python list", "A Series", "A new DataFrame", "A NumPy scalar"],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Which accessor selects rows/columns by integer position rather than by label?",
                        "options": [".loc", ".iloc", ".at", ".select"],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Which method gives you column dtypes and non-null counts in one call?",
                        "options": ["df.describe()", "df.shape", "df.info()", "df.dtypes.sum()"],
                        "correct_index": 2,
                    },
                    {
                        "question_text": "df['duration_min'] > 60 produces what?",
                        "options": [
                            "A single True/False value",
                            "A boolean Series, one value per row",
                            "A filtered DataFrame",
                            "A KeyError",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Cleaning messy real-world data",
            "description": "Missing values, duplicates, inconsistent types, and outliers.",
            "lessons": [
                {
                    "title": "Finding and handling missing values",
                    "estimated_minutes": 15,
                    "content": """Missing data shows up as `NaN` (Not a Number) in pandas, whether the
original gap was a blank cell, a null in a database export, or a parsing
failure. The first step is always to quantify it, not guess at it:

```python
df.isna().sum()                 # count of missing values per column
df.isna().mean() * 100           # percentage missing per column
```

Once you know where the gaps are, you have three real options, and the
right one depends on *why* the data is missing and *how much* is missing:

**Drop rows or columns.** Fine when missingness is rare and random.

```python
df_clean = df.dropna(subset=["station"])       # drop rows missing station
df_clean = df.dropna(axis=1, thresh=len(df)*0.5)  # drop columns >50% empty
```

**Fill with a sensible value.** Appropriate when you can defend the fill
value -- a numeric column might get its median (robust to outliers, unlike
the mean), a categorical column might get an explicit "unknown" label so
you don't silently pretend the value was known.

```python
df["duration_min"] = df["duration_min"].fillna(df["duration_min"].median())
df["station"] = df["station"].fillna("unknown")
```

**Leave it, and account for it downstream.** Sometimes missingness is
itself informative (e.g., a trip with no `end_station` might mean the bike
was never docked -- a real event, not noise). Don't clean away signal.

The trap to avoid is filling missing values *before* you understand why
they're missing. A duration column that's blank because the trip was still
in progress when the data was exported has a very different correct
treatment than one that's blank because of a broken sensor.""",
                },
                {
                    "title": "Duplicates, type coercion, and inconsistent categories",
                    "estimated_minutes": 15,
                    "content": """Two extremely common data-quality issues, and pandas has a purpose-built
tool for each.

**Duplicate rows.** Exact duplicates usually come from a source system
re-sending the same record, or a join that fanned out unexpectedly.

```python
df.duplicated().sum()          # how many exact duplicate rows exist
df = df.drop_duplicates()       # keep the first occurrence by default
df = df.drop_duplicates(subset=["trip_id"])  # dedupe on a key column instead
```

Always check `subset=` duplicates on a natural key (like `trip_id`) in
addition to full-row duplicates -- two rows can differ in one noisy column
while still being the same logical record.

**Wrong dtypes.** A numeric column read in as text (often because of a
stray non-numeric value like `"N/A"` somewhere in the column) silently
breaks arithmetic and sorting. `pd.to_numeric()` and `pd.to_datetime()`
convert explicitly and let you control what happens to unparseable values:

```python
df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")
df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
```

`errors="coerce"` turns anything that can't be parsed into `NaN` instead of
raising -- which turns a silent type-mismatch bug into a normal missing-data
problem you already know how to handle.

**Inconsistent categories.** Free-text fields are notorious for this --
`"Elm St"`, `"elm st"`, and `"Elm Street"` are the same station to a human
but three different values to pandas.

```python
df["station"] = df["station"].str.strip().str.lower()
df["station"] = df["station"].replace({"elm street": "elm st"})
```

`df["station"].value_counts()` is your best diagnostic tool here -- sorting
unique values by frequency makes near-duplicate categories jump out
immediately, especially the low-count ones that are almost always typos.""",
                },
                {
                    "title": "Outliers and sanity-checking your data",
                    "estimated_minutes": 14,
                    "content": """An outlier isn't automatically wrong -- but in most real datasets, extreme
values are disproportionately likely to be data errors rather than
genuinely rare events, so they deserve scrutiny before you trust them.

A quick, robust way to flag numeric outliers is the interquartile range
(IQR) method: anything more than 1.5x the IQR beyond the 25th/75th
percentile is flagged for review.

```python
q1 = df["duration_min"].quantile(0.25)
q3 = df["duration_min"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[(df["duration_min"] < lower) | (df["duration_min"] > upper)]
print(f"{len(outliers)} rows flagged out of {len(df)}")
```

Once flagged, you have to make a *documented* decision, not a silent one:
drop them, cap them at a threshold (`df["duration_min"].clip(upper=180)`),
or investigate whether they're real (a 300-minute bike trip could be a
genuine multi-stop rental, not an error -- you won't know until you check
whether the bike was actually returned and re-rented).

The broader habit this module is building is **sanity checking**: after
every cleaning step, re-run `.describe()` and `.info()` and ask "does this
still look plausible?" A dataset that goes from 10,000 rows to 400 after a
`dropna()` call, or a duration column whose max is now negative, is telling
you something went wrong upstream -- catching that immediately is far
cheaper than catching it after you've already computed and reported
results from it.""",
                },
            ],
            "quiz": {
                "title": "Data Cleaning Check",
                "questions": [
                    {
                        "question_text": "Why is filling missing numeric values with the median often preferred over the mean?",
                        "options": [
                            "The median is always faster to compute",
                            "The median is more robust to outliers than the mean",
                            "pandas doesn't support filling with the mean",
                            "There is no real difference",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does errors='coerce' do in pd.to_numeric()?",
                        "options": [
                            "Raises an exception on any unparseable value",
                            "Silently drops the whole column",
                            "Converts unparseable values to NaN instead of raising",
                            "Rounds values to the nearest integer",
                        ],
                        "correct_index": 2,
                    },
                    {
                        "question_text": "Which pandas method is most useful for spotting near-duplicate category values like 'Elm St' vs 'elm street'?",
                        "options": ["df.describe()", "df['col'].value_counts()", "df.shape", "df.duplicated()"],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "In the IQR outlier method, what defines the lower bound?",
                        "options": [
                            "Q1 - 1.5 * IQR",
                            "The minimum value in the column",
                            "The mean minus one standard deviation",
                            "Q1 divided by 2",
                        ],
                        "correct_index": 0,
                    },
                ],
            },
        },
        {
            "title": "Grouping, aggregating, and reshaping",
            "description": "Turning a clean row-level dataset into summarized answers.",
            "lessons": [
                {
                    "title": "groupby: split, apply, combine",
                    "estimated_minutes": 16,
                    "content": """`groupby()` is arguably the single most useful method in pandas for
analysis, and it follows a three-step mental model: **split** the data into
groups based on a column's values, **apply** a function to each group
independently, then **combine** the results back into one table.

```python
df.groupby("station")["duration_min"].mean()
```

Read that as: split trips into groups by station, take the mean
`duration_min` within each group, combine into one Series indexed by
station. You can group by multiple columns, and aggregate multiple columns
at once with `.agg()`:

```python
df.groupby(["station", "rider_type"])["duration_min"].agg(["mean", "count", "max"])
```

This gives you average, count, and max trip duration for every
station/rider-type combination in a single call -- exactly the kind of
summary table you'd otherwise build with a slow, error-prone loop.

For custom logic that doesn't fit a built-in aggregation, pass a named
function or a dict mapping columns to functions:

```python
df.groupby("station").agg(
    avg_duration=("duration_min", "mean"),
    trip_count=("trip_id", "count"),
)
```

This named-aggregation syntax is worth using over the plain version because
it gives your output columns clean, descriptive names (`avg_duration`,
`trip_count`) instead of the default (which just reuses the aggregation
function's name), which matters the moment you want to chart or export the
result.

A common mistake is grouping on a column that still has messy categories
(remember `"Elm St"` vs `"elm st"` from the previous module) -- always
clean categorical columns *before* grouping on them, or your "one station"
will silently split into several rows in the output.""",
                },
                {
                    "title": "Merging and joining datasets",
                    "estimated_minutes": 15,
                    "content": """Real analysis rarely lives in one table. You might have trip records in one
file and a station reference table (with latitude/longitude and capacity)
in another. `pd.merge()` combines them, and it works exactly like a SQL
join.

```python
stations = pd.read_csv("stations.csv")   # columns: station, lat, lon, capacity

trips_full = pd.merge(
    df, stations,
    left_on="station", right_on="station",
    how="left",
)
```

The `how` parameter controls what happens to rows that don't find a match:
- `"inner"`: keep only rows present in both tables (the default)
- `"left"`: keep all rows from the left table, filling unmatched columns
  from the right table with NaN
- `"right"`: the mirror of left
- `"outer"`: keep every row from both tables

`"left"` is the most common choice in practice -- you usually have one
"primary" table (trips) you don't want to lose rows from, and you're
enriching it with a reference table that may not cover every case.

After any merge, immediately check whether the row count changed
unexpectedly:

```python
print(len(df), len(trips_full))
```

If `trips_full` has *more* rows than `df`, your join key had duplicates on
the right-hand side (a station appearing twice in `stations.csv`) and the
join fanned out -- a bug you want to catch before it silently inflates
every downstream count and average.""",
                },
                {
                    "title": "Pivot tables and preparing data for charts",
                    "estimated_minutes": 14,
                    "content": """A pivot table reshapes a long, row-per-observation table into a wide
summary grid -- exactly the shape most charting tools want. `pd.pivot_table`
is `groupby` plus reshaping in one call:

```python
pivot = pd.pivot_table(
    df,
    values="duration_min",
    index="day_of_week",
    columns="rider_type",
    aggfunc="mean",
)
```

This produces a table with one row per day of week, one column per rider
type, and the average duration in each cell -- ready to hand directly to a
plotting library or export as a small, readable CSV, instead of a long
table you'd have to reshape by hand.

Before exporting or charting, it's worth explicitly ordering categorical
axes so they read naturally rather than alphabetically -- "Monday" through
"Sunday" alphabetically starts with "Friday," which is a real and common
gotcha:

```python
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = pivot.reindex(day_order)
```

Finally, `.to_csv()` writes any DataFrame back out, which is how you hand
off a cleaned, summarized dataset to a teammate, a BI tool, or -- for this
course's project -- your own written analysis:

```python
pivot.to_csv("avg_duration_by_day_and_rider.csv")
```

That's the full pipeline this module builds toward: read messy data, clean
it, group and merge it into an answerable shape, and export a small,
trustworthy summary table -- the exact workflow a working data analyst
repeats daily, just with different columns each time.""",
                },
            ],
            "quiz": {
                "title": "Grouping & Reshaping Check",
                "questions": [
                    {
                        "question_text": "What are the three conceptual steps behind groupby()?",
                        "options": [
                            "Sort, filter, export",
                            "Split, apply, combine",
                            "Read, clean, merge",
                            "Index, pivot, plot",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Which merge 'how' keeps every row from the left table, even those with no match on the right?",
                        "options": ["inner", "outer", "left", "cross"],
                        "correct_index": 2,
                    },
                    {
                        "question_text": "If a merge unexpectedly increases your row count, what's the most likely cause?",
                        "options": [
                            "pandas added extra rows automatically",
                            "Duplicate join-key values on one side caused a fan-out",
                            "The CSV file was read twice",
                            "This can never happen with pd.merge",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does pd.pivot_table primarily do?",
                        "options": [
                            "Removes duplicate rows",
                            "Reshapes long data into a wide summary grid via grouping",
                            "Converts a DataFrame to a NumPy array",
                            "Downloads data from a URL",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
    ],
}
