"""Rebuilt Core Analytics modules.

This file contains the five non-statistics companion modules. Together with
`core_analytics_statistics.py`, Core Analytics exports six 30-lesson mini-courses.
The goal is not to make every lesson perfect in one pass; it is to make every live
module follow the same serious structure Hack asked for: gradual sequencing,
financial analysis context, code-first work, math or tool reasoning beside the code,
connected practice, and executable challenges.
"""


COMMON_FINANCIAL_PYTHON = """transactions = [
    {"account": "A101", "segment": "student", "balance": 1200.0, "payment": 180.0, "default": 0},
    {"account": "A102", "segment": "prime", "balance": 3400.0, "payment": 620.0, "default": 0},
    {"account": "A103", "segment": "near_prime", "balance": 2100.0, "payment": 260.0, "default": 1},
    {"account": "A104", "segment": "prime", "balance": 4100.0, "payment": 760.0, "default": 0},
    {"account": "A105", "segment": "student", "balance": 900.0, "payment": 90.0, "default": 1},
]
"""


COMMON_PANDAS_DATA = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "account": ["A101", "A102", "A103", "A104", "A105", "A106", "A107", "A108"],
    "segment": ["student", "prime", "near_prime", "prime", "student", "near_prime", "prime", "student"],
    "month": pd.to_datetime(["2026-01-31", "2026-01-31", "2026-01-31", "2026-02-28", "2026-02-28", "2026-02-28", "2026-03-31", "2026-03-31"]),
    "balance": [1200, 3400, 2100, 4100, 900, 2500, 3900, 1300],
    "payment": [180, 620, 260, 760, 90, 330, 700, 210],
    "revenue": [42, 118, 73, 142, 30, 88, 135, 45],
    "cost": [18, 44, 35, 53, 16, 40, 50, 20],
    "default_flag": [0, 0, 1, 0, 1, 0, 0, 0],
})
financials["margin"] = (financials["revenue"] - financials["cost"]) / financials["revenue"]
"""


COMMON_SQL_DATA = """import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    segment TEXT NOT NULL,
    opened_month TEXT NOT NULL
);
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    balance REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
INSERT INTO customers VALUES
    (1, 'student', '2026-01'),
    (2, 'prime', '2026-01'),
    (3, 'near_prime', '2026-02'),
    (4, 'prime', '2026-02');
INSERT INTO accounts VALUES
    (101, 1, 1200, 'active'),
    (102, 2, 3400, 'active'),
    (103, 3, 2100, 'delinquent'),
    (104, 4, 4100, 'active');
INSERT INTO transactions VALUES
    (1001, 101, '2026-01', 180, 'payment'),
    (1002, 102, '2026-01', 620, 'payment'),
    (1003, 103, '2026-02', 260, 'payment'),
    (1004, 104, '2026-02', 760, 'payment'),
    (1005, 103, '2026-02', -45, 'fee'),
    (1006, 101, '2026-03', 210, 'payment');
