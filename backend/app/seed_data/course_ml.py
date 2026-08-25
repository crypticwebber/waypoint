COURSE = {
    "title": "Machine Learning Foundations",
    "description": (
        "A practical, code-first introduction to supervised machine learning: "
        "how models actually learn from data, how to tell whether one is any "
        "good, and how to avoid the mistakes that quietly invalidate most "
        "beginner ML projects."
    ),
    "category": "Data Science",
    "tags": ["machine learning", "scikit-learn", "regression", "classification", "overfitting"],
    "level": "intermediate",
    "duration_hours": 10,
    "color": "#D9695A",
    "project_brief": (
        "Using a provided housing dataset, build a regression model that "
        "predicts sale price from house features. Correctly split your data, "
        "try at least two different model types, evaluate both with an "
        "appropriate metric, and write a short report explaining which model "
        "you'd actually deploy and why -- including one thing that could make "
        "it fail in production."
    ),
    "modules": [
        {
            "title": "How models learn",
            "description": "The core idea behind supervised learning, from linear regression to loss functions.",
            "lessons": [
                {
                    "title": "What 'learning' means for a machine",
                    "estimated_minutes": 15,
                    "content": """Supervised machine learning is, at its core, function approximation from
examples. You have inputs (**features**, X) and known correct outputs
(**labels**, y), and you want an algorithm to find a function f such that
f(X) ≈ y closely enough to be useful on *new* inputs it hasn't seen.

The simplest possible version of this is linear regression: assume the
relationship is a weighted sum of the inputs, f(X) = w1*x1 + w2*x2 + ... + b,
and search for the weights (w) and bias (b) that make predictions closest
to the true labels across your training examples.

"Closest" needs a precise definition, which is what a **loss function**
gives you. For regression, the standard choice is mean squared error:

```python
import numpy as np

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

Training a model means searching for the weights that minimize this loss.
You will almost never write that search loop by hand -- scikit-learn does
it for you -- but understanding that "training" literally means "numerically
minimizing a loss function over your training examples" demystifies
everything that follows, including why more data, better features, and a
better-chosen model all help: they all change the shape of that
optimization problem.

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)          # this is where "learning" happens
predictions = model.predict(X_test)   # applying the learned function
```

Everything else in this course -- classification, evaluation, avoiding
overfitting -- is really just refinements and cautions layered on top of
this same fit-then-predict pattern.""",
                },
                {
                    "title": "Regression vs. classification",
                    "estimated_minutes": 14,
                    "content": """The single most important early decision in any ML problem is which of
these two tasks you actually have, because it determines which models,
metrics, and even loss functions are valid.

**Regression** predicts a continuous number: a house price, a temperature,
a delivery time. **Classification** predicts a category from a fixed set:
spam or not spam, which of five product categories, which digit (0-9) an
image shows.

The same underlying idea -- a model f(X) that approximates a target -- applies
to both, but the target's nature changes everything downstream. You
wouldn't use mean squared error to evaluate whether a model correctly
classified an email as spam (there's no meaningful "distance" between the
categories "spam" and "not spam"), and you wouldn't use accuracy to
evaluate a house-price prediction (being "exactly right" on a continuous
number essentially never happens, and being $500 off is very different
from being $500,000 off).

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

clf = LogisticRegression()
clf.fit(X_train, y_train)
clf.predict(X_test)          # returns class labels
clf.predict_proba(X_test)     # returns probability per class
```

Despite the name, `LogisticRegression` is a classification algorithm, not a
regression one -- it models the *probability* of each class, then applies a
threshold. This naming quirk trips up almost every beginner at least once,
so it's worth committing to memory early: if your target is a category,
you're doing classification, no matter what the algorithm's name contains.

Some algorithms -- decision trees, random forests, gradient boosting,
k-nearest-neighbors, neural networks -- come in both a `Regressor` and a
`Classifier` flavor in scikit-learn precisely because the *mechanism* can
work for either task; it's the loss function and evaluation that differ.""",
                },
                {
                    "title": "Features: the inputs that actually drive predictions",
                    "estimated_minutes": 15,
                    "content": """A model is only as good as the features you give it. Two preparation steps
matter for nearly every dataset before it's ready for scikit-learn.

**Encoding categorical variables.** Models operate on numbers, so a text
column like `neighborhood` has to be converted. One-hot encoding creates
one binary column per category:

```python
import pandas as pd

X = pd.get_dummies(X, columns=["neighborhood"], drop_first=True)
```

`drop_first=True` drops one category to avoid redundant, perfectly
correlated columns (if you know a row isn't "downtown" and isn't
"suburb," and those were the only two categories, you already know it's
the third -- keeping all three columns wastes a degree of freedom and can
destabilize some models).

**Scaling numeric features.** Many algorithms (though notably *not*
tree-based ones) are sensitive to the scale of inputs. A feature ranging
0-1,000,000 (square footage in some unit) will dominate a feature ranging
0-10 (number of bedrooms) purely because of its scale, not because it's
actually more predictive.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)   # note: transform, not fit_transform
```

That last comment matters more than it looks: you `fit` the scaler *only*
on training data, then `transform` (not re-fit) both training and test
data with those same learned parameters. Fitting on the full dataset before
splitting is one of the most common ways beginners accidentally leak
information from the test set into training -- a mistake subtle enough that
your model will look great in evaluation and then underperform in the
real world.""",
                },
            ],
            "quiz": {
                "title": "How Models Learn Check",
                "questions": [
                    {
                        "question_text": "What does 'training' a model mean, mechanically?",
                        "options": [
                            "Copying the training data into the model's memory",
                            "Numerically searching for parameters that minimize a loss function",
                            "Randomly guessing until accuracy reaches 100%",
                            "Sorting the dataset by the target column",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Despite its name, what kind of task is LogisticRegression used for?",
                        "options": ["Regression", "Classification", "Clustering", "Dimensionality reduction"],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why should you fit a StandardScaler only on the training set?",
                        "options": [
                            "It's faster that way",
                            "Fitting on the full dataset leaks test-set information into training",
                            "scikit-learn requires it by law",
                            "It has no real effect either way",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does drop_first=True do in pd.get_dummies?",
                        "options": [
                            "Deletes the first row of the dataset",
                            "Removes one redundant category column to avoid perfect correlation",
                            "Drops all categorical columns",
                            "Sorts categories alphabetically",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Evaluating models honestly",
            "description": "Train/test splits, metrics that match the task, and why accuracy can lie to you.",
            "lessons": [
                {
                    "title": "Train/test splits and why they're non-negotiable",
                    "estimated_minutes": 14,
                    "content": """If you evaluate a model on the same data it was trained on, you're not
measuring how well it generalizes -- you're measuring how well it
memorized. A model can achieve near-perfect training accuracy while being
useless on new data, and the only way to catch that is to test on data the
model never saw during training.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

`test_size=0.2` holds out 20% of the data purely for evaluation.
`random_state=42` fixes the random split so your results are reproducible
-- without it, re-running the same code gives you a different split and
slightly different numbers every time, which makes debugging and comparing
models unnecessarily noisy.

For datasets where the target is imbalanced (say, 95% "not fraud," 5%
"fraud"), a plain random split can accidentally put almost none of the
minority class in your test set. `stratify=y` fixes this by preserving the
class proportions in both splits:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

The discipline this builds is simple but easy to skip under time pressure:
every single preprocessing decision -- scaling, encoding, feature selection
-- has to be *fit* on the training set only, then *applied* to the test
set, never the other way around. The test set exists to simulate data your
model hasn't seen yet; the moment any information from it leaks into
training, that simulation is no longer honest.""",
                },
                {
                    "title": "Classification metrics: why accuracy alone is dangerous",
                    "estimated_minutes": 16,
                    "content": """Imagine a fraud-detection dataset where 99% of transactions are legitimate.
A model that predicts "not fraud" for *every single transaction* scores
99% accuracy -- while being completely useless. This is why accuracy alone
is a dangerous metric on imbalanced data, and why classification has a
richer set of metrics built specifically around this problem.

**Precision**: of everything the model flagged as positive, what fraction
was actually positive? High precision means few false alarms.

**Recall**: of everything that was actually positive, what fraction did
the model catch? High recall means few missed cases.

There's an inherent tension between them -- a model that flags everything as
fraud has perfect recall (it caught every real case) and terrible precision
(almost every flag is wrong). Which one matters more depends entirely on
the cost of each type of mistake: missing a real fraud case (low recall) is
often far more costly than investigating a false alarm (low precision), but
for a spam filter it's often the reverse -- a missed spam email is a minor
annoyance, while a legitimate email wrongly binned as spam can be a real
problem.

```python
from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
```

The **confusion matrix** breaks predictions into true positives, false
positives, true negatives, and false negatives -- the raw counts that
precision and recall are computed from -- and is worth reading directly
rather than jumping straight to the summary metrics, because it shows you
*which* kind of mistake your model is actually making.

**F1 score** is the harmonic mean of precision and recall, useful as a
single number when you need one but don't have a strong reason to weight
one over the other.""",
                },
                {
                    "title": "Regression metrics and cross-validation",
                    "estimated_minutes": 15,
                    "content": """Regression has its own metric family, all built around "how far off was
the prediction," but each answers a slightly different question.

**MAE (mean absolute error)**: average absolute difference between
prediction and truth, in the original units (e.g., "$14,000 off on
average"). Easy to explain to a non-technical stakeholder.

**RMSE (root mean squared error)**: similar, but squares errors before
averaging, which penalizes large errors disproportionately. A model with
one huge miss and RMSE will look worse than a model with several small
misses, even if their MAE is similar -- useful when big errors are
especially costly.

**R² (coefficient of determination)**: the proportion of variance in the
target your model explains, from roughly 0 (no better than always
predicting the mean) to 1 (perfect). Unlike MAE/RMSE, it's unit-free, which
makes it easier to compare models across different datasets.

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions, squared=False)
r2 = r2_score(y_test, predictions)
```

A single train/test split gives you one estimate of performance, which can
be noisy, especially on smaller datasets -- you might get a good or bad
split just by chance. **K-fold cross-validation** splits the data into k
chunks, trains k times (each time holding out a different chunk as the test
set), and averages the results, giving you a far more reliable estimate:

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring="r2")
print(scores.mean(), scores.std())
```

The standard deviation across folds is worth reporting alongside the mean
-- a model with mean R² 0.85 and std 0.02 is far more trustworthy than one
with the same mean but std 0.20, even though a single lucky split could
make the second model look identical to the first.""",
                },
            ],
            "quiz": {
                "title": "Evaluating Models Check",
                "questions": [
                    {
                        "question_text": "Why is evaluating a model on its own training data misleading?",
                        "options": [
                            "It's technically impossible to do",
                            "It measures memorization, not generalization to new data",
                            "Training data is always smaller than test data",
                            "scikit-learn blocks this by default",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "On a 99%-legitimate fraud dataset, why is accuracy alone dangerous?",
                        "options": [
                            "Accuracy can't be computed on imbalanced data",
                            "A model predicting 'not fraud' for everything scores 99% while being useless",
                            "Accuracy is only defined for regression",
                            "It isn't dangerous, it's the best metric",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does high recall mean in a classifier?",
                        "options": [
                            "Few false alarms",
                            "Few actual positives were missed",
                            "The model trained quickly",
                            "The dataset was balanced",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What is the main benefit of k-fold cross-validation over a single train/test split?",
                        "options": [
                            "It's always faster to compute",
                            "It gives a more reliable performance estimate by averaging over multiple splits",
                            "It removes the need for a test set entirely",
                            "It only works for classification",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Overfitting, underfitting, and model selection",
            "description": "Why more complex isn't always better, and how to choose between models responsibly.",
            "lessons": [
                {
                    "title": "The bias-variance tradeoff",
                    "estimated_minutes": 15,
                    "content": """**Underfitting** happens when a model is too simple to capture the real
pattern in the data -- it performs poorly on both training and test data.
A linear model trying to fit a clearly curved relationship is a classic
example: no matter how much data you give it, a straight line can't
capture a curve.

**Overfitting** happens when a model is complex enough to fit the noise in
the training data, not just the signal -- it performs great on training
data but poorly on new data. A decision tree with no depth limit will
happily create a leaf for nearly every individual training example,
achieving near-perfect training accuracy while learning essentially nothing
generalizable.

```python
from sklearn.tree import DecisionTreeRegressor

shallow = DecisionTreeRegressor(max_depth=3)
deep = DecisionTreeRegressor(max_depth=None)   # unlimited depth
```

The `deep` tree will almost always show much higher training R² than
`shallow` -- and often *lower* test R², which is the signature of
overfitting: training performance up, test performance down, as complexity
increases past the point the data actually supports.

This is the **bias-variance tradeoff**: an underfit model has high bias
(systematically wrong, in a consistent direction) and low variance
(consistent across different training sets); an overfit model has low bias
but high variance (wildly sensitive to exactly which training examples it
saw). The practical goal isn't to eliminate either one -- it's to find the
complexity level where their combined effect on test error is minimized,
which is exactly what comparing train vs. test performance across several
model complexities lets you find.""",
                },
                {
                    "title": "Regularization and hyperparameter tuning",
                    "estimated_minutes": 15,
                    "content": """**Regularization** is a family of techniques that discourage a model from
becoming too complex, directly addressing overfitting. For linear models,
Ridge and Lasso regression add a penalty term to the loss function that
grows with the size of the model's weights -- forcing the model to justify
every weight it uses, rather than freely fitting noise.

```python
from sklearn.linear_model import Ridge, Lasso

ridge = Ridge(alpha=1.0)   # alpha controls penalty strength
lasso = Lasso(alpha=1.0)
```

Lasso has a distinctive extra property: it can shrink weights all the way
to exactly zero, effectively performing feature selection by dropping
features it decides aren't pulling their weight. Ridge shrinks weights
towards zero but rarely to exactly zero, which is preferable when you
believe most features are at least somewhat relevant.

`alpha`, `max_depth`, and similar knobs you set *before* training (as
opposed to weights the model learns *during* training) are called
**hyperparameters**. Choosing them by hand and eyeballing test performance
is a subtle form of the same leakage problem from earlier -- you'd
effectively be fitting to the test set through your own trial and error.
The correct pattern is a validation set (or cross-validation) used
specifically for hyperparameter search, with the test set held out until
the very end for one final, honest evaluation:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0]}
search = GridSearchCV(Ridge(), param_grid, cv=5, scoring="r2")
search.fit(X_train, y_train)
print(search.best_params_)
```

`GridSearchCV` runs cross-validation for every combination of
hyperparameters in the grid and reports which combination performed best
-- automating exactly the search a beginner would otherwise do by hand,
badly.""",
                },
                {
                    "title": "Choosing a model responsibly",
                    "estimated_minutes": 14,
                    "content": """With scikit-learn's consistent `.fit()` / `.predict()` interface, trying
multiple model types is nearly free computationally -- so the real skill
isn't knowing which single algorithm is "best," it's building a fair
comparison and reading the results honestly.

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

models = {
    "linear": LinearRegression(),
    "random_forest": RandomForestRegressor(n_estimators=200, random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")
    print(f"{name}: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

A few things matter more than the leaderboard number:

**Interpretability vs. accuracy.** A linear model's coefficients tell you
directly how each feature affects the prediction; a random forest with 200
trees is far harder to explain to a stakeholder, even if it scores
slightly higher. Whether that tradeoff is worth it depends on the
application -- a model that influences loan approvals has very different
interpretability requirements than one recommending which article to show
next.

**Robustness, not just peak score.** A model whose cross-validation std is
tiny is more trustworthy than one with a slightly higher mean but much
wider std -- the second one got lucky or unlucky depending on the fold,
which means its real-world performance is genuinely uncertain.

**What could make it fail in production.** Real-world data drifts:
distributions shift, new categories appear, sensors get replaced. A model
evaluated only on a single historical test set has told you nothing about
how it degrades over time -- which is exactly the kind of limitation worth
naming explicitly in any report you write about a model, rather than
presenting a single accuracy number as the whole story.""",
                },
            ],
            "quiz": {
                "title": "Overfitting & Model Selection Check",
                "questions": [
                    {
                        "question_text": "What's the signature symptom of overfitting?",
                        "options": [
                            "Poor performance on both training and test data",
                            "High training performance but noticeably lower test performance",
                            "The model trains in under a second",
                            "The model refuses to converge",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What distinctive thing can Lasso regression do that Ridge typically doesn't?",
                        "options": [
                            "Shrink weights exactly to zero, performing feature selection",
                            "Train faster than any other algorithm",
                            "Work without a target variable",
                            "Guarantee zero overfitting",
                        ],
                        "correct_index": 0,
                    },
                    {
                        "question_text": "Why shouldn't you tune hyperparameters by repeatedly checking test-set performance?",
                        "options": [
                            "It's computationally impossible",
                            "It effectively leaks test-set information into your modeling decisions",
                            "scikit-learn disallows it",
                            "Hyperparameters don't affect performance",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why might you choose a less accurate but more interpretable model?",
                        "options": [
                            "Interpretability is always required by law",
                            "Some applications need to explain individual predictions to stakeholders",
                            "Interpretable models always run faster",
                            "There's never a good reason to",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
    ],
}