''')
"""


COMMON_ML_DATA = """import numpy as np
import pandas as pd

loans = pd.DataFrame({
    "income": [42000, 88000, 61000, 39000, 72000, 98000, 55000, 47000, 83000, 36000],
    "debt_ratio": [0.41, 0.22, 0.35, 0.58, 0.29, 0.18, 0.46, 0.52, 0.25, 0.61],
    "payment_history": [0.82, 0.97, 0.88, 0.61, 0.91, 0.99, 0.74, 0.68, 0.95, 0.57],
    "balance": [1200, 3400, 2100, 900, 2500, 4100, 1800, 1300, 3700, 800],
    "default_flag": [0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
})
feature_columns = ["income", "debt_ratio", "payment_history", "balance"]
"""


COMMON_TOOLS_DATA = """records = [
    {"account": "A101", "event": "payment", "amount": 180.0},
    {"account": "A102", "event": "payment", "amount": 620.0},
    {"account": "A103", "event": "fee", "amount": -45.0},
    {"account": "A104", "event": "payment", "amount": 760.0},
]
"""


def _questions(spec):
    return [
        {
            "type": "multiple_choice",
            "question": "What does this lesson build from?",
            "options": [spec["prior"], "An unrelated topic", "A memorized answer with no code", "A design preference"],
            "answer": 0,
            "explanation": "Each lesson starts from the object or skill created immediately before it.",
        },
        {
            "type": "multiple_choice",
            "question": "What is the new capability in this lesson?",
            "options": [spec["adds"], "Skipping the calculation", "A portfolio-risk opinion", "A superficial badge"],
            "answer": 0,
            "explanation": "The lesson adds one concrete capability.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the core token used in the lesson.",
            "template": f"{spec['token_label']} = ___",
            "answer": spec["token"],
            "explanation": f"The core token for this lesson is `{spec['token']}`.",
        },
        {
            "type": "multiple_choice",
            "question": "Why is the lesson code-first?",
            "options": [
                "The code exposes the object that the concept is operating on",
                "It avoids understanding the concept",
                "It makes the answer automatically correct",
                "It removes the need for practice",
            ],
            "answer": 0,
            "explanation": "Hack asked for Python/math first, with explanation alongside the code.",
        },
        {
            "type": "true_false",
            "question": "A library shortcut is strongest after you understand what it is doing.",
            "answer": True,
            "explanation": "The curriculum teaches the underlying operation before leaning on shortcuts.",
        },
        {
            "type": "multiple_choice",
            "question": "What should your challenge output include?",
            "options": [spec["labels"][0], "Only unlabeled numbers", "A written answer with no code", "A generic greeting"],
            "answer": 0,
            "explanation": "Labeled output makes the notebook auditable.",
        },
        {
            "type": "multiple_choice",
            "question": "What makes this lesson connected rather than erratic?",
            "options": [
                "It reuses the prior lesson's object and adds one new operation",
                "It starts over from unrelated material",
                "It hides all intermediate steps",
                "It asks only vocabulary questions",
            ],
            "answer": 0,
            "explanation": "The sequence is designed as a ladder.",
        },
        {
            "type": "true_false",
            "question": "The challenge should require writing or editing code.",
            "answer": True,
            "explanation": "The rebuilt modules emphasize active coding practice.",
        },
        {
            "type": "multiple_choice",
            "question": "What is the best next move after computing the result?",
            "options": [
                "Interpret it, check assumptions, and connect it to the next lesson",
                "Treat it as a guaranteed population truth",
                "Ignore whether the code used the right data",
                "Delete the intermediate variables",
            ],
            "answer": 0,
            "explanation": "Strong analytics work connects calculation, meaning, and limitation.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the phrase.",
            "template": "code first, explanation ___",
            "answer": "alongside",
            "explanation": "That is the teaching pattern for the rebuild.",
        },
        {
            "type": "multiple_choice",
            "question": "Which answer is most graduate-oriented?",
            "options": [
                "Show the object, the operation, the output, and the limitation",
                "Show only the final print line",
                "Use finance language without computation",
                "Use computation without interpretation",
            ],
            "answer": 0,
            "explanation": "Graduate preparation requires code, reasoning, and bounded claims.",
        },
        {
            "type": "true_false",
            "question": "A running program can still be conceptually wrong if it uses the wrong object.",
            "answer": True,
            "explanation": "Execution success does not prove analytical correctness.",
        },
        {
            "type": "multiple_choice",
            "question": "Which practice item best rehearses this skill?",
            "options": [
                f"Rebuilding {spec['produces']} from {spec['prior']} with `{spec['token']}`",
                "Random trivia",
                "Only unrelated navigation details",
                "Only a self-rating",
            ],
            "answer": 0,
            "explanation": "Practice should rehearse exactly what the lesson taught.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the first output label.",
            "template": "print('___', value)",
            "answer": spec["labels"][0],
            "explanation": f"The first required label is `{spec['labels'][0]}`.",
        },
        {
            "type": "multiple_choice",
            "question": "What is the role of financial context here?",
            "options": [
                "It supplies realistic data while the lesson teaches the technical skill",
                "It replaces the technical skill",
                "It turns every lesson into investment theory",
                "It removes the need to compute",
            ],
            "answer": 0,
            "explanation": "Finance is the context; the skill is the learning target.",
        },
        {
            "type": "true_false",
            "question": "The lesson should introduce only as many new abstractions as the prior code can support.",
            "answer": True,
            "explanation": "This prevents the erratic topic jumps Hack called out.",
        },
        {
            "type": "multiple_choice",
            "question": "Which artifact should the lesson help build toward?",
            "options": [
                "A reproducible notebook, script, query, model, or tool",
                "A superficial badge",
                "A shallow definition list",
                "A disconnected quiz",
            ],
            "answer": 0,
            "explanation": "The course should build usable analytics artifacts.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the core skill.",
            "template": "Today I can produce: ___",
            "answer": spec["produces"],
            "explanation": "The lesson's output is the concrete skill target.",
        },
        {
            "type": "true_false",
            "question": "A model answer should include working code.",
            "answer": True,
            "explanation": "Model answers should show how to produce the result, not just state it.",
        },
        {
            "type": "multiple_choice",
            "question": "What should carry into the next lesson?",
            "options": [spec["produces"], "Nothing", "Only a page title", "Only a confidence score"],
            "answer": 0,
            "explanation": "The output of one lesson becomes the starting object for the next.",
        },
    ]


def _concept(module_title, spec):
    labels = "\n".join(f"- `{label}`" for label in spec["labels"])
    return f"""## Lesson Aim

This lesson belongs to **{module_title}**.

The course is rebuilt as a gradual mini-course, not a short survey. The lesson should
teach a real skill, give several examples, and then ask you to code the same kind of
work in practice and challenge.

You already have:

```text
{spec["prior"]}
```

This lesson adds:

```text
{spec["adds"]}
```

By the end, you should be able to produce:

```text
{spec["produces"]}
```

## Why This Comes Next

The sequence matters. The previous lesson creates the object you need here. This
lesson applies one new operation to that object. The next lesson should reuse the
output you create today.

The ladder is:

```text
{spec["prior"]} -> {spec["adds"]} -> {spec["produces"]}
```

If the middle step feels unclear, do not jump ahead. Rebuild the prior object in code,
then run the new operation slowly.

## Code First

Study this worked code before using shortcuts:

```python
{spec["code"]}
```

Do not just run it. Read each line as an analytical claim:

- What object exists before this line?
- What new object does this line create?
- What assumption is hidden in the operation?
- What would break if the data shape changed?

## Technical Notes

Core token:

```text
{spec["token"]}
```

Key idea:

```text
{spec["technical_note"]}
```

The token is not vocabulary for its own sake. It is the handle you use to connect code,
math, and interpretation.

## Finance Context

The financial context supplies realistic data: balances, payments, margins, segments,
transactions, defaults, and model outputs. The context should never replace the
technical lesson. You are learning the tool deeply enough to apply it to many
financial datasets later.

## Interpretation Standard

After the code runs, write an analyst sentence:

```text
I computed {spec["produces"]} from the available sample. The result helps because it
connects {spec["prior"]} to {spec["adds"]}. The limitation is that the result depends
on the sample, assumptions, and data quality.
```

## Required Challenge Labels

Your challenge should print:

{labels}

The labels make the work checkable. In a real notebook, labeled outputs are the
difference between a calculation you can defend and a pile of unlabeled numbers.

## Common Mistakes

- Starting with the shortcut before understanding the object.
- Treating a sample result as a guaranteed future result.
- Using finance words while skipping the calculation.
- Letting the lesson topic jump without carrying forward the prior object.
- Printing a number without a label, assumption, or limitation.

## Bridge Forward

The next lesson should begin with `{spec["produces"]}`. That is the course contract:
each lesson earns the next one.
"""


def _lesson(module_title, spec):
    tests = [{"type": "code_contains", "value": token} for token in spec["contains"]]
    tests += [{"type": "output_contains", "value": label} for label in spec["labels"]]
    tests.append({"type": "runs_without_error"})
    return {
        "id": spec["id"],
        "title": spec["title"],
        "order": spec["order"],
        "duration_min": spec.get("duration_min", 90),
        "difficulty": spec.get("difficulty", "intermediate"),
        "real_world_context": spec["context"],
        "concept": _concept(module_title, spec),
        "worked_example": {
            "description": spec["worked_goal"],
            "code": spec["code"],
            "explanation": f"This example produces {spec['produces']} from {spec['prior']}.",
        },
        "reference": {
            "key_syntax": spec["contains"],
            "notes": spec["technical_note"],
        },
        "questions": _questions(spec),
        "challenge": {
            "instructions": (
                f"Write code that produces {spec['produces']}. Print the required "
                "labels and keep the output interpretable."
            ),
            "starter_code": spec["starter"],
            "tests": tests,
            "solution": spec["code"],
        },
    }


def _module(module_id, title, description, course, order, lessons):
    built = [_lesson(title, spec) for spec in lessons]
    return {
        "id": module_id,
        "title": title,
        "description": description,
        "course": course,
        "order": order,
        "locked": False,
        "supplementary_courses": [],
        "concept_map": [
            {
                "id": lesson["id"],
                "label": lesson["title"][:42],
                "connects_to": [built[index + 1]["id"]] if index + 1 < len(built) else [],
            }
            for index, lesson in enumerate(built)
        ],
        "lessons": built,
    }


def _spec(prefix, order, title, prior, adds, produces, token, code, labels, contains, context, note=None):
    return {
        "id": f"{prefix}-l{order}",
        "title": title,
        "order": order,
        "prior": prior,
        "adds": adds,
        "produces": produces,
        "token": token,
        "token_label": "core_token",
        "technical_note": note or f"`{token}` is the main operation or object for this lesson.",
        "worked_goal": f"Produce {produces} using finance-oriented data.",
        "code": code,
        "starter": "# Write your code below. Use the lesson example as your model.\n",
        "labels": labels,
        "contains": contains,
        "context": context,
        "duration_min": 90,
        "difficulty": "intermediate" if order > 6 else "beginner",
    }


def _py_code(body):
    return COMMON_FINANCIAL_PYTHON + "\n" + body


def _pd_code(body):
    return COMMON_PANDAS_DATA + "\n" + body


def _sql_code(body):
    return COMMON_SQL_DATA + "\n" + body


def _ml_code(body):
    return COMMON_ML_DATA + "\n" + body


def _tools_code(body):
    return COMMON_TOOLS_DATA + "\n" + body


PYTHON_LESSONS = [
    ("Python Execution And Analyst Output", "nothing but the interpreter", "print output and labeled analyst results", "labeled Python output", "print", _py_code("""print("Account count:", len(transactions))
print("First account:", transactions[0]["account"])
print("Analyst output:", "Python is running on financial records")"""), ["Account count", "First account", "Analyst output"], ["print", "transactions"]),
    ("Variables And Numeric Types", "labeled output", "variables, integers, floats, and assignment", "named numeric finance values", "=", _py_code("""balance = transactions[0]["balance"]
payment = transactions[0]["payment"]
payment_rate = payment / balance
print("Balance:", balance)
print("Payment:", payment)
print("Payment rate:", round(payment_rate, 4))"""), ["Balance", "Payment", "Payment rate"], ["balance", "payment_rate"]),
    ("Finance Formulas As Expressions", "numeric variables", "arithmetic expressions for ratios and changes", "computed financial ratios", "/", _py_code("""total_balance = sum(row["balance"] for row in transactions)
total_payment = sum(row["payment"] for row in transactions)
portfolio_payment_rate = total_payment / total_balance
print("Total balance:", total_balance)
print("Total payment:", total_payment)
print("Portfolio payment rate:", round(portfolio_payment_rate, 4))"""), ["Total balance", "Total payment", "Portfolio payment rate"], ["sum", "portfolio_payment_rate"]),
    ("Strings And Formatted Analyst Text", "computed ratios", "strings, f-strings, rounding, and percent formatting", "readable analyst sentences", "f-string", _py_code("""total_balance = sum(row["balance"] for row in transactions)
total_payment = sum(row["payment"] for row in transactions)
rate = total_payment / total_balance
sentence = f"Portfolio payment rate is {rate:.2%}."
print("Formatted sentence:", sentence)
print("Rounded rate:", round(rate, 4))"""), ["Formatted sentence", "Rounded rate"], ["f\"", ".2%"]),
    ("Booleans And Comparisons", "numeric expressions", "comparison operators and boolean flags", "risk flags from account values", ">", _py_code("""flags = [row["balance"] > 2000 for row in transactions]
high_balance_count = sum(flags)
print("High balance flags:", flags)
print("High balance count:", high_balance_count)
print("Any high balance:", any(flags))"""), ["High balance flags", "High balance count", "Any high balance"], [">", "any"]),
    ("If Else Decisions", "boolean flags", "conditional branches for deterministic rules", "rule-based account decisions", "if", _py_code("""decisions = []
for row in transactions:
    if row["default"] == 1:
        decisions.append("review")
    else:
        decisions.append("standard")
print("Decisions:", decisions)
print("Review count:", decisions.count("review"))"""), ["Decisions", "Review count"], ["if", "else"]),
    ("Lists And Indexing", "conditional results", "lists, positions, slicing, and ordered collections", "indexed financial values", "list", _py_code("""balances = [row["balance"] for row in transactions]
first_balance = balances[0]
last_two = balances[-2:]
print("Balances:", balances)
print("First balance:", first_balance)
print("Last two balances:", last_two)"""), ["Balances", "First balance", "Last two balances"], ["balances", "[0]"]),
    ("Dictionaries And Records", "lists of values", "dictionary records and key lookup", "structured account records", "dict", _py_code("""record = transactions[2]
payment_ratio = record["payment"] / record["balance"]
summary = {"account": record["account"], "payment_ratio": payment_ratio, "default": record["default"]}
print("Record account:", summary["account"])
print("Record payment ratio:", round(summary["payment_ratio"], 4))
print("Record default:", summary["default"])"""), ["Record account", "Record payment ratio", "Record default"], ["summary", "record"]),
    ("Loops And Accumulators", "records in dictionaries", "for loops and running totals", "loop-based portfolio totals", "for", _py_code("""total = 0
for row in transactions:
    total += row["balance"]
average_balance = total / len(transactions)
print("Loop total balance:", total)
print("Loop average balance:", round(average_balance, 2))"""), ["Loop total balance", "Loop average balance"], ["for", "total +="]),
    ("Functions And Return Values", "loop calculations", "functions, parameters, and return values", "reusable finance calculations", "def", _py_code("""def payment_rate(payment, balance):
    return payment / balance

rates = [payment_rate(row["payment"], row["balance"]) for row in transactions]
print("Payment rates:", [round(rate, 4) for rate in rates])
print("Average payment rate:", round(sum(rates) / len(rates), 4))"""), ["Payment rates", "Average payment rate"], ["def", "return"]),
    ("Scope And Intermediate Variables", "functions", "local variables and calculation traceability", "auditable function internals", "return", _py_code("""def account_summary(row):
    balance = row["balance"]
    payment = row["payment"]
    rate = payment / balance
    return {"account": row["account"], "rate": rate}

summaries = [account_summary(row) for row in transactions]
print("First summary:", summaries[0])
print("Summary count:", len(summaries))"""), ["First summary", "Summary count"], ["account_summary", "return"]),
    ("Comprehensions", "loops and functions", "list comprehensions for compact transformations", "derived lists from financial records", "comprehension", _py_code("""rates = [row["payment"] / row["balance"] for row in transactions]
review_accounts = [row["account"] for row in transactions if row["default"] == 1]
print("Rates:", [round(rate, 4) for rate in rates])
print("Review accounts:", review_accounts)"""), ["Rates", "Review accounts"], ["for row in transactions", "if"]),
    ("Tuples And Unpacking", "derived lists", "tuples and unpacking returned results", "multi-value calculation outputs", "tuple", _py_code("""def totals(rows):
    total_balance = sum(row["balance"] for row in rows)
    total_payment = sum(row["payment"] for row in rows)
    return total_balance, total_payment

total_balance, total_payment = totals(transactions)
print("Unpacked balance:", total_balance)
print("Unpacked payment:", total_payment)"""), ["Unpacked balance", "Unpacked payment"], ["total_balance, total_payment", "return"]),
    ("Sets And Unique Categories", "records and lists", "sets for uniqueness and membership", "unique segment analysis", "set", _py_code("""segments = {row["segment"] for row in transactions}
is_prime_present = "prime" in segments
print("Unique segments:", sorted(segments))
print("Prime present:", is_prime_present)
print("Segment count:", len(segments))"""), ["Unique segments", "Prime present", "Segment count"], ["set", "segments"]),
    ("Error Handling", "functions and records", "try except for controlled failures", "safe ratio calculations", "try", _py_code("""def safe_rate(payment, balance):
    try:
        return payment / balance
    except ZeroDivisionError:
        return None

rates = [safe_rate(row["payment"], row["balance"]) for row in transactions]
print("Safe rates:", [round(rate, 4) for rate in rates])
print("Missing rate count:", rates.count(None))"""), ["Safe rates", "Missing rate count"], ["try", "except"]),
    ("Files And CSV Style Rows", "safe functions", "text lines, splitting, and CSV-like parsing", "parsed transaction rows", "split", _py_code("""csv_lines = ["account,balance,payment", "A101,1200,180", "A102,3400,620"]
header = csv_lines[0].split(",")
rows = [line.split(",") for line in csv_lines[1:]]
print("CSV header:", header)
print("Parsed rows:", rows)
print("Parsed row count:", len(rows))"""), ["CSV header", "Parsed rows", "Parsed row count"], ["split", "csv_lines"]),
    ("Modules And Imports", "parsed rows", "imports and reusable libraries", "standard-library calculations", "import", _py_code("""import statistics

balances = [row["balance"] for row in transactions]
mean_balance = statistics.mean(balances)
median_balance = statistics.median(balances)
print("Mean balance:", round(mean_balance, 2))
print("Median balance:", round(median_balance, 2))"""), ["Mean balance", "Median balance"], ["import statistics", "statistics.mean"]),
    ("Dates And Periods", "imports", "date parsing and period calculations", "time-aware account records", "datetime", _py_code("""from datetime import date

start = date(2026, 1, 1)
end = date(2026, 3, 31)
days = (end - start).days + 1
print("Start date:", start.isoformat())
print("End date:", end.isoformat())
print("Days in window:", days)"""), ["Start date", "End date", "Days in window"], ["date", "isoformat"]),
    ("Nested Data Structures", "records and imports", "nested lists and dictionaries", "multi-account grouped data", "nested", _py_code("""by_segment = {}
for row in transactions:
    by_segment.setdefault(row["segment"], []).append(row["balance"])
segment_averages = {segment: sum(values) / len(values) for segment, values in by_segment.items()}
print("Grouped balances:", by_segment)
print("Segment averages:", segment_averages)"""), ["Grouped balances", "Segment averages"], ["setdefault", "by_segment"]),
    ("Assertions And Tests", "functions", "assert statements and expected outputs", "basic correctness checks", "assert", _py_code("""def payment_rate(payment, balance):
    return payment / balance

assert round(payment_rate(180, 1200), 4) == 0.15
assert payment_rate(620, 3400) > 0
print("Assertions passed:", True)
print("Checked function:", "payment_rate")"""), ["Assertions passed", "Checked function"], ["assert", "payment_rate"]),
    ("NumPy Arrays From Python Lists", "lists and tests", "NumPy arrays and vectorized arithmetic", "array-based calculations", "np.array", """import numpy as np
""" + COMMON_FINANCIAL_PYTHON + """balances = np.array([row["balance"] for row in transactions])
payments = np.array([row["payment"] for row in transactions])
rates = payments / balances
print("Balance array:", balances)
print("Rate array:", np.round(rates, 4))
print("Mean rate:", round(rates.mean(), 4))""", ["Balance array", "Rate array", "Mean rate"], ["np.array", "rates"]),
    ("Vectorized Finance Formulas", "NumPy arrays", "array formulas without manual loops", "vectorized payment and default metrics", "vectorized", """import numpy as np
""" + COMMON_FINANCIAL_PYTHON + """balances = np.array([row["balance"] for row in transactions])
payments = np.array([row["payment"] for row in transactions])
defaults = np.array([row["default"] for row in transactions])
rates = payments / balances
weighted_default_exposure = (balances * defaults).sum()
print("Vectorized rates:", np.round(rates, 4))
print("Default exposure:", weighted_default_exposure)""", ["Vectorized rates", "Default exposure"], ["np.array", "defaults"]),
    ("Pandas Series Bridge", "NumPy vectors", "pandas Series labels and vector methods", "labeled one-dimensional analysis", "Series", _pd_code("""rate_series = financials["payment"] / financials["balance"]
print("Rate series:")
print(rate_series.round(4))
print("Series mean:", round(rate_series.mean(), 4))"""), ["Rate series", "Series mean"], ["rate_series", "mean"]),
    ("Pandas DataFrame Bridge", "Series analysis", "DataFrames as tables of aligned Series", "tabular financial analysis", "DataFrame", _pd_code("""analysis = financials[["account", "segment", "balance", "payment", "margin"]].copy()
analysis["payment_rate"] = analysis["payment"] / analysis["balance"]
print("Analysis columns:", list(analysis.columns))
print("Analysis row count:", len(analysis))
print("Mean payment rate:", round(analysis["payment_rate"].mean(), 4))"""), ["Analysis columns", "Analysis row count", "Mean payment rate"], ["analysis", "payment_rate"]),
    ("Clean Code And Type Hints", "functions and DataFrames", "small typed functions and readable names", "clean reusable analytics code", "type", _py_code("""def exposure_ratio(payment: float, balance: float) -> float:
    return payment / balance

ratios = [exposure_ratio(row["payment"], row["balance"]) for row in transactions]
print("Typed function name:", exposure_ratio.__name__)
print("Ratios:", [round(value, 4) for value in ratios])"""), ["Typed function name", "Ratios"], ["-> float", "exposure_ratio"]),
    ("Debugging With Print And Assertions", "clean functions", "debug traces and failing-case isolation", "debuggable finance functions", "debug", _py_code("""def payment_rate(row):
    rate = row["payment"] / row["balance"]
    print("Debug account:", row["account"], "rate:", round(rate, 4))
    return rate

rates = [payment_rate(row) for row in transactions[:2]]
assert all(rate > 0 for rate in rates)
print("Debugged rates:", [round(rate, 4) for rate in rates])"""), ["Debug account", "Debugged rates"], ["Debug", "assert"]),
    ("Packages And Virtual Environments", "imports", "package boundaries and reproducible dependencies", "dependency-aware scripts", "package", _py_code("""required_packages = ["numpy", "pandas", "scipy", "statsmodels"]
installed_plan = {name: "required for analytics" for name in required_packages}
print("Required packages:", required_packages)
print("Dependency plan:", installed_plan)"""), ["Required packages", "Dependency plan"], ["required_packages", "pandas"]),
    ("JSON And API Shaped Data", "nested dictionaries", "JSON-like payloads and response parsing", "API-ready finance records", "json", _py_code("""import json

payload = {"source": "mock_api", "records": transactions[:2]}
payload_text = json.dumps(payload)
parsed = json.loads(payload_text)
print("Payload source:", parsed["source"])
print("Payload record count:", len(parsed["records"]))"""), ["Payload source", "Payload record count"], ["json.dumps", "json.loads"]),
    ("Mini Analysis Script", "all Python fundamentals", "end-to-end script structure", "a complete reusable analysis script", "script", _py_code("""def analyze(rows):
    total_balance = sum(row["balance"] for row in rows)
    total_payment = sum(row["payment"] for row in rows)
    default_rate = sum(row["default"] for row in rows) / len(rows)
    return total_balance, total_payment, default_rate

total_balance, total_payment, default_rate = analyze(transactions)
print("Script total balance:", total_balance)
print("Script total payment:", total_payment)
print("Script default rate:", round(default_rate, 4))"""), ["Script total balance", "Script total payment", "Script default rate"], ["def analyze", "default_rate"]),
    ("Python Foundations Capstone", "mini analysis scripts", "functions, data structures, arrays, and analyst output", "a capstone financial calculator", "capstone", """import numpy as np
""" + COMMON_FINANCIAL_PYTHON + """def portfolio_summary(rows):
    balances = np.array([row["balance"] for row in rows])
    payments = np.array([row["payment"] for row in rows])
    defaults = np.array([row["default"] for row in rows])
    return {
        "total_balance": balances.sum(),
        "payment_rate": payments.sum() / balances.sum(),
        "default_rate": defaults.mean(),
    }

summary = portfolio_summary(transactions)
print("Capstone total balance:", round(summary["total_balance"], 2))
print("Capstone payment rate:", round(summary["payment_rate"], 4))
print("Capstone default rate:", round(summary["default_rate"], 4))""", ["Capstone total balance", "Capstone payment rate", "Capstone default rate"], ["portfolio_summary", "np.array"]),
]


def _build_specs(prefix, raw, context):
    specs = []
    prior = "the previous lesson's output"
    for index, item in enumerate(raw, start=1):
        title, previous, adds, produces, token, code, labels, contains = item
        specs.append(_spec(prefix, index, title, previous or prior, adds, produces, token, code, labels, contains, context))
        prior = produces
    return specs


DATA_RAW = [
    ("NumPy Arrays For Financial Columns", "Python lists of balances and payments", "NumPy arrays and vectorized operations", "array calculations for balances and rates", "np.array", _pd_code("""balances = financials["balance"].to_numpy()
payments = financials["payment"].to_numpy()
rates = payments / balances
print("Balance array:", balances)
print("Payment rate array:", np.round(rates, 4))
print("Mean payment rate:", round(rates.mean(), 4))"""), ["Balance array", "Payment rate array", "Mean payment rate"], ["to_numpy", "rates"]),
    ("DataFrames For Financial Tables", "array calculations", "DataFrame inspection and table shape", "auditable financial tables", "DataFrame", _pd_code("""print("Table shape:", financials.shape)
print("Table columns:", list(financials.columns))
print("First rows:")
print(financials.head(3))"""), ["Table shape", "Table columns", "First rows"], ["shape", "head"]),
    ("Reading And Validating Data", "DataFrame tables", "schema checks and required columns", "validated input tables", "schema", _pd_code("""required = {"account", "balance", "payment", "default_flag"}
missing = required - set(financials.columns)
print("Required columns:", sorted(required))
print("Missing columns:", sorted(missing))
print("Validation passed:", len(missing) == 0)"""), ["Required columns", "Missing columns", "Validation passed"], ["required", "missing"]),
    ("Selecting Columns And Rows", "validated tables", "column selection, loc, and boolean masks", "focused analytical subsets", "loc", _pd_code("""subset = financials.loc[financials["balance"] > 2000, ["account", "segment", "balance"]]
print("Subset row count:", len(subset))
print("Subset accounts:", subset["account"].to_list())
print("Subset mean balance:", round(subset["balance"].mean(), 2))"""), ["Subset row count", "Subset accounts", "Subset mean balance"], ["loc", "balance"]),
    ("Sorting And Ranking", "filtered subsets", "sort_values and rank", "ranked account lists", "sort_values", _pd_code("""ranked = financials.sort_values("balance", ascending=False).copy()
ranked["balance_rank"] = ranked["balance"].rank(ascending=False)
print("Top account:", ranked.iloc[0]["account"])
print("Top balance:", ranked.iloc[0]["balance"])
print("Ranks:", ranked["balance_rank"].to_list())"""), ["Top account", "Top balance", "Ranks"], ["sort_values", "rank"]),
    ("GroupBy Aggregation", "ranked rows", "groupby, aggregation, and segment summaries", "segment-level financial summaries", "groupby", _pd_code("""segment_summary = financials.groupby("segment").agg(
    average_balance=("balance", "mean"),
    default_rate=("default_flag", "mean"),
    total_revenue=("revenue", "sum"),
)
print("Segment summary:")
print(segment_summary.round(4))"""), ["Segment summary"], ["groupby", "agg"]),
    ("Missing Values", "group summaries", "isna, fillna, and missingness interpretation", "missingness audit", "isna", _pd_code("""audit = financials.isna().sum()
filled = financials.fillna({"payment": 0})
print("Missing audit:")
print(audit)
print("Filled row count:", len(filled))"""), ["Missing audit", "Filled row count"], ["isna", "fillna"]),
    ("Data Types And Casting", "missingness audit", "dtypes and numeric casting", "typed analysis columns", "dtypes", _pd_code("""types_before = financials.dtypes.astype(str)
financials["balance_float"] = financials["balance"].astype(float)
print("Types before:")
print(types_before)
print("Balance float dtype:", str(financials["balance_float"].dtype))"""), ["Types before", "Balance float dtype"], ["dtypes", "astype"]),
    ("Derived Columns", "typed columns", "new feature creation from existing columns", "payment and margin features", "assign", _pd_code("""features = financials.assign(
    payment_rate=financials["payment"] / financials["balance"],
    profit=financials["revenue"] - financials["cost"],
)
print("Feature columns:", ["payment_rate", "profit"])
print("Mean payment rate:", round(features["payment_rate"].mean(), 4))
print("Total profit:", round(features["profit"].sum(), 2))"""), ["Feature columns", "Mean payment rate", "Total profit"], ["assign", "payment_rate"]),
    ("Merging Tables", "derived columns", "merge and relational joins in pandas", "combined customer-account tables", "merge", _pd_code("""segments = pd.DataFrame({"segment": ["student", "prime", "near_prime"], "risk_weight": [1.4, 0.7, 1.1]})
joined = financials.merge(segments, on="segment", how="left")
print("Joined columns:", list(joined.columns))
print("Mean risk weight:", round(joined["risk_weight"].mean(), 4))"""), ["Joined columns", "Mean risk weight"], ["merge", "how"]),
    ("Concatenating Data", "merged tables", "concat and stacked periods", "multi-period tables", "concat", _pd_code("""next_month = financials.copy()
next_month["month"] = next_month["month"] + pd.offsets.MonthEnd(1)
stacked = pd.concat([financials, next_month], ignore_index=True)
print("Stacked row count:", len(stacked))
print("Month count:", stacked["month"].nunique())"""), ["Stacked row count", "Month count"], ["concat", "ignore_index"]),
    ("Pivot Tables", "multi-period tables", "pivot_table summaries", "matrix summaries by segment and month", "pivot_table", _pd_code("""pivot = financials.pivot_table(index="segment", columns="month", values="balance", aggfunc="mean")
print("Pivot shape:", pivot.shape)
print("Pivot table:")
print(pivot.round(2))"""), ["Pivot shape", "Pivot table"], ["pivot_table", "aggfunc"]),
    ("Date Indexing", "pivot summaries", "datetime columns and index operations", "time-indexed financial data", "datetime", _pd_code("""time_indexed = financials.set_index("month").sort_index()
print("Index type:", type(time_indexed.index).__name__)
print("First date:", time_indexed.index.min().date())
print("Last date:", time_indexed.index.max().date())"""), ["Index type", "First date", "Last date"], ["set_index", "sort_index"]),
    ("Rolling Metrics", "time-indexed data", "rolling windows and moving averages", "rolling payment trends", "rolling", _pd_code("""monthly = financials.groupby("month")["payment"].sum().sort_index()
rolling_payment = monthly.rolling(2).mean()
print("Monthly payments:")
print(monthly)
print("Rolling payment:")
print(rolling_payment)"""), ["Monthly payments", "Rolling payment"], ["rolling", "groupby"]),
    ("Reshaping Long And Wide", "rolling metrics", "melt and wide-to-long thinking", "tidy metric tables", "melt", _pd_code("""wide = financials[["account", "balance", "payment", "revenue"]]
long = wide.melt(id_vars="account", var_name="metric", value_name="value")
print("Long row count:", len(long))
print("Metric names:", sorted(long["metric"].unique()))"""), ["Long row count", "Metric names"], ["melt", "id_vars"]),
    ("String Cleanup", "tidy tables", "string methods for categories and IDs", "clean categorical variables", "str", _pd_code("""messy = financials.copy()
messy["segment"] = messy["segment"].str.upper()
clean = messy.assign(segment=messy["segment"].str.lower().str.strip())
print("Clean segments:", sorted(clean["segment"].unique()))
print("Account prefix:", clean["account"].str[0].unique().tolist())"""), ["Clean segments", "Account prefix"], ["str.lower", "str.strip"]),
    ("Outlier Detection", "clean columns", "quantiles, IQR, and flags", "outlier flags for financial metrics", "quantile", _pd_code("""q1 = financials["balance"].quantile(0.25)
q3 = financials["balance"].quantile(0.75)
iqr = q3 - q1
outlier_flag = (financials["balance"] < q1 - 1.5 * iqr) | (financials["balance"] > q3 + 1.5 * iqr)
print("IQR:", round(iqr, 2))
print("Outlier count:", int(outlier_flag.sum()))"""), ["IQR", "Outlier count"], ["quantile", "outlier_flag"]),
    ("Correlation Analysis", "outlier-aware metrics", "correlation matrices and relationship checks", "correlation matrix", "corr", _pd_code("""corr = financials[["balance", "payment", "revenue", "margin"]].corr()
print("Correlation matrix:")
print(corr.round(4))
print("Balance payment corr:", round(corr.loc["balance", "payment"], 4))"""), ["Correlation matrix", "Balance payment corr"], ["corr", "loc"]),
    ("Distributions And Histograms", "correlation matrix", "distribution bins and shape", "empirical distribution summaries", "histogram", _pd_code("""counts, bin_edges = np.histogram(financials["balance"], bins=4)
print("Histogram counts:", counts.tolist())
print("Histogram edges:", np.round(bin_edges, 2).tolist())
print("Balance skew proxy:", round(financials["balance"].mean() - financials["balance"].median(), 2))"""), ["Histogram counts", "Histogram edges", "Balance skew proxy"], ["np.histogram", "bin_edges"]),
    ("Hypothesis Test Workflow", "distributions", "sample difference, standard error, and test statistic", "test-ready comparison", "test_statistic", _pd_code("""prime = financials.loc[financials["segment"] == "prime", "payment"]
student = financials.loc[financials["segment"] == "student", "payment"]
difference = prime.mean() - student.mean()
se = np.sqrt(prime.var(ddof=1) / len(prime) + student.var(ddof=1) / len(student))
test_statistic = difference / se
print("Mean difference:", round(difference, 4))
print("Test statistic:", round(test_statistic, 4))"""), ["Mean difference", "Test statistic"], ["test_statistic", "var"]),
    ("Visualization Data Prep", "test-ready comparison", "chart-ready aggregation", "plot-ready summary table", "plot", _pd_code("""plot_data = financials.groupby("segment", as_index=False)["balance"].mean()
print("Plot rows:", len(plot_data))
print("Plot columns:", list(plot_data.columns))
print("Plot data:")
print(plot_data.round(2))"""), ["Plot rows", "Plot columns", "Plot data"], ["plot_data", "groupby"]),
    ("Matplotlib Basics", "plot-ready tables", "figure, axes, and labeled chart code", "a basic chart artifact", "matplotlib", _pd_code("""import matplotlib.pyplot as plt
plot_data = financials.groupby("segment", as_index=False)["balance"].mean()
fig, ax = plt.subplots()
ax.bar(plot_data["segment"], plot_data["balance"])
ax.set_title("Average Balance By Segment")
print("Chart title:", ax.get_title())
print("Bar count:", len(ax.patches))
plt.close(fig)"""), ["Chart title", "Bar count"], ["plt.subplots", "ax.bar"]),
    ("Professional Chart Labels", "basic chart", "titles, axes, units, and readable labels", "presentation-ready chart metadata", "label", _pd_code("""import matplotlib.pyplot as plt
plot_data = financials.groupby("segment", as_index=False)["payment"].mean()
fig, ax = plt.subplots()
ax.bar(plot_data["segment"], plot_data["payment"])
ax.set_title("Average Payment By Segment")
ax.set_ylabel("Dollars")
print("Chart title:", ax.get_title())
print("Y label:", ax.get_ylabel())
plt.close(fig)"""), ["Chart title", "Y label"], ["set_title", "set_ylabel"]),
    ("EDA Notebook Structure", "chart metadata", "question, data, analysis, interpretation sections", "reproducible EDA outline", "EDA", _pd_code("""eda_sections = ["question", "data check", "summary stats", "visuals", "interpretation", "limitations"]
summary = financials[["balance", "payment", "margin"]].describe()
print("EDA sections:", eda_sections)
print("Summary rows:", list(summary.index))"""), ["EDA sections", "Summary rows"], ["describe", "eda_sections"]),
    ("Pipelines With Functions", "EDA outline", "functions that transform and summarize data", "reusable analytics pipeline", "pipeline", _pd_code("""def add_features(df):
    return df.assign(payment_rate=df["payment"] / df["balance"], profit=df["revenue"] - df["cost"])

def summarize(df):
    return df.groupby("segment")["payment_rate"].mean()

features = add_features(financials)
summary = summarize(features)
print("Pipeline columns:", list(features.columns))
print("Pipeline summary:")
print(summary.round(4))"""), ["Pipeline columns", "Pipeline summary"], ["add_features", "summarize"]),
    ("Quality Checks", "pipeline functions", "row counts, schema checks, and assertions", "tested analytics pipeline", "assert", _pd_code("""features = financials.assign(payment_rate=financials["payment"] / financials["balance"])
assert len(features) == len(financials)
assert "payment_rate" in features.columns
assert features["payment_rate"].notna().all()
print("Quality checks passed:", True)
print("Checked rows:", len(features))"""), ["Quality checks passed", "Checked rows"], ["assert", "notna"]),
    ("Feature Store Thinking", "quality-checked features", "stable feature definitions and reuse", "feature table", "feature_store", _pd_code("""feature_table = financials[["account", "segment", "balance", "payment", "margin", "default_flag"]].copy()
feature_table["payment_rate"] = feature_table["payment"] / feature_table["balance"]
feature_dictionary = {col: str(feature_table[col].dtype) for col in feature_table.columns}
print("Feature table columns:", list(feature_table.columns))
print("Feature dictionary:", feature_dictionary)"""), ["Feature table columns", "Feature dictionary"], ["feature_table", "feature_dictionary"]),
    ("Analytics Report Tables", "feature table", "tables for memo-ready reporting", "polished report tables", "report", _pd_code("""report_table = financials.groupby("segment").agg(
    accounts=("account", "count"),
    avg_balance=("balance", "mean"),
    default_rate=("default_flag", "mean"),
)
print("Report table:")
print(report_table.round(4))
print("Report row count:", len(report_table))"""), ["Report table", "Report row count"], ["report_table", "agg"]),
    ("Model Answer Tables", "report tables", "tables that pair calculation with interpretation", "self-check analytical answer table", "model_answer", _pd_code("""answer_table = financials.groupby("segment").agg(
    average_balance=("balance", "mean"),
    average_margin=("margin", "mean"),
    default_rate=("default_flag", "mean"),
)
answer_table["interpretation"] = np.where(answer_table["default_rate"] > 0, "review risk", "standard monitoring")
print("Model answer table:")
print(answer_table.round(4))
print("Interpretation labels:", answer_table["interpretation"].to_list())"""), ["Model answer table", "Interpretation labels"], ["answer_table", "interpretation"]),
    ("Data Analytics Capstone", "report tables", "full pandas workflow from raw table to insight", "complete analytics notebook output", "capstone", _pd_code("""features = financials.assign(payment_rate=financials["payment"] / financials["balance"], profit=financials["revenue"] - financials["cost"])
summary = features.groupby("segment").agg(avg_balance=("balance", "mean"), avg_payment_rate=("payment_rate", "mean"), total_profit=("profit", "sum"), default_rate=("default_flag", "mean"))
top_segment = summary["total_profit"].idxmax()
print("Capstone summary:")
print(summary.round(4))
print("Top profit segment:", top_segment)
print("Capstone limitation:", "Small sample; validate on more months.")"""), ["Capstone summary", "Top profit segment", "Capstone limitation"], ["features", "summary"]),
]

SQL_RAW = [
    ("Database Tables And Schemas", "structured data needs", "tables, columns, and schema inspection", "a readable database schema", "schema", _sql_code("""tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print("Table names:", [row[0] for row in tables])
print("Schema ready:", len(tables) == 3)"""), ["Table names", "Schema ready"], ["sqlite_master", "execute"]),
    ("SELECT And FROM", "database schema", "basic row retrieval", "first query result set", "SELECT", _sql_code("""rows = cur.execute("SELECT customer_id, segment FROM customers ORDER BY customer_id").fetchall()
print("Selected rows:", rows)
print("Row count:", len(rows))"""), ["Selected rows", "Row count"], ["SELECT", "FROM"]),
    ("WHERE Filters", "basic SELECT", "row filters and comparison predicates", "filtered financial rows", "WHERE", _sql_code("""rows = cur.execute("SELECT account_id, balance FROM accounts WHERE balance > 2000 ORDER BY balance").fetchall()
print("Filtered accounts:", rows)
print("Filtered count:", len(rows))"""), ["Filtered accounts", "Filtered count"], ["WHERE", "balance"]),
    ("ORDER BY And LIMIT", "filtered rows", "sorting and limiting result sets", "ranked query outputs", "ORDER BY", _sql_code("""rows = cur.execute("SELECT account_id, balance FROM accounts ORDER BY balance DESC LIMIT 2").fetchall()
print("Top accounts:", rows)
print("Top account id:", rows[0][0])"""), ["Top accounts", "Top account id"], ["ORDER BY", "LIMIT"]),
    ("Aggregates", "ranked rows", "COUNT, SUM, AVG, MIN, and MAX", "portfolio-level SQL summaries", "AVG", _sql_code("""row = cur.execute("SELECT COUNT(*), SUM(balance), AVG(balance), MAX(balance) FROM accounts").fetchone()
print("Account count:", row[0])
print("Total balance:", row[1])
print("Average balance:", round(row[2], 2))
print("Max balance:", row[3])"""), ["Account count", "Total balance", "Average balance", "Max balance"], ["COUNT", "AVG"]),
    ("GROUP BY", "aggregates", "grouped aggregation by segment", "segment SQL summaries", "GROUP BY", _sql_code("""rows = cur.execute('''
SELECT c.segment, COUNT(*), AVG(a.balance)
FROM accounts a JOIN customers c ON a.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY c.segment
''').fetchall()
print("Segment groups:", rows)"""), ["Segment groups"], ["GROUP BY", "JOIN"]),
    ("HAVING", "grouped summaries", "filters after aggregation", "filtered segment groups", "HAVING", _sql_code("""rows = cur.execute('''
SELECT c.segment, AVG(a.balance) AS avg_balance
FROM accounts a JOIN customers c ON a.customer_id = c.customer_id
GROUP BY c.segment
HAVING avg_balance > 1500
''').fetchall()
print("Having groups:", rows)
print("Having count:", len(rows))"""), ["Having groups", "Having count"], ["HAVING", "avg_balance"]),
    ("CASE Expressions", "filtered groups", "conditional labels in SQL", "rule-based SQL categories", "CASE", _sql_code("""rows = cur.execute('''
SELECT account_id, balance,
CASE WHEN status = 'delinquent' THEN 'review' WHEN balance > 3000 THEN 'monitor' ELSE 'standard' END AS action
FROM accounts
ORDER BY account_id
''').fetchall()
print("Case actions:", rows)"""), ["Case actions"], ["CASE", "WHEN"]),
    ("NULL Handling", "CASE labels", "COALESCE and NULLIF defensive logic", "null-safe calculations", "COALESCE", _sql_code("""row = cur.execute("SELECT COALESCE(NULL, 'missing'), NULLIF(100, 100)").fetchone()
print("Coalesce result:", row[0])
print("Nullif result:", row[1])"""), ["Coalesce result", "Nullif result"], ["COALESCE", "NULLIF"]),
    ("INNER JOIN", "single-table queries", "joining related customer and account tables", "combined relational records", "JOIN", _sql_code("""rows = cur.execute('''
SELECT a.account_id, c.segment, a.balance
FROM accounts a INNER JOIN customers c ON a.customer_id = c.customer_id
ORDER BY a.account_id
''').fetchall()
print("Joined rows:", rows)
print("Joined count:", len(rows))"""), ["Joined rows", "Joined count"], ["INNER JOIN", "ON"]),
    ("LEFT JOIN", "inner joins", "preserving left-side rows", "left-joined account coverage", "LEFT JOIN", _sql_code("""rows = cur.execute('''
SELECT c.customer_id, c.segment, a.account_id
FROM customers c LEFT JOIN accounts a ON c.customer_id = a.customer_id
ORDER BY c.customer_id
''').fetchall()
print("Left joined rows:", rows)
print("Left join count:", len(rows))"""), ["Left joined rows", "Left join count"], ["LEFT JOIN", "customers"]),
    ("Multi Table Joins", "two-table joins", "joining customers, accounts, and transactions", "transaction-level analytical rows", "multi_join", _sql_code("""rows = cur.execute('''
SELECT t.transaction_id, c.segment, a.status, t.amount
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
ORDER BY t.transaction_id
''').fetchall()
print("Multi join rows:", rows)
print("Multi join count:", len(rows))"""), ["Multi join rows", "Multi join count"], ["transactions t", "JOIN accounts"]),
    ("Subqueries", "multi-table joins", "queries inside filters", "nested query outputs", "subquery", _sql_code("""rows = cur.execute('''
SELECT account_id, balance
FROM accounts
WHERE balance > (SELECT AVG(balance) FROM accounts)
ORDER BY balance
''').fetchall()
print("Above average accounts:", rows)"""), ["Above average accounts"], ["SELECT AVG", "WHERE balance"]),
    ("CTEs", "subqueries", "WITH clauses and named intermediate results", "readable staged SQL", "WITH", _sql_code("""rows = cur.execute('''
WITH account_payments AS (
    SELECT account_id, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY account_id
)
SELECT account_id, total_amount FROM account_payments ORDER BY account_id
''').fetchall()
print("CTE results:", rows)"""), ["CTE results"], ["WITH", "account_payments"]),
    ("Window Functions", "CTEs", "analytics without losing row detail", "ranked rows with window values", "OVER", _sql_code("""rows = cur.execute('''
SELECT account_id, balance,
RANK() OVER (ORDER BY balance DESC) AS balance_rank
FROM accounts
ORDER BY balance_rank
''').fetchall()
print("Window ranks:", rows)"""), ["Window ranks"], ["OVER", "RANK"]),
    ("Date And Text Functions", "window rows", "date and string operations", "period-aware SQL outputs", "substr", _sql_code("""rows = cur.execute("SELECT transaction_id, substr(month, 1, 7) AS month_key FROM transactions ORDER BY transaction_id").fetchall()
print("Month keys:", rows)"""), ["Month keys"], ["substr", "month_key"]),
    ("Primary And Foreign Keys", "joined tables", "key constraints and relational integrity", "key-aware schema reasoning", "FOREIGN KEY", _sql_code("""foreign_keys = cur.execute("PRAGMA foreign_key_list(accounts)").fetchall()
print("Account foreign keys:", foreign_keys)
print("Foreign key count:", len(foreign_keys))"""), ["Account foreign keys", "Foreign key count"], ["PRAGMA", "foreign_key_list"]),
    ("Normalization", "key-aware schema", "separating entities to reduce duplication", "normalized customer-account design", "normalization", _sql_code("""customer_columns = cur.execute("PRAGMA table_info(customers)").fetchall()
account_columns = cur.execute("PRAGMA table_info(accounts)").fetchall()
print("Customer columns:", [row[1] for row in customer_columns])
print("Account columns:", [row[1] for row in account_columns])"""), ["Customer columns", "Account columns"], ["PRAGMA table_info", "customers"]),
    ("CREATE TABLE", "normalized design", "DDL table creation", "new analytical table schema", "CREATE TABLE", _sql_code("""cur.execute("CREATE TABLE risk_scores (account_id INTEGER PRIMARY KEY, score REAL NOT NULL)")
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='risk_scores'").fetchall()
print("Created table:", tables[0][0])
print("Create succeeded:", len(tables) == 1)"""), ["Created table", "Create succeeded"], ["CREATE TABLE", "risk_scores"]),
    ("INSERT INTO", "created tables", "loading rows into tables", "inserted analytical records", "INSERT", _sql_code("""cur.execute("CREATE TABLE risk_scores (account_id INTEGER PRIMARY KEY, score REAL NOT NULL)")
cur.executemany("INSERT INTO risk_scores VALUES (?, ?)", [(101, 0.12), (103, 0.71)])
rows = cur.execute("SELECT * FROM risk_scores ORDER BY account_id").fetchall()
print("Inserted scores:", rows)"""), ["Inserted scores"], ["INSERT INTO", "executemany"]),
    ("UPDATE And DELETE", "inserted rows", "controlled modifications", "modified analytical records", "UPDATE", _sql_code("""cur.execute("CREATE TABLE risk_scores (account_id INTEGER PRIMARY KEY, score REAL NOT NULL)")
cur.executemany("INSERT INTO risk_scores VALUES (?, ?)", [(101, 0.12), (103, 0.71)])
cur.execute("UPDATE risk_scores SET score = 0.75 WHERE account_id = 103")
cur.execute("DELETE FROM risk_scores WHERE account_id = 101")
rows = cur.execute("SELECT * FROM risk_scores").fetchall()
print("Remaining scores:", rows)"""), ["Remaining scores"], ["UPDATE", "DELETE"]),
    ("Views", "query outputs", "saved SELECT logic", "reusable analytical view", "VIEW", _sql_code("""cur.execute("CREATE VIEW active_accounts AS SELECT account_id, balance FROM accounts WHERE status = 'active'")
rows = cur.execute("SELECT * FROM active_accounts ORDER BY account_id").fetchall()
print("View rows:", rows)
print("View count:", len(rows))"""), ["View rows", "View count"], ["CREATE VIEW", "active_accounts"]),
    ("Indexes", "views", "index creation and lookup planning", "indexed query support", "INDEX", _sql_code("""cur.execute("CREATE INDEX idx_transactions_account ON transactions(account_id)")
indexes = cur.execute("PRAGMA index_list(transactions)").fetchall()
print("Transaction indexes:", indexes)
print("Index count:", len(indexes))"""), ["Transaction indexes", "Index count"], ["CREATE INDEX", "PRAGMA index_list"]),
    ("Transactions", "modification queries", "commit, rollback, and atomic changes", "transaction-safe updates", "rollback", _sql_code("""conn.execute("BEGIN")
cur.execute("UPDATE accounts SET balance = balance + 100 WHERE account_id = 101")
conn.rollback()
balance = cur.execute("SELECT balance FROM accounts WHERE account_id = 101").fetchone()[0]
print("Balance after rollback:", balance)"""), ["Balance after rollback"], ["BEGIN", "rollback"]),
    ("Python SQLite Connection", "SQL statements", "Python DB-API workflow", "query results inside Python", "sqlite3", _sql_code("""rows = cur.execute("SELECT COUNT(*) FROM transactions").fetchone()
print("SQLite row count:", rows[0])
print("Connection type:", type(conn).__name__)"""), ["SQLite row count", "Connection type"], ["sqlite3", "fetchone"]),
    ("Parameterized Queries", "Python SQLite", "safe placeholders and query parameters", "safe user-filtered queries", "parameter", _sql_code("""status = "active"
rows = cur.execute("SELECT account_id FROM accounts WHERE status = ?", (status,)).fetchall()
print("Parameterized accounts:", rows)
print("Parameterized count:", len(rows))"""), ["Parameterized accounts", "Parameterized count"], ["?", "(status,)"]),
    ("Pandas Read SQL", "parameterized queries", "loading SQL results into DataFrames", "SQL-to-pandas analytical table", "read_sql_query", _sql_code("""import pandas as pd
df = pd.read_sql_query("SELECT account_id, balance, status FROM accounts", conn)
print("DataFrame shape:", df.shape)
print("Mean SQL balance:", round(df["balance"].mean(), 2))"""), ["DataFrame shape", "Mean SQL balance"], ["read_sql_query", "DataFrame"]),
    ("Analytical Marts", "SQL-to-pandas tables", "building reusable analysis tables", "account performance mart", "mart", _sql_code("""rows = cur.execute('''
CREATE TABLE account_mart AS
SELECT a.account_id, c.segment, a.balance, a.status, COALESCE(SUM(t.amount), 0) AS net_amount
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN transactions t ON a.account_id = t.account_id
GROUP BY a.account_id, c.segment, a.balance, a.status
''')
mart = cur.execute("SELECT * FROM account_mart ORDER BY account_id").fetchall()
print("Mart rows:", mart)
print("Mart count:", len(mart))"""), ["Mart rows", "Mart count"], ["CREATE TABLE account_mart", "GROUP BY"]),
    ("Cohort Queries", "analytical marts", "cohort grouping by start period", "cohort retention-style summary", "cohort", _sql_code("""rows = cur.execute('''
SELECT opened_month, COUNT(*) AS customers
FROM customers
GROUP BY opened_month
ORDER BY opened_month
''').fetchall()
print("Cohort rows:", rows)
print("Cohort count:", len(rows))"""), ["Cohort rows", "Cohort count"], ["opened_month", "GROUP BY"]),
    ("SQL Capstone", "all SQL skills", "schema, joins, aggregates, CTEs, windows, and Python execution", "complete SQL analytics packet", "capstone", _sql_code("""query = '''
WITH account_totals AS (
    SELECT a.account_id, c.segment, a.balance, a.status, COALESCE(SUM(t.amount), 0) AS net_amount
    FROM accounts a
    JOIN customers c ON a.customer_id = c.customer_id
    LEFT JOIN transactions t ON a.account_id = t.account_id
    GROUP BY a.account_id, c.segment, a.balance, a.status
)
SELECT segment, COUNT(*) AS accounts, AVG(balance) AS avg_balance, SUM(net_amount) AS net_amount
FROM account_totals
GROUP BY segment
ORDER BY segment
'''
rows = cur.execute(query).fetchall()
print("Capstone SQL rows:", rows)
print("Capstone query length:", len(query))"""), ["Capstone SQL rows", "Capstone query length"], ["WITH", "LEFT JOIN"]),
]

ML_RAW = [
    ("Machine Learning Workflow", "clean analysis tables", "features, target, model, evaluation, and limitation", "ML workflow map", "workflow", _ml_code("""X = loans[feature_columns]
y = loans["default_flag"]
print("Feature columns:", list(X.columns))
print("Target mean:", round(y.mean(), 4))
print("Workflow steps:", ["split", "train", "predict", "evaluate"])"""), ["Feature columns", "Target mean", "Workflow steps"], ["feature_columns", "default_flag"]),
    ("Feature Target Split", "workflow map", "X/y separation for supervised learning", "feature matrix and target vector", "X", _ml_code("""X = loans[feature_columns].to_numpy()
y = loans["default_flag"].to_numpy()
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Positive class rate:", round(y.mean(), 4))"""), ["X shape", "y shape", "Positive class rate"], ["to_numpy", "X"]),
    ("Train Test Split", "X/y arrays", "honest holdout evaluation", "train and test datasets", "split", _ml_code("""X = loans[feature_columns].to_numpy()
y = loans["default_flag"].to_numpy()
train_idx = np.arange(0, 7)
test_idx = np.arange(7, len(loans))
print("Train shape:", X[train_idx].shape)
print("Test shape:", X[test_idx].shape)
print("Test target rate:", round(y[test_idx].mean(), 4))"""), ["Train shape", "Test shape", "Test target rate"], ["train_idx", "test_idx"]),
    ("Baselines", "train/test split", "naive predictions and baseline metrics", "baseline model score", "baseline", _ml_code("""y = loans["default_flag"].to_numpy()
baseline_prediction = np.repeat(0, len(y))
accuracy = (baseline_prediction == y).mean()
print("Baseline prediction:", 0)
print("Baseline accuracy:", round(accuracy, 4))"""), ["Baseline prediction", "Baseline accuracy"], ["baseline_prediction", "accuracy"]),
    ("Linear Regression For Numeric Prediction", "baseline scoring", "OLS for continuous outcomes", "manual regression coefficients", "OLS", _ml_code("""X = loans[["income", "debt_ratio"]].to_numpy()
y = loans["balance"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
predictions = X_design @ beta
print("OLS beta:", np.round(beta, 4))
print("Prediction mean:", round(predictions.mean(), 4))"""), ["OLS beta", "Prediction mean"], ["np.linalg.pinv", "beta"]),
    ("Regression Metrics", "numeric predictions", "MAE, RMSE, and R-squared", "regression evaluation table", "RMSE", _ml_code("""X = loans[["income", "debt_ratio"]].to_numpy()
y = loans["balance"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
pred = X_design @ beta
mae = np.abs(y - pred).mean()
rmse = np.sqrt(((y - pred) ** 2).mean())
r2 = 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
print("MAE:", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R squared:", round(r2, 4))"""), ["MAE", "RMSE", "R squared"], ["rmse", "r2"]),
    ("Logistic Regression", "classification target", "probability model for default", "logistic predictions", "logistic", _ml_code("""X = loans[["debt_ratio", "payment_history"]].to_numpy()
y = loans["default_flag"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta = np.zeros(X_design.shape[1])
for _ in range(600):
    p = 1 / (1 + np.exp(-(X_design @ beta)))
    beta -= 0.4 * (X_design.T @ (p - y) / len(y))
print("Logistic beta:", np.round(beta, 4))
print("Mean predicted probability:", round(p.mean(), 4))"""), ["Logistic beta", "Mean predicted probability"], ["np.exp", "beta"]),
    ("Classification Metrics", "logistic probabilities", "accuracy, precision, recall", "classification metric set", "precision", _ml_code("""scores = loans["debt_ratio"] - loans["payment_history"]
y = loans["default_flag"].to_numpy()
pred = (scores > -0.35).astype(int)
tp = int(((pred == 1) & (y == 1)).sum())
fp = int(((pred == 1) & (y == 0)).sum())
fn = int(((pred == 0) & (y == 1)).sum())
accuracy = (pred == y).mean()
precision = tp / (tp + fp)
recall = tp / (tp + fn)
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))"""), ["Accuracy", "Precision", "Recall"], ["precision", "recall"]),
    ("Confusion Matrix", "classification metrics", "TP, FP, TN, FN matrix", "confusion matrix counts", "confusion", _ml_code("""scores = loans["debt_ratio"] - loans["payment_history"]
y = loans["default_flag"].to_numpy()
pred = (scores > -0.35).astype(int)
matrix = {
    "tp": int(((pred == 1) & (y == 1)).sum()),
    "fp": int(((pred == 1) & (y == 0)).sum()),
    "tn": int(((pred == 0) & (y == 0)).sum()),
    "fn": int(((pred == 0) & (y == 1)).sum()),
}
print("Confusion matrix:", matrix)"""), ["Confusion matrix"], ["tp", "fp"]),
    ("Threshold Tuning", "confusion matrix", "classification thresholds and tradeoffs", "threshold comparison table", "threshold", _ml_code("""prob = 1 / (1 + np.exp(-(6 * loans["debt_ratio"] - 5 * loans["payment_history"])))
y = loans["default_flag"].to_numpy()
for threshold in [0.3, 0.5, 0.7]:
    pred = (prob >= threshold).astype(int)
    print("Threshold result:", threshold, round((pred == y).mean(), 4), int(pred.sum()))"""), ["Threshold result"], ["threshold", "prob"]),
    ("ROC And AUC", "threshold tuning", "ranking quality across thresholds", "AUC estimate", "AUC", _ml_code("""scores = (loans["debt_ratio"] - loans["payment_history"]).to_numpy()
y = loans["default_flag"].to_numpy()
pos = scores[y == 1]
neg = scores[y == 0]
pairs = [(p > n) + 0.5 * (p == n) for p in pos for n in neg]
auc = np.mean(pairs)
print("AUC estimate:", round(float(auc), 4))
print("Positive score mean:", round(pos.mean(), 4))"""), ["AUC estimate", "Positive score mean"], ["auc", "pairs"]),
    ("Feature Scaling", "model scores", "standardization for model inputs", "scaled feature matrix", "scaling", _ml_code("""X = loans[feature_columns]
scaled = (X - X.mean()) / X.std(ddof=1)
print("Scaled means:")
print(scaled.mean().round(4))
print("Scaled stds:")
print(scaled.std(ddof=1).round(4))"""), ["Scaled means", "Scaled stds"], ["scaled", "std"]),
    ("K Nearest Neighbors", "scaled features", "distance-based prediction", "nearest-neighbor classification", "distance", _ml_code("""X = ((loans[["debt_ratio", "payment_history"]] - loans[["debt_ratio", "payment_history"]].mean()) / loans[["debt_ratio", "payment_history"]].std(ddof=1)).to_numpy()
y = loans["default_flag"].to_numpy()
target = X[0]
distances = np.linalg.norm(X - target, axis=1)
nearest = np.argsort(distances)[1:4]
print("Nearest indexes:", nearest.tolist())
print("Neighbor default rate:", round(y[nearest].mean(), 4))"""), ["Nearest indexes", "Neighbor default rate"], ["np.linalg.norm", "nearest"]),
    ("K Means Clustering", "scaled features", "unsupervised segmentation", "cluster assignments", "kmeans", _ml_code("""X = ((loans[["debt_ratio", "payment_history"]] - loans[["debt_ratio", "payment_history"]].mean()) / loans[["debt_ratio", "payment_history"]].std(ddof=1)).to_numpy()
centers = X[[0, 3]].copy()
for _ in range(5):
    labels = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2).argmin(axis=1)
    centers = np.array([X[labels == k].mean(axis=0) for k in range(2)])
print("Cluster labels:", labels.tolist())
print("Cluster centers:", np.round(centers, 4))"""), ["Cluster labels", "Cluster centers"], ["centers", "labels"]),
    ("Decision Rules And Trees", "feature thresholds", "interpretable rule splits", "simple tree-like rule", "tree", _ml_code("""rule_pred = ((loans["debt_ratio"] > 0.5) | (loans["payment_history"] < 0.7)).astype(int)
accuracy = (rule_pred == loans["default_flag"]).mean()
print("Rule predictions:", rule_pred.to_list())
print("Rule accuracy:", round(accuracy, 4))"""), ["Rule predictions", "Rule accuracy"], ["rule_pred", "accuracy"]),
    ("Ensembles", "single rules", "multiple rules and averaged votes", "ensemble prediction", "ensemble", _ml_code("""rule1 = (loans["debt_ratio"] > 0.5).astype(int)
rule2 = (loans["payment_history"] < 0.75).astype(int)
rule3 = (loans["income"] < 50000).astype(int)
votes = rule1 + rule2 + rule3
ensemble_pred = (votes >= 2).astype(int)
print("Ensemble votes:", votes.to_list())
print("Ensemble accuracy:", round((ensemble_pred == loans["default_flag"]).mean(), 4))"""), ["Ensemble votes", "Ensemble accuracy"], ["votes", "ensemble_pred"]),
    ("Cross Validation", "model evaluation", "fold-based validation", "cross-validation scores", "fold", _ml_code("""y = loans["default_flag"].to_numpy()
scores = []
for fold_start in [0, 2, 4, 6, 8]:
    test_idx = np.arange(fold_start, min(fold_start + 2, len(loans)))
    pred = (loans.iloc[test_idx]["debt_ratio"] > 0.45).astype(int).to_numpy()
    scores.append((pred == y[test_idx]).mean())
print("CV scores:", scores)
print("Mean CV score:", round(np.mean(scores), 4))"""), ["CV scores", "Mean CV score"], ["scores", "fold_start"]),
    ("Overfitting And Underfitting", "cross-validation scores", "training fit vs generalization", "fit comparison metrics", "overfit", _ml_code("""train_accuracy = 1.0
cv_accuracy = 0.7
gap = train_accuracy - cv_accuracy
print("Train accuracy:", train_accuracy)
print("CV accuracy:", cv_accuracy)
print("Generalization gap:", round(gap, 4))"""), ["Train accuracy", "CV accuracy", "Generalization gap"], ["gap", "cv_accuracy"]),
    ("Regularization", "generalization gap", "coefficient penalties", "regularized coefficient estimate", "lambda", _ml_code("""X = loans[["debt_ratio", "payment_history"]].to_numpy()
y = loans["default_flag"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
lam = 1.0
penalty = np.eye(X_design.shape[1])
penalty[0, 0] = 0
beta_ridge = np.linalg.pinv(X_design.T @ X_design + lam * penalty) @ X_design.T @ y
print("Ridge beta:", np.round(beta_ridge, 4))
print("Penalty lambda:", lam)"""), ["Ridge beta", "Penalty lambda"], ["lam", "beta_ridge"]),
    ("Hyperparameter Tuning", "regularized models", "grid search over choices", "selected hyperparameter", "grid", _ml_code("""candidates = [0.1, 1.0, 10.0]
scores = {lam: 1 / (1 + abs(lam - 1.0)) for lam in candidates}
best_lam = max(scores, key=scores.get)
print("Grid scores:", scores)
print("Best lambda:", best_lam)"""), ["Grid scores", "Best lambda"], ["candidates", "best_lam"]),
    ("Pipelines", "tuned components", "ordered preprocessing and modeling steps", "reproducible model pipeline", "pipeline", _ml_code("""pipeline_steps = ["select features", "scale", "fit model", "predict", "evaluate"]
X = loans[feature_columns]
scaled = (X - X.mean()) / X.std(ddof=1)
print("Pipeline steps:", pipeline_steps)
print("Pipeline feature shape:", scaled.shape)"""), ["Pipeline steps", "Pipeline feature shape"], ["pipeline_steps", "scaled"]),
    ("Data Leakage", "pipelines", "training-only transformations and leakage checks", "leakage-safe workflow", "leakage", _ml_code("""features = set(feature_columns)
forbidden = {"default_flag"}
leakage_found = len(features & forbidden) > 0
print("Leakage found:", leakage_found)
print("Feature count:", len(features))"""), ["Leakage found", "Feature count"], ["forbidden", "leakage_found"]),
    ("Imbalanced Classes", "classification metrics", "class rates and weighted thinking", "imbalance-aware evaluation", "imbalance", _ml_code("""y = loans["default_flag"]
class_counts = y.value_counts().sort_index()
class_rates = y.value_counts(normalize=True).sort_index()
print("Class counts:", class_counts.to_dict())
print("Class rates:", class_rates.round(4).to_dict())"""), ["Class counts", "Class rates"], ["value_counts", "class_rates"]),
    ("Calibration", "predicted probabilities", "probability bins and observed rates", "calibration table", "calibration", _ml_code("""prob = 1 / (1 + np.exp(-(6 * loans["debt_ratio"] - 5 * loans["payment_history"])))
calibration = pd.DataFrame({"prob": prob, "actual": loans["default_flag"]})
calibration["bin"] = pd.cut(calibration["prob"], bins=3)
table = calibration.groupby("bin", observed=False)["actual"].mean()
print("Calibration table:")
print(table.round(4))"""), ["Calibration table"], ["pd.cut", "groupby"]),
    ("Interpretability", "calibrated models", "feature contribution and transparent explanations", "model explanation table", "interpret", _ml_code("""weights = pd.Series({"income": -0.1, "debt_ratio": 0.8, "payment_history": -0.9, "balance": 0.2})
top_driver = weights.abs().idxmax()
print("Feature weights:")
print(weights)
print("Top driver:", top_driver)"""), ["Feature weights", "Top driver"], ["weights", "idxmax"]),
    ("Saving Model Artifacts", "interpretable model", "serializable coefficients and metadata", "saved model dictionary", "artifact", _ml_code("""artifact = {"model": "risk_score_v1", "features": feature_columns, "weights": [0.1, 0.8, -0.9, 0.2]}
print("Artifact model:", artifact["model"])
print("Artifact feature count:", len(artifact["features"]))"""), ["Artifact model", "Artifact feature count"], ["artifact", "features"]),
    ("Monitoring Model Drift", "saved artifacts", "input drift and performance monitoring", "drift monitoring metrics", "drift", _ml_code("""baseline_mean = loans["debt_ratio"].mean()
new_mean = baseline_mean + 0.04
drift = new_mean - baseline_mean
print("Baseline debt ratio:", round(baseline_mean, 4))
print("New debt ratio:", round(new_mean, 4))
print("Drift amount:", round(drift, 4))"""), ["Baseline debt ratio", "New debt ratio", "Drift amount"], ["drift", "baseline_mean"]),
    ("Model Cards And Documentation", "drift metrics", "documenting purpose, data, metrics, limits, and review cadence", "model documentation card", "model_card", _ml_code("""model_card = {
    "model_name": "default_risk_v1",
    "target": "default_flag",
    "features": feature_columns,
    "metric": "accuracy and recall",
    "limitation": "small training sample",
}
print("Model card name:", model_card["model_name"])
print("Model card target:", model_card["target"])
print("Model card limitation:", model_card["limitation"])"""), ["Model card name", "Model card target", "Model card limitation"], ["model_card", "limitation"]),
    ("Ethics And Fairness Checks", "model documentation", "segment-level error checks and ethical limitations", "fairness audit summary", "fairness", _ml_code("""rule_pred = ((loans["debt_ratio"] > 0.5) | (loans["payment_history"] < 0.7)).astype(int)
audit = loans.assign(prediction=rule_pred, correct=(rule_pred == loans["default_flag"]))
segment_accuracy = audit.assign(segment=np.where(audit["income"] < 50000, "lower_income", "higher_income")).groupby("segment")["correct"].mean()
print("Fairness audit:")
print(segment_accuracy.round(4))
print("Fairness limitation:", "Segments are crude proxies; review with better data.")"""), ["Fairness audit", "Fairness limitation"], ["segment_accuracy", "Fairness"]),
    ("ML Capstone", "full ML workflow", "feature prep, model, evaluation, interpretation, and limitation", "complete default-risk model packet", "capstone", _ml_code("""X = loans[["debt_ratio", "payment_history"]].to_numpy()
y = loans["default_flag"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta = np.zeros(X_design.shape[1])
for _ in range(700):
    prob = 1 / (1 + np.exp(-(X_design @ beta)))
    beta -= 0.4 * (X_design.T @ (prob - y) / len(y))
pred = (prob >= 0.5).astype(int)
accuracy = (pred == y).mean()
print("Capstone beta:", np.round(beta, 4))
print("Capstone accuracy:", round(accuracy, 4))
print("Capstone limitation:", "Tiny sample; validate out of sample.")"""), ["Capstone beta", "Capstone accuracy", "Capstone limitation"], ["beta", "accuracy"]),
]

TOOLS_RAW = [
    ("Command Line Thinking", "Python scripts", "arguments, inputs, outputs, and exit points", "CLI-style tool output", "cli", _tools_code("""args = {"min_amount": 100}
filtered = [row for row in records if row["amount"] >= args["min_amount"]]
print("CLI args:", args)
print("Filtered records:", filtered)"""), ["CLI args", "Filtered records"], ["args", "filtered"]),
    ("Logging", "CLI tool output", "structured run logs", "logged tool events", "log", _tools_code("""logs = []
logs.append({"level": "INFO", "message": "loaded records", "count": len(records)})
logs.append({"level": "INFO", "message": "computed total", "amount": sum(r["amount"] for r in records)})
print("Log entries:", logs)
print("Log count:", len(logs))"""), ["Log entries", "Log count"], ["logs", "append"]),
    ("Configuration", "logged scripts", "config dictionaries and defaults", "configurable analysis tool", "config", _tools_code("""config = {"min_amount": 100, "include_fees": False}
selected = [r for r in records if r["amount"] >= config["min_amount"]]
print("Config:", config)
print("Selected count:", len(selected))"""), ["Config", "Selected count"], ["config", "min_amount"]),
    ("JSON Storage", "configurable tools", "serializing and loading records", "JSON-backed local store", "json", _tools_code("""import json
payload = json.dumps(records)
loaded = json.loads(payload)
print("JSON length:", len(payload))
print("Loaded count:", len(loaded))"""), ["JSON length", "Loaded count"], ["json.dumps", "json.loads"]),
    ("Key Value Store", "JSON records", "dictionary-backed persistence", "account lookup store", "key_value", _tools_code("""store = {row["account"]: row for row in records}
print("Store keys:", sorted(store.keys()))
print("Lookup A103:", store["A103"])"""), ["Store keys", "Lookup A103"], ["store", "keys"]),
    ("CSV Query Engine", "key-value records", "filtering rows with a tiny query function", "queryable flat-file data", "query", _tools_code("""def query(rows, predicate):
    return [row for row in rows if predicate(row)]

payments = query(records, lambda row: row["event"] == "payment")
print("Query count:", len(payments))
print("Query total:", sum(row["amount"] for row in payments))"""), ["Query count", "Query total"], ["query", "lambda"]),
    ("Search Index", "query functions", "inverted indexes for lookup", "searchable event records", "index", _tools_code("""index = {}
for row in records:
    index.setdefault(row["event"], []).append(row["account"])
print("Index keys:", sorted(index.keys()))
print("Payment accounts:", index["payment"])"""), ["Index keys", "Payment accounts"], ["setdefault", "index"]),
    ("Regex Style Matching", "search indexes", "pattern matching with simple rules", "matched account IDs", "match", _tools_code("""matches = [row["account"] for row in records if row["account"].startswith("A10")]
fees = [row for row in records if row["event"] == "fee"]
print("Matched accounts:", matches)
print("Fee records:", fees)"""), ["Matched accounts", "Fee records"], ["startswith", "matches"]),
    ("Template Engine", "matched records", "rendering text from data", "rendered analyst text", "template", _tools_code("""template = "Account {account} had {event} amount {amount}."
rendered = [template.format(**row) for row in records]
print("Rendered first:", rendered[0])
print("Rendered count:", len(rendered))"""), ["Rendered first", "Rendered count"], ["template", "format"]),
    ("Markdown Report Generator", "rendered text", "tables and sections as strings", "generated markdown report", "markdown", _tools_code("""lines = ["# Payment Report", "", "| account | amount |", "|---|---:|"]
for row in records:
    lines.append(f"| {row['account']} | {row['amount']} |")
report = "\\n".join(lines)
print("Markdown title:", lines[0])
print("Markdown line count:", len(lines))"""), ["Markdown title", "Markdown line count"], ["report", "join"]),
    ("Notebook Cell Model", "markdown reports", "cell lists and execution order", "notebook-like artifact", "cell", _tools_code("""cells = [{"type": "markdown", "source": "# Analysis"}, {"type": "code", "source": "sum_amount = 1515"}]
print("Cell count:", len(cells))
print("First cell type:", cells[0]["type"])"""), ["Cell count", "First cell type"], ["cells", "source"]),
    ("Task Scheduler", "notebook artifacts", "queueing and ordering work", "scheduled analysis tasks", "schedule", _tools_code("""tasks = [{"name": "load"}, {"name": "clean"}, {"name": "summarize"}]
for i, task in enumerate(tasks, start=1):
    task["order"] = i
print("Scheduled tasks:", tasks)
print("Next task:", tasks[0]["name"])"""), ["Scheduled tasks", "Next task"], ["tasks", "enumerate"]),
    ("In Memory Cache", "scheduled tasks", "caching expensive calculations", "cached summary values", "cache", _tools_code("""cache = {}
def total_amount():
    if "total" not in cache:
        cache["total"] = sum(row["amount"] for row in records)
    return cache["total"]

print("Cached total:", total_amount())
print("Cache keys:", list(cache.keys()))"""), ["Cached total", "Cache keys"], ["cache", "total_amount"]),
    ("HTTP Request Parser", "cached values", "request text parsing", "parsed request components", "HTTP", _tools_code("""request = "GET /accounts?segment=prime HTTP/1.1"
method, path, protocol = request.split(" ")
print("HTTP method:", method)
print("HTTP path:", path)
print("HTTP protocol:", protocol)"""), ["HTTP method", "HTTP path", "HTTP protocol"], ["split", "protocol"]),
    ("HTTP Response Builder", "parsed requests", "status lines, headers, and body", "HTTP response text", "response", _tools_code("""body = "OK"
response = "HTTP/1.1 200 OK\\r\\nContent-Type: text/plain\\r\\n\\r\\n" + body
print("Response starts:", response.split("\\r\\n")[0])
print("Response length:", len(response))"""), ["Response starts", "Response length"], ["response", "Content-Type"]),
    ("API Client With Mock Data", "HTTP responses", "client functions and parsed payloads", "mock API client result", "client", _tools_code("""def fetch_accounts():
    return {"status": 200, "data": records}

result = fetch_accounts()
print("API status:", result["status"])
print("API record count:", len(result["data"]))"""), ["API status", "API record count"], ["fetch_accounts", "result"]),
    ("SQLite Tool", "API-shaped data", "local database storage", "database-backed tool output", "sqlite", """import sqlite3
""" + COMMON_TOOLS_DATA + """conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE records (account TEXT, event TEXT, amount REAL)")
cur.executemany("INSERT INTO records VALUES (:account, :event, :amount)", records)
total = cur.execute("SELECT SUM(amount) FROM records").fetchone()[0]
print("SQLite total:", total)
print("SQLite rows:", cur.execute("SELECT COUNT(*) FROM records").fetchone()[0])""", ["SQLite total", "SQLite rows"], ["sqlite3", "executemany"]),
    ("Message Queue", "database-backed tools", "FIFO task processing", "processed queue output", "queue", _tools_code("""queue = records.copy()
processed = []
while queue:
    processed.append(queue.pop(0)["account"])
print("Processed accounts:", processed)
print("Queue empty:", len(queue) == 0)"""), ["Processed accounts", "Queue empty"], ["queue", "pop"]),
    ("Retry Logic", "queued tasks", "controlled retries after failure", "retry-aware process", "retry", _tools_code("""attempts = []
for attempt in range(1, 4):
    attempts.append(attempt)
    success = attempt == 3
    if success:
        break
print("Attempts:", attempts)
print("Succeeded:", success)"""), ["Attempts", "Succeeded"], ["attempts", "break"]),
    ("Rate Limiter", "retry logic", "simple throttling logic", "rate-limited events", "rate_limit", _tools_code("""limit = 2
allowed = records[:limit]
blocked = records[limit:]
print("Allowed count:", len(allowed))
print("Blocked count:", len(blocked))"""), ["Allowed count", "Blocked count"], ["limit", "blocked"]),
    ("Validation Layer", "rate-limited inputs", "schema validation before processing", "validated records", "validate", _tools_code("""required = {"account", "event", "amount"}
valid = [required.issubset(row.keys()) for row in records]
print("Validation flags:", valid)
print("All valid:", all(valid))"""), ["Validation flags", "All valid"], ["required", "issubset"]),
    ("Error Budget", "validation layer", "counting failures and acceptable limits", "error-budget report", "error_budget", _tools_code("""failures = [row for row in records if row["amount"] < 0]
budget = 1
within_budget = len(failures) <= budget
print("Failure count:", len(failures))
print("Within budget:", within_budget)"""), ["Failure count", "Within budget"], ["failures", "budget"]),
    ("Unit Tests", "validated tools", "assertions over tool behavior", "tested tool functions", "test", _tools_code("""def total(rows):
    return sum(row["amount"] for row in rows)

assert total(records) == 1515.0
assert len(records) == 4
print("Unit tests passed:", True)
print("Tested function:", "total")"""), ["Unit tests passed", "Tested function"], ["assert", "total"]),
    ("Plugin Boundaries", "tested functions", "inputs, outputs, and contracts", "plugin-style function contract", "contract", _tools_code("""def tool_contract(rows):
    return {"input_rows": len(rows), "output_total": sum(row["amount"] for row in rows)}

result = tool_contract(records)
print("Contract result:", result)
print("Contract keys:", sorted(result.keys()))"""), ["Contract result", "Contract keys"], ["tool_contract", "result"]),
    ("Simple Auth Token", "tool contracts", "token checks and guarded access", "guarded tool call", "token", _tools_code("""expected_token = "local-dev-token"
provided_token = "local-dev-token"
allowed = provided_token == expected_token
print("Token allowed:", allowed)
print("Guarded records:", len(records) if allowed else 0)"""), ["Token allowed", "Guarded records"], ["expected_token", "allowed"]),
    ("Audit Trail", "guarded access", "recording who did what and when", "audit event log", "audit", _tools_code("""audit_log = []
audit_log.append({"actor": "Hack", "action": "run_summary", "rows": len(records)})
print("Audit log:", audit_log)
print("Audit count:", len(audit_log))"""), ["Audit log", "Audit count"], ["audit_log", "append"]),
    ("Deployment Checklist", "audit trail", "readiness checks before sharing", "deployment readiness report", "deploy", _tools_code("""checks = {"tests": True, "docs": True, "secrets_removed": True, "sample_data": True}
ready = all(checks.values())
print("Deployment checks:", checks)
print("Ready to share:", ready)"""), ["Deployment checks", "Ready to share"], ["checks", "ready"]),
    ("Monitoring Dashboard Data", "deployment checklist", "status metrics and counters", "dashboard-ready metrics", "monitor", _tools_code("""metrics = {"records_processed": len(records), "negative_amounts": sum(1 for r in records if r["amount"] < 0), "total_amount": sum(r["amount"] for r in records)}
print("Monitoring metrics:", metrics)
print("Metric count:", len(metrics))"""), ["Monitoring metrics", "Metric count"], ["metrics", "records_processed"]),
    ("Secrets And Environment Variables", "monitoring metrics", "keeping credentials out of source code", "safe configuration report", "secrets", _tools_code("""import os

os.environ["ORION_DEMO_TOKEN"] = "local-demo"
token_present = "ORION_DEMO_TOKEN" in os.environ
safe_config = {"uses_env_var": token_present, "hardcoded_secret": False}
print("Safe config:", safe_config)
print("Token present:", token_present)"""), ["Safe config", "Token present"], ["os.environ", "safe_config"]),
    ("Build Tools Capstone", "monitoring metrics", "storage, query, report, validation, and audit", "complete local analytics tool", "capstone", _tools_code("""def build_report(rows):
    total = sum(row["amount"] for row in rows)
    negatives = [row for row in rows if row["amount"] < 0]
    return {"rows": len(rows), "total": total, "negative_count": len(negatives)}

report = build_report(records)
print("Capstone report:", report)
print("Capstone limitation:", "Toy local tool; add persistence and UI before production.")"""), ["Capstone report", "Capstone limitation"], ["build_report", "report"]),
]


MODULE_1_REBUILT = _module(
    "module1",
    "Python Foundations For Financial Analytics",
    "A 30-lesson Python mini-course that teaches beginner programming through finance-oriented calculations, scripts, and reusable functions.",
    "Core Analytics - Python Foundations",
    2,
    _build_specs("m1", PYTHON_LESSONS, "Python is taught through financial records, analyst calculations, and reproducible scripts."),
)

MODULE_2_REBUILT = _module(
    "module2",
    "Data Analytics With Python",
    "A 30-lesson pandas and NumPy mini-course for cleaning, transforming, visualizing, and reporting financial-analysis datasets.",
    "Core Analytics - Data Analytics",
    3,
    _build_specs("m2", DATA_RAW, "Data analytics is taught through account, payment, margin, default, and segment datasets."),
)

MODULE_3_REBUILT = _module(
    "module3",
    "Structured Data And SQL For Financial Analytics",
    "A 30-lesson SQL mini-course that teaches relational thinking, analytical queries, database design, Python SQLite, and SQL reporting.",
    "Core Analytics - SQL",
    4,
    _build_specs("m3", SQL_RAW, "SQL is taught through customers, accounts, transactions, joins, cohorts, and analytical marts."),
)

MODULE_4_REBUILT = _module(
    "module4",
    "Machine Learning For Financial Analytics",
    "A 30-lesson machine-learning mini-course that builds from X/y arrays to evaluation, classification, clustering, pipelines, and monitoring.",
    "Core Analytics - Machine Learning",
    5,
    _build_specs("m4", ML_RAW, "Machine learning is taught through default-risk, payment-history, and balance prediction examples."),
)

MODULE_5_REBUILT = _module(
    "module5",
    "Build It Yourself - Analytics Systems And Tools",
    "A 30-lesson systems mini-course for building small local tools that support analytics workflows: storage, search, reports, APIs, queues, tests, and monitoring.",
    "Core Analytics - Build Tools",
    6,
    _build_specs("m5", TOOLS_RAW, "Systems are taught as small local tools that make analytics work reproducible and inspectable."),
)
