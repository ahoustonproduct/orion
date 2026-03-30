MODULE_4 = {
    "id": "module4",
    "title": "Machine Learning in Python",
    "description": "Build models that learn from data and make predictions. Machine learning is the engine behind AI — and scikit-learn makes it accessible to every analyst.",
    "course": "MSBC 5180 · Machine Learning",
    "order": 4,
    "locked": True,
    "concept_map": [
        {"id": "m4-l1",  "label": "What is ML?",               "connects_to": ["m4-l2"]},
        {"id": "m4-l2",  "label": "ML Workflow",               "connects_to": ["m4-l3"]},
        {"id": "m4-l3",  "label": "Preparing Data",            "connects_to": ["m4-l4"]},
        {"id": "m4-l4",  "label": "Train/Test Split",          "connects_to": ["m4-l5", "m4-l7"]},
        {"id": "m4-l5",  "label": "Linear Regression",         "connects_to": ["m4-l6"]},
        {"id": "m4-l6",  "label": "Evaluating Regression",     "connects_to": ["m4-l17"]},
        {"id": "m4-l7",  "label": "Logistic Regression",       "connects_to": ["m4-l8"]},
        {"id": "m4-l8",  "label": "Evaluating Classification", "connects_to": ["m4-l9"]},
        {"id": "m4-l9",  "label": "Confusion Matrix",          "connects_to": ["m4-l10"]},
        {"id": "m4-l10", "label": "Decision Trees",            "connects_to": ["m4-l11"]},
        {"id": "m4-l11", "label": "Random Forests",            "connects_to": ["m4-l15"]},
        {"id": "m4-l12", "label": "KNN",                       "connects_to": ["m4-l14"]},
        {"id": "m4-l13", "label": "K-Means Clustering",        "connects_to": ["m4-l15"]},
        {"id": "m4-l14", "label": "Feature Scaling",           "connects_to": ["m4-l12", "m4-l20"]},
        {"id": "m4-l15", "label": "Feature Selection",         "connects_to": ["m4-l16"]},
        {"id": "m4-l16", "label": "Cross-Validation",          "connects_to": ["m4-l17"]},
        {"id": "m4-l17", "label": "Overfitting/Underfitting",  "connects_to": ["m4-l18"]},
        {"id": "m4-l18", "label": "Regularization",            "connects_to": ["m4-l19"]},
        {"id": "m4-l19", "label": "Hyperparameter Tuning",     "connects_to": ["m4-l20"]},
        {"id": "m4-l20", "label": "ML Pipelines",              "connects_to": ["m4-l21"]},
        {"id": "m4-l21", "label": "ROC Curve & AUC",           "connects_to": ["m4-l22"]},
        {"id": "m4-l22", "label": "Saving Models",             "connects_to": ["m4-l25"]},
        {"id": "m4-l23", "label": "Imbalanced Data",           "connects_to": ["m4-l24"]},
        {"id": "m4-l24", "label": "Churn Prediction",          "connects_to": ["m4-l25"]},
        {"id": "m4-l25", "label": "Deploying ML Models",       "connects_to": ["m4-capstone"]},
        {"id": "m4-capstone", "label": "Capstone Project",     "connects_to": []},
    ],
    "lessons": [
        # ─────────────────────────────────────────────
        # LESSON 1
        # ─────────────────────────────────────────────
        {
            "id": "m4-l1",
            "title": "What is Machine Learning?",
            "order": 1,
            "duration_min": 15,
            "real_world_context": "Netflix recommends movies, banks flag fraud, doctors predict diagnoses — all with ML. You'll build your first predictive model in this module.",
            "concept": """**Machine learning** is the practice of teaching a computer to learn patterns from data — instead of writing explicit rules yourself.

**The Big Idea: Traditional Programming vs. Machine Learning**

In traditional programming, a human writes every rule:
```python
# Traditional rule-based approach
def approve_loan(credit_score, income, debt):
    if credit_score > 700 and income > 50000 and debt < 0.3:
        return "Approved"
    else:
        return "Denied"
# Problem: you have to think of every rule yourself
```

In machine learning, the computer *discovers* the rules from historical data:
```python
from sklearn.ensemble import RandomForestClassifier

# Give the model historical loan decisions
# It figures out the rules automatically!
model = RandomForestClassifier()
model.fit(X_historical_loans, y_approved_or_denied)

# Now predict on new applicants
prediction = model.predict([[720, 62000, 0.25]])
# Output: ['Approved']
```

**Three Types of Machine Learning:**

**1. Supervised Learning** — Learning with labeled examples
- You have historical data WITH correct answers
- Goal: predict the answer for new data
- Examples: predicting house prices, classifying emails as spam, forecasting sales
```python
# Label = "correct answer" the model learns from
# Input: house features → Output: price (which you know from past sales)
X = [[1500, 3, 2], [2200, 4, 3]]  # sqft, bedrooms, bathrooms
y = [250000, 380000]               # actual sale prices (the "labels")
```

**2. Unsupervised Learning** — Finding hidden patterns without labels
- You have data but NO correct answers
- Goal: discover structure, groups, or patterns
- Examples: customer segmentation, anomaly detection
```python
# No labels — the model finds natural groups on its own
# Input: customer purchase data → Output: "Segment A, B, C"
```

**3. Reinforcement Learning** — Learning through trial and error
- An agent takes actions and receives rewards/penalties
- Examples: game-playing AI, robotics, recommendation systems
- (We focus on supervised and unsupervised in this module)

**Real Business Examples:**
| Business Problem | ML Type | Algorithm |
|---|---|---|
| Predict customer churn | Supervised | Logistic Regression |
| Forecast next month's sales | Supervised | Linear Regression |
| Segment customers | Unsupervised | K-Means |
| Detect credit card fraud | Supervised | Random Forest |
| Email spam filter | Supervised | Decision Tree |

The library you'll use throughout this module is **scikit-learn** (sklearn) — the gold standard for ML in Python.
```python
import sklearn
print(sklearn.__version__)
# Output: 1.4.0  (or similar)
```""",
            "worked_example": {
                "description": "Let's see the difference between traditional rules and ML side-by-side using a simple salary prediction scenario.",
                "code": """import numpy as np

# Traditional approach: human writes rules
def estimate_salary_traditional(years_exp):
    if years_exp < 2:
        return 45000
    elif years_exp < 5:
        return 65000
    elif years_exp < 10:
        return 85000
    else:
        return 110000

# ML approach: model learns from data
from sklearn.linear_model import LinearRegression

# Historical data: years experience → salary
years_exp = np.array([[1],[2],[3],[5],[7],[10],[12]])
salaries   = np.array([42000, 50000, 60000, 75000, 88000, 105000, 118000])

model = LinearRegression()
model.fit(years_exp, salaries)

# Predict salary for someone with 8 years experience
prediction = model.predict([[8]])
print(f"Traditional rule: ${estimate_salary_traditional(8):,}")
print(f"ML prediction:    ${prediction[0]:,.0f}")
# Traditional rule: $85,000
# ML prediction:    $96,857""",
                "explanation": "The traditional function uses hand-coded thresholds. The ML model mathematically fits a line through the data — and can give a precise prediction for ANY value, not just the buckets a human defined."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "import sklearn",
                    "from sklearn.linear_model import LinearRegression",
                    "model.fit(X, y)  # train",
                    "model.predict(X_new)  # predict"
                ],
                "notes": "Supervised = you have labels (correct answers). Unsupervised = no labels. Reinforcement = reward signals."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A bank wants to predict whether a loan applicant will default, using 10,000 past loans that are each labeled 'defaulted' or 'paid off'. Which type of ML is this?",
                    "options": ["Unsupervised learning", "Reinforcement learning", "Supervised learning", "Rule-based programming"],
                    "answer": 2,
                    "explanation": "Supervised learning uses labeled historical data — here each past loan has a known outcome (defaulted or paid off), which the model learns from."
                },
                {
                    "type": "true_false",
                    "question": "In machine learning, you must write every decision rule explicitly in code.",
                    "answer": False,
                    "explanation": "That's traditional programming. In ML, the algorithm discovers the rules (patterns) automatically from training data."
                },
                {
                    "type": "fill_blank",
                    "question": "The Python ML library used throughout this module is called ___-learn.",
                    "template": "from ___ .linear_model import LinearRegression",
                    "answer": "sklearn",
                    "explanation": "scikit-learn (imported as sklearn) is the standard Python library for machine learning, providing hundreds of ready-to-use algorithms."
                }
            ],
            "challenge": {
                "instructions": "Import LinearRegression from sklearn. Create training data: a list of years_experience values [1, 3, 5, 7, 9] and corresponding annual_revenue values [20000, 45000, 80000, 110000, 150000]. Reshape years_experience into a 2D array using .reshape(-1, 1). Fit the model and predict revenue for 6 years of experience. Print the prediction.",
                "starter_code": "from sklearn.linear_model import LinearRegression\nimport numpy as np\n\nyears_experience = np.array([1, 3, 5, 7, 9])\nannual_revenue   = np.array([20000, 45000, 80000, 110000, 150000])\n\n# Reshape years_experience to 2D (sklearn requires this)\nX = years_experience.reshape(-1, 1)\ny = annual_revenue\n\n# Create and fit the model\n\n\n# Predict revenue for 6 years of experience\n",
                "tests": [
                    {"type": "output_contains", "value": "9"},
                    {"type": "code_contains", "value": "LinearRegression"},
                    {"type": "code_contains", "value": ".fit("}
                ],
                "solution": "from sklearn.linear_model import LinearRegression\nimport numpy as np\nyears_experience = np.array([1, 3, 5, 7, 9])\nannual_revenue   = np.array([20000, 45000, 80000, 110000, 150000])\nX = years_experience.reshape(-1, 1)\ny = annual_revenue\nmodel = LinearRegression()\nmodel.fit(X, y)\nprediction = model.predict([[6]])\nprint(f'Predicted revenue for 6 years: ${prediction[0]:,.0f}')"
            },
            "challenge_variations": [
                "Variation 1: Use advertising_spend [1000,3000,5000,7000,9000] and sales [5000,12000,22000,30000,40000] to predict sales for $6,000 spend.",
                "Variation 2: Use store_size_sqft [500,1000,1500,2000,2500] and daily_customers [50,110,155,210,260] to predict customers for a 1800 sqft store.",
                "Variation 3: Create employee data with hours_worked [20,30,40,50,60] and productivity_score [55,70,85,88,80]. Fit and predict for 45 hours.",
                "Variation 4: Use temperature [60,65,70,75,80] and ice_cream_sales [100,150,220,310,420] to predict sales on a 72-degree day.",
                "Variation 5: Create a dataset with study_hours [1,2,4,6,8] and exam_scores [50,58,72,85,95]. Predict score for 5 hours studied.",
                "Variation 6: Build a model using num_employees [5,10,20,50,100] and monthly_costs [2000,3800,7200,17000,33000]. Predict costs for 30 employees.",
                "Variation 7: Use commute_distance_miles [2,5,10,20,30] and late_arrivals_per_month [0,1,3,7,12]. Predict for 15 miles.",
                "Variation 8: With marketing_emails_sent [100,500,1000,5000,10000] and new_signups [3,12,22,95,180], predict signups for 2000 emails.",
                "Variation 9: Create years_since_renovation [0,2,5,10,20] and maintenance_cost [500,900,1800,4000,9500]. Predict for 7 years.",
                "Variation 10: Use social_media_followers [1000,5000,10000,50000,100000] and monthly_sales [200,800,1500,6000,11000]. Predict for 20000 followers."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 2
        # ─────────────────────────────────────────────
        {
            "id": "m4-l2",
            "title": "The ML Workflow — From Data to Prediction",
            "order": 2,
            "duration_min": 15,
            "real_world_context": "Every ML project — whether at Google, a hospital, or a small startup — follows the same 6-step workflow. Mastering this workflow is what separates analysts who dabble in ML from those who deploy it.",
            "concept": """Every successful ML project follows six steps. Skip one and the whole model falls apart.

**The 6-Step ML Workflow:**

```
Step 1: Define the Problem
Step 2: Collect & Explore Data
Step 3: Prepare Data (clean, encode, scale)
Step 4: Train the Model
Step 5: Evaluate the Model
Step 6: Deploy & Monitor
```

**Step 1 — Define the Problem**
Be specific. "Use ML" is not a goal. A real goal is:
> "Predict whether a customer will cancel their subscription in the next 30 days, so our retention team can intervene."

Ask yourself:
- What am I predicting? (a number → regression; a category → classification)
- What data do I have?
- What counts as success? (95% accuracy? Save $500K/year?)

**Step 2 — Collect & Explore Data**
```python
import pandas as pd

df = pd.read_csv("customer_data.csv")
print(df.shape)        # How many rows and columns?
print(df.head())       # What does it look like?
print(df.describe())   # Summary statistics
print(df.isnull().sum()) # How many missing values?
```

**Step 3 — Prepare Data**
```python
# Handle missing values, encode categories, scale numbers
# (You'll learn each of these in detail in upcoming lessons)
df["age"].fillna(df["age"].median(), inplace=True)
df = pd.get_dummies(df, columns=["city"])
```

**Step 4 — Train the Model**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X = df.drop("churned", axis=1)
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)   # <-- this is where learning happens
```

**Step 5 — Evaluate the Model**
```python
from sklearn.metrics import accuracy_score

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.1%}")
# Output: Accuracy: 87.3%
```

**Step 6 — Deploy & Monitor**
- Save the model to a file
- Wrap it in an API endpoint (you'll do this in Lesson 25)
- Monitor for performance drift over time

**Why the order matters:**
You MUST explore and prepare data BEFORE training. Training on messy data produces a garbage model — the famous "garbage in, garbage out" principle.
""",
            "worked_example": {
                "description": "Here is the complete 6-step workflow applied to a tiny sales dataset so you can see every step connected.",
                "code": """import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# ── STEP 1: Define the problem ──────────────────────────
# Goal: predict monthly sales from advertising budget

# ── STEP 2: Collect & explore data ──────────────────────
data = {
    "ad_budget":     [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
    "monthly_sales": [5200, 9800, 14100, 19500, 24200, 28800, 33500, 39000]
}
df = pd.DataFrame(data)
print("Shape:", df.shape)               # Shape: (8, 2)
print("Missing:", df.isnull().sum())    # Missing: 0

# ── STEP 3: Prepare data ────────────────────────────────
X = df[["ad_budget"]]    # Feature matrix (must be 2D)
y = df["monthly_sales"]  # Target vector

# ── STEP 4: Train the model ─────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
model = LinearRegression()
model.fit(X_train, y_train)

# ── STEP 5: Evaluate ────────────────────────────────────
preds = model.predict(X_test)
mae   = mean_absolute_error(y_test, preds)
print(f"MAE: ${mae:,.0f}")
# Output: MAE: $412

# ── STEP 6: Use it ──────────────────────────────────────
new_budget = [[5500]]
forecast   = model.predict(new_budget)
print(f"Forecast for $5,500 budget: ${forecast[0]:,.0f}")
# Forecast for $5,500 budget: $26,389""",
                "explanation": "Each step builds on the previous one. Notice how X is always 2D (double brackets [[...]]) because sklearn expects a table, not a list. The model never sees the test data during training — that's what makes the evaluation honest."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "df.isnull().sum()  # check missing values",
                    "X = df.drop('target', axis=1)",
                    "y = df['target']",
                    "train_test_split(X, y, test_size=0.2, random_state=42)",
                    "model.fit(X_train, y_train)",
                    "model.predict(X_test)"
                ],
                "notes": "Always use random_state=42 (or any fixed number) so your results are reproducible. Without it, the split changes every run."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "In the ML workflow, what happens BEFORE training the model?",
                    "options": [
                        "Deploy and monitor",
                        "Evaluate the model",
                        "Prepare and clean data",
                        "Tune hyperparameters"
                    ],
                    "answer": 2,
                    "explanation": "Data preparation (Step 3) must happen before training (Step 4). Skipping this leads to garbage-in, garbage-out."
                },
                {
                    "type": "true_false",
                    "question": "You should train your model first, then explore and clean the data.",
                    "answer": False,
                    "explanation": "Data exploration and preparation always come before training. Training on dirty data produces unreliable models."
                },
                {
                    "type": "fill_blank",
                    "question": "To separate features from the target column 'price', you write: X = df.___(columns=['price'], axis=1)",
                    "template": "X = df.___('price', axis=1)",
                    "answer": "drop",
                    "explanation": "df.drop('price', axis=1) removes the target column, leaving only the feature columns as your X matrix."
                }
            ],
            "challenge": {
                "instructions": "Follow the 6-step workflow. You have data about store locations: store_size (sqft), num_employees, and weekly_revenue. Step 1: the goal is to predict weekly_revenue. Step 2: create the DataFrame and print shape. Step 3: create X and y. Step 4: split 80/20 and fit a LinearRegression. Step 5: print predictions on the test set. Step 6: predict revenue for a new store with size=1800, employees=12.",
                "starter_code": "import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\n\ndata = {\n    'store_size':     [800, 1200, 1500, 2000, 2500, 3000, 1800, 2200],\n    'num_employees':  [4,   6,    8,    10,   13,   15,   9,    11  ],\n    'weekly_revenue': [12000,18000,24000,32000,41000,48000,28000,36000]\n}\ndf = pd.DataFrame(data)\n\n# Step 2: explore\n\n# Step 3: create X and y\n\n# Step 4: split and train\n\n# Step 5: print predictions\n\n# Step 6: predict for size=1800, employees=12\n",
                "tests": [
                    {"type": "code_contains", "value": "train_test_split"},
                    {"type": "code_contains", "value": ".fit("},
                    {"type": "code_contains", "value": ".predict("}
                ],
                "solution": "import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\ndata = {'store_size':[800,1200,1500,2000,2500,3000,1800,2200],'num_employees':[4,6,8,10,13,15,9,11],'weekly_revenue':[12000,18000,24000,32000,41000,48000,28000,36000]}\ndf = pd.DataFrame(data)\nprint(df.shape)\nX = df[['store_size','num_employees']]\ny = df['weekly_revenue']\nX_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)\nmodel = LinearRegression()\nmodel.fit(X_train,y_train)\nprint('Predictions:', model.predict(X_test))\nprint('New store revenue:', model.predict([[1800,12]]))"
            },
            "challenge_variations": [
                "Variation 1: Use delivery_distance [5,10,15,20,25,30] and delivery_time_min [12,22,35,45,58,70]. Follow all 6 steps and predict time for 18 miles.",
                "Variation 2: Use product_weight_kg [0.5,1,2,5,10,20] and shipping_cost [3,5,8,15,25,45]. Predict cost for 7 kg.",
                "Variation 3: Use office_temp_celsius [18,20,22,24,26,28] and employee_productivity [65,78,88,85,75,60]. Predict productivity at 23°C.",
                "Variation 4: Customer data: account_age_months [3,6,12,24,36,48] and lifetime_value [150,280,520,1100,1600,2200]. Predict LTV at 18 months.",
                "Variation 5: Use num_support_tickets [0,1,2,5,10,20] and churn_rate_pct [2,5,8,18,35,62]. Predict churn rate for 7 tickets.",
                "Variation 6: Use pages_visited [1,3,5,8,12,15] and conversion_rate_pct [1,3,6,10,14,17]. Predict rate for 10 pages.",
                "Variation 7: Use num_features [5,10,20,50,100,200] and model_training_time_sec [2,5,12,30,65,140]. Predict time for 75 features.",
                "Variation 8: Use daily_calls [10,25,50,100,200,400] and monthly_revenue [500,1200,2300,4500,8800,17000]. Predict for 150 calls/day.",
                "Variation 9: Use years_in_business [1,2,5,10,15,20] and annual_profit [8000,20000,60000,150000,210000,290000]. Predict for 8 years.",
                "Variation 10: Use discount_pct [0,5,10,15,20,25] and units_sold [100,130,165,205,250,300]. Predict units for 12% discount."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 3
        # ─────────────────────────────────────────────
        {
            "id": "m4-l3",
            "title": "Preparing Data for ML",
            "order": 3,
            "duration_min": 20,
            "real_world_context": "Raw business data is always messy — missing salaries, text categories, dates. Before any model can learn, you need to turn that messy reality into a clean numeric matrix. This lesson is where analysts spend 80% of their time.",
            "concept": """ML models only understand numbers. Your job in data preparation is to convert every real-world column into clean numbers.

**The Feature Matrix X and Target Vector y**

```python
import pandas as pd

df = pd.DataFrame({
    "experience": [2, 5, 3, 8, 1],
    "education":  ["BS", "MS", "BS", "PhD", "BS"],
    "city":       ["NYC", "LA", "NYC", "Chicago", "LA"],
    "salary":     [55000, 85000, 62000, 120000, 48000]
})

# X = all columns except what you're predicting
X = df.drop("salary", axis=1)  # features

# y = the column you ARE predicting
y = df["salary"]               # target
```

**Problem 1: Missing Values**

ML models crash on NaN (missing) values. You must handle them first.
```python
print(df.isnull().sum())    # count missing per column

# Strategy A — fill with median (best for skewed numbers like salary)
df["salary"].fillna(df["salary"].median(), inplace=True)

# Strategy B — fill with mean (works for normally distributed numbers)
df["age"].fillna(df["age"].mean(), inplace=True)

# Strategy C — fill with mode (best for categorical columns)
df["city"].fillna(df["city"].mode()[0], inplace=True)

# Strategy D — drop rows with missing values (only if very few)
df.dropna(inplace=True)
```

**Problem 2: Categorical (Text) Columns**

Models need numbers, not strings like "NYC" or "BS".

```python
# pd.get_dummies() — one-hot encoding
# Turns one text column into multiple 0/1 columns
df_encoded = pd.get_dummies(df, columns=["education", "city"])
print(df_encoded.columns.tolist())
# ['experience', 'salary', 'education_BS', 'education_MS',
#  'education_PhD', 'city_Chicago', 'city_LA', 'city_NYC']
```

Now every column is a number (0 or 1). This is called **one-hot encoding**.

**Problem 3: Ordering Categorical Data**

Sometimes categories have order (Low < Medium < High). Use label encoding:
```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["risk_level"] = le.fit_transform(["Low", "High", "Medium", "Low", "High"])
# Low→0, Medium→1 (or varies by alphabet), High→2
# Better approach for ordered categories:
risk_map = {"Low": 0, "Medium": 1, "High": 2}
df["risk_level"] = df["risk_level"].map(risk_map)
```

**The Full Prep Pipeline:**
```python
import pandas as pd

df = pd.read_csv("employees.csv")

# 1. Handle missing values
df["salary"].fillna(df["salary"].median(), inplace=True)
df["department"].fillna("Unknown", inplace=True)

# 2. Encode categoricals
df = pd.get_dummies(df, columns=["department", "region"])

# 3. Separate X and y
X = df.drop("left_company", axis=1)
y = df["left_company"]

print("X shape:", X.shape)
# X shape: (1000, 24)  — 1000 rows, 24 numeric features
print("y shape:", y.shape)
# y shape: (1000,)
```""",
            "worked_example": {
                "description": "Preparing a messy employee dataset with missing values and text columns for ML.",
                "code": """import pandas as pd
import numpy as np

# Messy real-world data
data = {
    "years_exp":  [3, 7, np.nan, 5, 2, 9, 4],
    "department": ["Sales", "Eng", "Sales", "HR", "Eng", "HR", np.nan],
    "remote":     ["Yes", "No", "Yes", "No", "Yes", "No", "Yes"],
    "salary":     [55000, 92000, 58000, 61000, 50000, 88000, 57000]
}
df = pd.DataFrame(data)

print("=== BEFORE PREP ===")
print(df)
print("\\nMissing values:")
print(df.isnull().sum())

# ── Step 1: Fix missing values ──────────────────────────
df["years_exp"].fillna(df["years_exp"].median(), inplace=True)
df["department"].fillna("Unknown", inplace=True)

# ── Step 2: Encode text columns ──────────────────────────
df["remote"] = df["remote"].map({"Yes": 1, "No": 0})
df = pd.get_dummies(df, columns=["department"])

# ── Step 3: Separate X and y ─────────────────────────────
X = df.drop("salary", axis=1)
y = df["salary"]

print("\\n=== AFTER PREP ===")
print(X)
print("\\nX shape:", X.shape)
# X shape: (7, 6)
print("\\nColumn names:", X.columns.tolist())
# ['years_exp', 'remote', 'department_Eng', 'department_HR',
#  'department_Sales', 'department_Unknown']""",
                "explanation": "Notice how 'department' became 3 separate 0/1 columns (one per unique value) and 'remote' became a single 0/1 column. There are no NaN values or text strings left — only numbers. sklearn is now happy."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "df.isnull().sum()  # count missing values",
                    "df['col'].fillna(df['col'].median(), inplace=True)",
                    "pd.get_dummies(df, columns=['col'])  # one-hot encode",
                    "df['col'].map({'Yes':1, 'No':0})  # manual mapping",
                    "X = df.drop('target', axis=1)",
                    "y = df['target']"
                ],
                "notes": "Use median (not mean) for skewed financial data like salary or revenue — outliers distort the mean. Use mode for categorical columns."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A column contains ['Small', 'Large', 'Medium', 'Small']. What technique converts this to numbers sklearn can use?",
                    "options": [
                        "fillna()",
                        "One-hot encoding with pd.get_dummies()",
                        "train_test_split()",
                        "model.fit()"
                    ],
                    "answer": 1,
                    "explanation": "pd.get_dummies() converts text categories into multiple 0/1 columns — one per unique value. This is called one-hot encoding."
                },
                {
                    "type": "true_false",
                    "question": "It is fine to leave NaN (missing) values in your data before calling model.fit().",
                    "answer": False,
                    "explanation": "sklearn models will raise a ValueError if they encounter NaN values. You must handle missing values in the preparation step."
                },
                {
                    "type": "fill_blank",
                    "question": "To fill missing values in the 'age' column with the median age, you write:",
                    "template": "df['age'].fillna(df['age'].___(), inplace=True)",
                    "answer": "median",
                    "explanation": "median() is preferred over mean() for financial or skewed data because it is not affected by extreme outliers."
                }
            ],
            "challenge": {
                "instructions": "You have a raw customer DataFrame with missing values and text columns. Your tasks: (1) Fill missing 'purchase_amount' with the median. (2) Fill missing 'region' with 'Unknown'. (3) One-hot encode 'region' using pd.get_dummies(). (4) Map 'subscribed' Yes/No to 1/0. (5) Create X (drop 'churned') and y ('churned'). (6) Print X.shape and X.columns.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\ndata = {\n    'purchase_amount': [120, np.nan, 340, 89, np.nan, 210, 450, 175],\n    'region':          ['North','South', np.nan,'East','West','North','South','East'],\n    'subscribed':      ['Yes','No','Yes','Yes','No','Yes','No','Yes'],\n    'churned':         [0, 1, 0, 0, 1, 0, 1, 0]\n}\ndf = pd.DataFrame(data)\n\n# 1. Fill missing purchase_amount with median\n\n# 2. Fill missing region with 'Unknown'\n\n# 3. One-hot encode 'region'\n\n# 4. Map subscribed to 1/0\n\n# 5. Create X and y\n\n# 6. Print X.shape and X.columns\n",
                "tests": [
                    {"type": "code_contains", "value": "get_dummies"},
                    {"type": "code_contains", "value": "fillna"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\ndata = {'purchase_amount':[120,np.nan,340,89,np.nan,210,450,175],'region':['North','South',np.nan,'East','West','North','South','East'],'subscribed':['Yes','No','Yes','Yes','No','Yes','No','Yes'],'churned':[0,1,0,0,1,0,1,0]}\ndf = pd.DataFrame(data)\ndf['purchase_amount'].fillna(df['purchase_amount'].median(),inplace=True)\ndf['region'].fillna('Unknown',inplace=True)\ndf = pd.get_dummies(df,columns=['region'])\ndf['subscribed'] = df['subscribed'].map({'Yes':1,'No':0})\nX = df.drop('churned',axis=1)\ny = df['churned']\nprint(X.shape)\nprint(X.columns.tolist())"
            },
            "challenge_variations": [
                "Variation 1: Create a product DataFrame with price (some NaN), category (text), and in_stock (Yes/No). Prep it for ML with target = 'sold'.",
                "Variation 2: Employee data with age (some NaN), department (text), gender (M/F), and target = 'promoted'. Handle all missing values and encode all categoricals.",
                "Variation 3: Loan data with income (NaN values), employment_type ('Full','Part','Self'), credit_score, and target = 'approved'. Prep fully.",
                "Variation 4: Housing data with num_rooms, neighborhood (text with NaNs), has_garage (Yes/No), and target = 'sold_above_asking'. Prep for ML.",
                "Variation 5: Student data with gpa (some NaN), major (text), scholarship (Yes/No), and target = 'graduated_on_time'. Full prep pipeline.",
                "Variation 6: Sales rep data with calls_per_day, territory (text), experience_level (Low/Mid/Senior ordered), and target = 'hit_quota'. Use map() for ordered encoding.",
                "Variation 7: Hospital data with patient_age (NaN), admission_type (Emergency/Routine/Elective), insurance (Yes/No), and target = 'readmitted'. Full prep.",
                "Variation 8: E-commerce data with session_duration (NaN), device_type (Mobile/Desktop/Tablet), returning_customer (Yes/No), and target = 'purchased'. Prep it.",
                "Variation 9: Restaurant review data with num_visits, cuisine_type (text), delivery_available (Yes/No), avg_rating (some NaN), and target = 'closed_within_year'.",
                "Variation 10: Job listing data with required_experience (NaN), job_type (Full/Part/Contract), remote_ok (Yes/No), and target = 'filled_within_week'."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 4
        # ─────────────────────────────────────────────
        {
            "id": "m4-l4",
            "title": "Train/Test Split — Honest Evaluation",
            "order": 4,
            "duration_min": 15,
            "real_world_context": "Would you study with the exam answers and then claim you know the material? That's what happens when you evaluate a model on training data. The train/test split is how ML maintains honesty.",
            "concept": """**The Core Problem: Cheating Without Knowing It**

If you train and evaluate your model on the same data, your model will look great — because it has already *memorized* that data. But it will fail on new, unseen data. This is the most common beginner mistake.

```python
# WRONG — this is cheating!
model.fit(X, y)
accuracy = model.score(X, y)    # evaluating on training data
print(accuracy)
# Output: 0.97  ← Looks amazing but is meaningless!

# RIGHT — evaluate on data the model has never seen
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)        # train on 80%
accuracy = model.score(X_test, y_test)  # evaluate on held-out 20%
print(accuracy)
# Output: 0.84  ← Honest estimate of real-world performance
```

**Understanding train_test_split()**

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,           # feature matrix
    y,           # target vector
    test_size=0.2,     # 20% for testing, 80% for training
    random_state=42    # "seed" — makes the split reproducible
)

print(f"Training rows:  {len(X_train)}")  # Training rows:  800
print(f"Testing rows:   {len(X_test)}")   # Testing rows:   200
```

**What random_state Does**

train_test_split randomly shuffles data before splitting. Without random_state, you get a different split every run — different results every time.
```python
# Same data, different random_state → different splits
X_tr1, X_te1, _, _ = train_test_split(X, y, test_size=0.2, random_state=0)
X_tr2, X_te2, _, _ = train_test_split(X, y, test_size=0.2, random_state=99)

# X_tr1 and X_tr2 will contain different rows!
# Fix: always use the same random_state for reproducible experiments
```

**The Golden Rule: Never Peek at the Test Set**
Treat your test set like a sealed envelope. Rules:
- Never use test data to make any decisions about the model
- Never retrain on test data after evaluation
- Never tune parameters based on test performance
- The test set is used ONCE, at the very end, to get the final score

**Common Split Sizes:**
```
test_size=0.20 → 80% train, 20% test  (most common for medium datasets)
test_size=0.25 → 75% train, 25% test
test_size=0.30 → 70% train, 30% test  (common for small datasets)
```

**Stratified Splitting (for classification)**

When predicting categories, make sure both splits have the same proportion of each class:
```python
# stratify=y ensures equal class distribution in train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```""",
            "worked_example": {
                "description": "Demonstrating the difference between training accuracy and test accuracy — and why test accuracy is the only one that matters.",
                "code": """import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Customer churn dataset
np.random.seed(42)
n = 200
X = pd.DataFrame({
    "tenure_months":  np.random.randint(1, 60, n),
    "monthly_charges": np.random.uniform(20, 100, n),
    "num_tickets":    np.random.randint(0, 15, n)
})
y = (X["num_tickets"] > 8).astype(int)  # churn if many complaints

# WRONG way: evaluate on training data
model_wrong = DecisionTreeClassifier(random_state=42)
model_wrong.fit(X, y)
train_acc = accuracy_score(y, model_wrong.predict(X))
print(f"[WRONG] Training accuracy: {train_acc:.1%}")
# [WRONG] Training accuracy: 100.0% ← memorized the data!

# RIGHT way: honest train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model_right = DecisionTreeClassifier(random_state=42)
model_right.fit(X_train, y_train)

train_acc = accuracy_score(y_train, model_right.predict(X_train))
test_acc  = accuracy_score(y_test,  model_right.predict(X_test))

print(f"[RIGHT] Training accuracy: {train_acc:.1%}")
print(f"[RIGHT] Test accuracy:     {test_acc:.1%}")
# [RIGHT] Training accuracy: 100.0%
# [RIGHT] Test accuracy:     95.0%  ← honest estimate""",
                "explanation": "The model trained on all data shows 100% training accuracy — but that is useless because it memorized answers. The model trained properly shows a realistic test accuracy. Notice training accuracy is usually higher than test accuracy; that is normal."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "from sklearn.model_selection import train_test_split",
                    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
                    "model.fit(X_train, y_train)",
                    "model.score(X_test, y_test)",
                    "stratify=y  # for balanced class splits"
                ],
                "notes": "The Golden Rule: never make ANY model decisions based on test set performance. Use it once, at the very end, for the final evaluation."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "You train a model and evaluate it on the same data. It scores 99% accuracy. What does this most likely indicate?",
                    "options": [
                        "The model is excellent and ready to deploy",
                        "The model memorized the training data (overfitting)",
                        "The dataset is too small",
                        "You need more features"
                    ],
                    "answer": 1,
                    "explanation": "Evaluating on training data almost always gives artificially high scores because the model has seen those exact examples before. This is overfitting."
                },
                {
                    "type": "true_false",
                    "question": "random_state=42 in train_test_split ensures the same rows end up in train and test sets every time the code runs.",
                    "answer": True,
                    "explanation": "random_state sets a seed for the random number generator, making the shuffle — and therefore the split — identical every run. Essential for reproducibility."
                },
                {
                    "type": "fill_blank",
                    "question": "To use 25% of data for testing, you set test_size=___",
                    "template": "train_test_split(X, y, test_size=___, random_state=42)",
                    "answer": "0.25",
                    "explanation": "test_size accepts a float between 0 and 1 representing the fraction of data for testing. 0.25 means 25% test, 75% train."
                }
            ],
            "challenge": {
                "instructions": "Create a DataFrame with 100 rows: 'hours_studied' (random 1-10), 'sleep_hours' (random 5-9), and 'passed' (1 if hours_studied > 6 else 0). Split 80/20 with random_state=0. Fit a DecisionTreeClassifier. Print both the training accuracy AND test accuracy. Confirm they are different numbers.",
                "starter_code": "import pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nnp.random.seed(0)\nn = 100\ndf = pd.DataFrame({\n    'hours_studied': np.random.randint(1, 11, n),\n    'sleep_hours':   np.random.uniform(5, 9, n),\n    'passed':        (np.random.randint(1,11,n) > 6).astype(int)\n})\n\nX = df[['hours_studied', 'sleep_hours']]\ny = df['passed']\n\n# Split 80/20 with random_state=0\n\n# Fit DecisionTreeClassifier\n\n# Print training accuracy\n\n# Print test accuracy\n",
                "tests": [
                    {"type": "code_contains", "value": "train_test_split"},
                    {"type": "code_contains", "value": "accuracy_score"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\nnp.random.seed(0)\nn=100\ndf=pd.DataFrame({'hours_studied':np.random.randint(1,11,n),'sleep_hours':np.random.uniform(5,9,n),'passed':(np.random.randint(1,11,n)>6).astype(int)})\nX=df[['hours_studied','sleep_hours']]\ny=df['passed']\nX_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)\nmodel=DecisionTreeClassifier(random_state=0)\nmodel.fit(X_train,y_train)\nprint('Train accuracy:',accuracy_score(y_train,model.predict(X_train)))\nprint('Test accuracy:', accuracy_score(y_test, model.predict(X_test)))"
            },
            "challenge_variations": [
                "Variation 1: With a 500-row sales dataset, compare train vs test accuracy using 70/30 split. Which is higher and why?",
                "Variation 2: Split the same dataset twice — once with random_state=1 and once with random_state=99. Print the first 5 rows of each X_train to show they differ.",
                "Variation 3: Create a credit risk dataset (income, debt_ratio, credit_score → approved). Use stratify=y and verify both train and test have similar ratios of 0s and 1s.",
                "Variation 4: Use test_size=0.1 (90/10 split) on a 200-row dataset. Print how many rows are in each split and discuss whether this is enough test data.",
                "Variation 5: Intentionally train on all data and evaluate on all data. Print that accuracy. Then do a proper 80/20 split and compare. Comment on the difference.",
                "Variation 6: Create customer data (age, monthly_spend, num_products → churned). Split 75/25. Train a LogisticRegression. Print train and test accuracy.",
                "Variation 7: With employee data (years_exp, salary, dept_encoded → promoted), show that training accuracy is always >= test accuracy by trying 3 different random_state values.",
                "Variation 8: Demonstrate what happens when you call train_test_split without random_state — run it twice and show the test sets are different.",
                "Variation 9: Use a very small dataset (20 rows). Try test_size=0.2 and 0.3. Print the train/test row counts for each. When does the test set become too small to be useful?",
                "Variation 10: Create a multi-class target (low/mid/high churn) and use stratify=y. Print value_counts() on y_train and y_test to confirm proportions match."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 5
        # ─────────────────────────────────────────────
        {
            "id": "m4-l5",
            "title": "Linear Regression — Predicting Numbers",
            "order": 5,
            "duration_min": 20,
            "real_world_context": "Forecasting next quarter's revenue, estimating a property's value, predicting how many units will sell — these are all regression problems. Linear Regression is the most important model in business analytics.",
            "concept": """**What is Regression?**

Regression predicts a *continuous number* — like salary, price, or sales volume. It answers the question: "How much?"

**The Intuition: Fitting a Line**

Imagine plotting years of experience (x-axis) vs. salary (y-axis). Each employee is a dot. Linear Regression draws the best-fit line through those dots.

```
salary = (slope × experience) + intercept
salary = (11,200 × years) + 35,000
```

Once you have the line, predicting is just plugging in a number:
```
5 years → (11,200 × 5) + 35,000 = $91,000
```

**Implementing with sklearn**

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Business dataset: advertising spend → sales
data = {
    "tv_ads":      [230, 44, 17, 151, 181, 8, 57, 120, 199, 66],
    "radio_ads":   [37, 39, 45, 41, 10, 48, 32, 19, 36, 23],
    "sales":       [22, 10, 9, 18, 13, 7, 12, 14, 21, 12]
}
df = pd.DataFrame(data)

X = df[["tv_ads", "radio_ads"]]
y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Create the model
model = LinearRegression()

# .fit() is where learning happens — finds the best line
model.fit(X_train, y_train)

# .predict() applies the formula to new data
predictions = model.predict(X_test)
print("Predictions:", predictions.round(1))
# Predictions: [14.2  9.8 21.4 12.1]
print("Actual:     ", y_test.values)
# Actual:      [14  10  21  12]
```

**Inspecting the Model**

```python
# The slope(s): how much y changes per unit of x
print("Coefficients:", model.coef_)
# Coefficients: [0.054  0.112]
# → each $1 more in TV ads → +$0.054K sales
# → each $1 more in radio ads → +$0.112K sales

# The intercept: y-value when all X = 0
print("Intercept:", round(model.intercept_, 2))
# Intercept: 4.63

# Predict for a specific scenario
new_campaign = pd.DataFrame({"tv_ads": [200], "radio_ads": [40]})
forecast = model.predict(new_campaign)
print(f"Predicted sales: ${forecast[0]*1000:,.0f}")
# Predicted sales: $19,310
```

**Business Use Cases for Linear Regression:**
- Forecast quarterly revenue from marketing spend
- Predict employee salary from years of experience and education
- Estimate energy consumption from building size and occupancy
- Model house prices from square footage, bedrooms, and location
- Predict delivery time from distance and package weight""",
            "worked_example": {
                "description": "Building a salary prediction model for an HR analytics dashboard.",
                "code": """import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# HR dataset: predict employee salary
data = {
    "years_exp":      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "performance":    [3, 4, 3, 5, 4, 5, 4, 5, 5, 5,  4,  5 ],
    "salary_k":       [42,48,52,60,65,72,78,85,90,98,102,110]
}
df = pd.DataFrame(data)

X = df[["years_exp", "performance"]]
y = df["salary_k"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
preds = model.predict(X_test)

print("Actual salaries (test):    ", y_test.values)
# Actual salaries (test):     [ 48  72  42 110]
print("Predicted salaries (test): ", preds.round(1))
# Predicted salaries (test):  [ 50.2  71.8  43.1 108.9]

mae = mean_absolute_error(y_test, preds)
print(f"\\nOn average, predictions are off by: ${mae*1000:,.0f}")
# On average, predictions are off by: $1,650

# Interpret the model
print("\\nModel Formula:")
print(f"  salary = {model.coef_[0]:.1f} × years_exp")
print(f"          + {model.coef_[1]:.1f} × performance")
print(f"          + {model.intercept_:.1f}")
# salary = 6.4 × years_exp + 4.8 × performance + 24.1

# Predict for a new hire: 4 years exp, performance rating 4
new_hire = pd.DataFrame({"years_exp": [4], "performance": [4]})
predicted_salary = model.predict(new_hire)[0]
print(f"\\nNew hire salary estimate: ${predicted_salary*1000:,.0f}")
# New hire salary estimate: $69,700""",
                "explanation": "The model learned that each year of experience adds about $6,400 to salary and each performance point adds $4,800. These coefficients are the 'rules' the model discovered from data — you did not have to write them yourself."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "from sklearn.linear_model import LinearRegression",
                    "model = LinearRegression()",
                    "model.fit(X_train, y_train)",
                    "model.predict(X_new)",
                    "model.coef_  # slope(s)",
                    "model.intercept_  # y-intercept"
                ],
                "notes": "X must always be 2D — use double brackets df[['col']] or .reshape(-1,1) for a single feature. y can be 1D."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "model.coef_ for a Linear Regression with two features returns [3.5, -0.8]. What does -0.8 mean for the second feature?",
                    "options": [
                        "Each unit increase in the second feature decreases the prediction by 0.8",
                        "The model is 80% accurate",
                        "The second feature is not important",
                        "The intercept is -0.8"
                    ],
                    "answer": 0,
                    "explanation": "Each coefficient tells you how much y changes when that feature increases by 1 (all others held constant). A negative coefficient means the feature negatively impacts the prediction."
                },
                {
                    "type": "true_false",
                    "question": "Linear Regression is used to predict a category (like 'approved' or 'denied').",
                    "answer": False,
                    "explanation": "Linear Regression predicts continuous numbers (salary, price, revenue). For categories (yes/no, A/B/C), use classification models like Logistic Regression."
                },
                {
                    "type": "fill_blank",
                    "question": "After fitting a model, to get predictions on new data you call model.___( X_new )",
                    "template": "predictions = model.___(X_new)",
                    "answer": "predict",
                    "explanation": "model.predict() applies the learned formula to new input data and returns predicted values."
                }
            ],
            "challenge": {
                "instructions": "Build a house price prediction model. Data: square_feet [1000,1500,2000,2500,3000,3500,4000,4500,5000], num_bathrooms [1,1,2,2,3,3,4,4,5], and price_k [180,240,310,375,450,520,600,680,760]. Create X with both features and y as price_k. Split 80/20 random_state=42. Fit LinearRegression. Print: predictions on test set, actual values, model coefficients, and prediction for a 2750 sqft house with 3 bathrooms.",
                "starter_code": "import pandas as pd\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\n\ndata = {\n    'square_feet':    [1000,1500,2000,2500,3000,3500,4000,4500,5000],\n    'num_bathrooms':  [1,   1,   2,   2,   3,   3,   4,   4,   5   ],\n    'price_k':        [180, 240, 310, 375, 450, 520, 600, 680, 760 ]\n}\ndf = pd.DataFrame(data)\n\n# Create X and y\n\n# Split 80/20\n\n# Fit model\n\n# Print predictions vs actuals\n\n# Print coefficients\n\n# Predict for 2750 sqft, 3 bathrooms\n",
                "tests": [
                    {"type": "code_contains", "value": "LinearRegression"},
                    {"type": "code_contains", "value": "model.coef_"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\ndata={'square_feet':[1000,1500,2000,2500,3000,3500,4000,4500,5000],'num_bathrooms':[1,1,2,2,3,3,4,4,5],'price_k':[180,240,310,375,450,520,600,680,760]}\ndf=pd.DataFrame(data)\nX=df[['square_feet','num_bathrooms']]\ny=df['price_k']\nX_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)\nmodel=LinearRegression()\nmodel.fit(X_train,y_train)\npreds=model.predict(X_test)\nprint('Predictions:',preds.round(1))\nprint('Actual:',y_test.values)\nprint('Coefficients:',model.coef_)\nprint('Intercept:',model.intercept_)\nprint('2750sqft 3bath:',[model.predict([[2750,3]])[0]])"
            },
            "challenge_variations": [
                "Variation 1: Predict monthly electricity bill (kWh) from building_size and avg_temperature. Find the coefficient for temperature.",
                "Variation 2: Predict student_gpa from study_hours and sleep_hours. Which feature has a larger coefficient?",
                "Variation 3: Predict delivery_time from distance and num_stops. Print the model equation as a readable string.",
                "Variation 4: Predict store_revenue from foot_traffic and avg_transaction_value. Print predictions for 3 new store scenarios.",
                "Variation 5: Predict employee_productivity from years_experience and training_hours. What happens to productivity per training hour?",
                "Variation 6: Use only ONE feature (square_feet) to predict price. Compare model.coef_ and intercept_ to a 2-feature model.",
                "Variation 7: Predict quarterly_profit from num_customers and avg_order_value. Use test_size=0.3. Print the R² score (model.score).",
                "Variation 8: Build a model on website_traffic and conversion_rate to predict monthly_revenue. Predict for 5 new traffic/conversion scenarios.",
                "Variation 9: Create a model from scratch: define the data, build, train, predict, and print a formatted 'Model Report' with coefficients and 3 predictions.",
                "Variation 10: Predict insurance_premium from age and bmi. Evaluate with both model.score() and manually compute mean absolute error."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 6
        # ─────────────────────────────────────────────
        {
            "id": "m4-l6",
            "title": "Evaluating Regression — Did Your Model Work?",
            "order": 6,
            "duration_min": 20,
            "real_world_context": "A model that's off by $5,000 on a $50,000 salary prediction is very different from one that's off by $5,000 on a $500,000 house. Regression metrics help you measure error in business-meaningful terms.",
            "concept": """After making predictions, you need to measure *how wrong* you are. Each metric tells a different story.

**The Four Key Regression Metrics**

**MAE — Mean Absolute Error** (easiest to interpret)
> On average, how many units off are my predictions?
```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, predictions)
print(f"MAE: ${mae:,.0f}")
# MAE: $4,200
# Interpretation: on average, predictions are off by $4,200
```

**MSE — Mean Squared Error** (penalizes large errors more)
> Average of squared errors — punishes big mistakes heavily
```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_test, predictions)
print(f"MSE: {mse:,.0f}")
# MSE: 31,500,000  ← hard to interpret directly (it's in squared dollars)
```

**RMSE — Root Mean Squared Error** (most commonly reported)
> Square root of MSE — back in original units, but penalizes outliers
```python
import numpy as np

rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"RMSE: ${rmse:,.0f}")
# RMSE: $5,612  ← same units as salary, but more sensitive to large errors
```

**R² — R-Squared (Coefficient of Determination)** (intuitive %)
> What percentage of the variation in y does the model explain?
```python
from sklearn.metrics import r2_score

r2 = r2_score(y_test, predictions)
print(f"R²: {r2:.3f}")
# R²: 0.847  → model explains 84.7% of salary variation

# Also available as:
r2 = model.score(X_test, y_test)
```

**Interpreting R²:**
```
R² = 1.0  → perfect predictions (impossible in practice)
R² = 0.9  → excellent (90% of variation explained)
R² = 0.7  → good for many business problems
R² = 0.5  → moderate — might be acceptable or might need work
R² = 0.0  → no better than predicting the mean every time
R² < 0.0  → worse than predicting the mean (your model is broken)
```

**Visualizing Residuals** (the errors)

A good model has residuals (actual - predicted) randomly scattered around 0:
```python
import matplotlib.pyplot as plt

residuals = y_test - predictions

plt.scatter(predictions, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals (Actual - Predicted)")
plt.title("Residual Plot")
plt.show()
# If residuals fan out (get bigger as predictions grow),
# your model has problems with larger values
```

**Overfitting Warning Signs:**
```python
train_r2 = model.score(X_train, y_train)
test_r2  = model.score(X_test, y_test)

print(f"Train R²: {train_r2:.3f}")  # Train R²: 0.985
print(f"Test R²:  {test_r2:.3f}")   # Test R²:  0.612
# Large gap = overfitting. Model memorized training data but generalizes poorly.
```""",
            "worked_example": {
                "description": "Evaluating a house price regression model and diagnosing whether it is reliable.",
                "code": """import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Housing data
np.random.seed(42)
n = 100
df = pd.DataFrame({
    'sqft':     np.random.randint(800, 4000, n),
    'bedrooms': np.random.randint(1, 6, n),
    'age':      np.random.randint(0, 40, n),
    'price':    np.random.randint(800, 4000, n) * 110 + np.random.normal(0, 15000, n)
})

X = df[['sqft', 'bedrooms', 'age']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)

# ── All four metrics ─────────────────────────────────
mae  = mean_absolute_error(y_test, preds)
mse  = mean_squared_error(y_test, preds)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, preds)

print("=== Model Evaluation Report ===")
print(f"MAE:  ${mae:>12,.0f}  (avg error per house)")
print(f"RMSE: ${rmse:>12,.0f}  (penalizes large errors)")
print(f"R²:   {r2:>12.3f}  (variation explained)")

# Check for overfitting
train_r2 = model.score(X_train, y_train)
print(f"\\nTrain R²: {train_r2:.3f}")
print(f"Test R²:  {r2:.3f}")
gap = train_r2 - r2
print(f"Gap:      {gap:.3f}", "← possible overfit" if gap > 0.1 else "← looks healthy")""",
                "explanation": "MAE gives you the plain-English interpretation: predictions are off by $X on average. RMSE is larger than MAE when there are occasional large errors. The train/test R² gap tells you about overfitting — a gap larger than 0.1 is a warning sign."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score",
                    "mae  = mean_absolute_error(y_test, preds)",
                    "rmse = np.sqrt(mean_squared_error(y_test, preds))",
                    "r2   = r2_score(y_test, preds)",
                    "model.score(X_test, y_test)  # same as r2_score"
                ],
                "notes": "For business reports, use MAE — it's in the same units as your target and easy to explain to stakeholders. R² is great for comparing models."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Your model has Train R² = 0.97 and Test R² = 0.58. What does this most likely indicate?",
                    "options": [
                        "The model is generalizing well",
                        "The test set is too small",
                        "The model is overfitting — it memorized training data",
                        "You need more features"
                    ],
                    "answer": 2,
                    "explanation": "A large gap between train and test R² (0.97 vs 0.58) is a classic sign of overfitting. The model performed well on training data but failed to generalize."
                },
                {
                    "type": "true_false",
                    "question": "An R² of 0.75 means the model's predictions are 75% accurate.",
                    "answer": False,
                    "explanation": "R² = 0.75 means the model explains 75% of the variance in the target variable. It does not mean predictions are within 75% of the true value. Use MAE for that interpretation."
                },
                {
                    "type": "fill_blank",
                    "question": "MAE measures the ___ absolute difference between actual and predicted values.",
                    "template": "mae = mean_absolute_error(y_test, predictions)  # gives the ___ error",
                    "answer": "mean",
                    "explanation": "MAE = Mean Absolute Error. It averages the absolute value of each (actual - predicted) difference, giving you the typical error magnitude in original units."
                }
            ],
            "challenge": {
                "instructions": "Using the salary dataset (years_exp, education_encoded, salary), train a LinearRegression and compute all four evaluation metrics: MAE, MSE, RMSE, and R². Print them in a formatted report. Then print both train R² and test R² and comment (with a print statement) on whether the model is overfitting.",
                "starter_code": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n\ndata = {\n    'years_exp':  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],\n    'edu_level':  [1,1,2,1,2,3,2,3,3,2, 3, 3, 2, 3, 3 ],\n    'salary_k':   [42,48,56,58,65,78,75,88,94,92,105,112,98,118,125]\n}\ndf = pd.DataFrame(data)\n\nX = df[['years_exp','edu_level']]\ny = df['salary_k']\n\n# Split 80/20 random_state=42\n\n# Fit LinearRegression\n\n# Compute and print MAE, MSE, RMSE, R²\n\n# Print train R² and test R², comment on overfitting\n",
                "tests": [
                    {"type": "code_contains", "value": "mean_absolute_error"},
                    {"type": "code_contains", "value": "r2_score"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score\ndata={'years_exp':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],'edu_level':[1,1,2,1,2,3,2,3,3,2,3,3,2,3,3],'salary_k':[42,48,56,58,65,78,75,88,94,92,105,112,98,118,125]}\ndf=pd.DataFrame(data)\nX=df[['years_exp','edu_level']]\ny=df['salary_k']\nX_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)\nmodel=LinearRegression()\nmodel.fit(X_train,y_train)\npreds=model.predict(X_test)\nmae=mean_absolute_error(y_test,preds)\nmse=mean_squared_error(y_test,preds)\nrmse=np.sqrt(mse)\nr2=r2_score(y_test,preds)\nprint(f'MAE: {mae:.2f}k')\nprint(f'MSE: {mse:.2f}')\nprint(f'RMSE: {rmse:.2f}k')\nprint(f'R2: {r2:.3f}')\ntrain_r2=model.score(X_train,y_train)\nprint(f'Train R2: {train_r2:.3f} | Test R2: {r2:.3f}')\nprint('Overfitting' if train_r2-r2>0.1 else 'No major overfitting detected')"
            },
            "challenge_variations": [
                "Variation 1: Evaluate a marketing spend → sales model. Which metric would you report to the VP of Sales and why?",
                "Variation 2: Create two models (one with 1 feature, one with 3 features). Compare their R² scores. Does more features always help?",
                "Variation 3: Deliberately overfit a model using DecisionTreeRegressor(max_depth=None). Compare train vs test RMSE.",
                "Variation 4: Predict house price and report MAE as a percentage of the average house price. Is 5% good? 15%?",
                "Variation 5: Build a delivery time model. Print a readable error report including what MAE means in plain English for a logistics manager.",
                "Variation 6: Train on 50% of data and evaluate. Then train on 80%. Compare R² values — how does training size affect performance?",
                "Variation 7: What is the baseline RMSE if you always predict the mean y value? Compare it to your model's RMSE.",
                "Variation 8: Plot predicted vs actual values (scatter plot). A perfect model has all points on the y=x diagonal line.",
                "Variation 9: Compute residuals (actual - predicted). Print their mean and std. A good model has residuals centered near 0.",
                "Variation 10: Create a 'Model Evaluation Dashboard' function that takes y_test and preds and prints all 4 metrics in one formatted block."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 7
        # ─────────────────────────────────────────────
        {
            "id": "m4-l7",
            "title": "Logistic Regression — Predicting Yes/No",
            "order": 7,
            "duration_min": 20,
            "real_world_context": "Will this customer churn? Will this loan default? Will this email be spam? These are classification problems — the answer is a category, not a number. Logistic Regression is the most interpretable classifier in business.",
            "concept": """**Classification vs. Regression — What's the Difference?**

| | Regression | Classification |
|---|---|---|
| Question | How much? | Which category? |
| Output | A number (e.g., $85,000) | A label (e.g., "Churn" / "Stay") |
| Example | Predict salary | Predict if customer will leave |
| Algorithm | Linear Regression | Logistic Regression |

**The Sigmoid Function — Turning Numbers into Probabilities**

Logistic Regression doesn't directly output a 0 or 1. It outputs a *probability* between 0 and 1, then uses a threshold (usually 0.5) to classify:

```
probability = sigmoid(linear_combination_of_features)
prediction  = 1  if probability >= 0.5  else  0
```

The sigmoid squeezes any number into the (0, 1) range. Think of it like a smooth on/off switch.

**Implementing Logistic Regression**

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Customer churn dataset
data = {
    "tenure_months":    [2, 34, 5, 60, 7, 44, 12, 2, 56, 15],
    "monthly_charges":  [70, 55, 85, 45, 80, 50, 65, 90, 40, 72],
    "num_complaints":   [5, 0, 4, 0, 3, 1, 2, 6, 0, 3],
    "churned":          [1, 0, 1, 0, 1, 0, 0, 1, 0, 1]
}
df = pd.DataFrame(data)

X = df.drop("churned", axis=1)
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

# Hard predictions: 0 or 1
predictions = model.predict(X_test)
print("Predicted classes:", predictions)
# Predicted classes: [1 0 1 0]

# Accuracy
print(f"Accuracy: {accuracy_score(y_test, predictions):.1%}")
# Accuracy: 75.0%
```

**Getting Probability Scores (Very Useful in Business)**

```python
# predict_proba() gives probabilities for each class
proba = model.predict_proba(X_test)
print(proba)
# [[0.21, 0.79],   ← 79% chance of churning
#  [0.88, 0.12],   ← 12% chance of churning
#  [0.15, 0.85],   ← 85% chance of churning
#  [0.73, 0.27]]   ← 27% chance of churning

# Get just the probability of churning (class 1)
churn_proba = proba[:, 1]
print("Churn probabilities:", churn_proba.round(2))
# Churn probabilities: [0.79 0.12 0.85 0.27]
```

**Why Probabilities Are Valuable in Business:**
Instead of a binary "will churn / won't churn", you can:
- Rank customers by risk score
- Target only the top 20% highest-risk customers for a retention call
- Set a custom threshold (e.g., flag anyone with >30% probability)
- Calculate expected cost of churn across your whole customer base""",
            "worked_example": {
                "description": "Building a loan approval classifier that outputs both decisions and probability scores.",
                "code": """import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Loan applicant data
np.random.seed(42)
n = 12
data = {
    "credit_score":   [720, 580, 650, 800, 540, 710, 690, 760, 620, 550, 730, 670],
    "income_k":       [65,  35,  50,  90,  28,  70,  58,  85,  42,  32,  78,  55 ],
    "debt_ratio":     [0.2, 0.5, 0.4, 0.1, 0.6, 0.2, 0.3, 0.1, 0.5, 0.7, 0.2, 0.3],
    "approved":       [1,   0,   1,   1,   0,   1,   1,   1,   0,   0,   1,   1  ]
}
df = pd.DataFrame(data)

X = df.drop("approved", axis=1)
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Hard predictions
preds = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]  # probability of approval

print("=== Loan Approval Results ===")
print(f"{'Credit':>8} {'Income':>8} {'Debt':>6} | {'Actual':>8} {'Predicted':>10} {'Approval%':>10}")
print("-" * 60)
for i in range(len(X_test)):
    row = X_test.iloc[i]
    print(f"{row['credit_score']:>8.0f} {row['income_k']:>8.0f} {row['debt_ratio']:>6.1f} | "
          f"{y_test.iloc[i]:>8} {preds[i]:>10} {proba[i]:>9.1%}")

print(f"\\nAccuracy: {accuracy_score(y_test, preds):.1%}")""",
                "explanation": "predict_proba() is more useful than predict() for business decisions. You can rank applicants by approval probability, flag borderline cases for human review, or adjust the threshold based on risk tolerance."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "from sklearn.linear_model import LogisticRegression",
                    "model = LogisticRegression(max_iter=1000)",
                    "model.fit(X_train, y_train)",
                    "model.predict(X_test)  # returns 0 or 1",
                    "model.predict_proba(X_test)  # returns probabilities",
                    "proba[:, 1]  # probability of class 1"
                ],
                "notes": "Always set max_iter=1000 or higher — the default sometimes fails to converge on larger datasets. If you see a ConvergenceWarning, increase max_iter."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "model.predict_proba(X_test) returns [[0.3, 0.7], [0.8, 0.2]]. What is the predicted class for the first row (using default threshold 0.5)?",
                    "options": ["Class 0 (probability 0.3)", "Class 1 (probability 0.7)", "Cannot determine", "Class 0.7"],
                    "answer": 1,
                    "explanation": "The default threshold is 0.5. The first row has 70% probability for class 1, which exceeds 0.5, so it is classified as class 1."
                },
                {
                    "type": "true_false",
                    "question": "Logistic Regression can only classify data into exactly 2 categories.",
                    "answer": False,
                    "explanation": "Logistic Regression supports multi-class classification (more than 2 categories) using strategies like 'one-vs-rest'. However, binary classification (2 classes) is its most common use."
                },
                {
                    "type": "fill_blank",
                    "question": "To get probabilities instead of hard labels, use model.predict_proba(X_test)[:, ___] for the probability of class 1.",
                    "template": "churn_proba = model.predict_proba(X_test)[:, ___]",
                    "answer": "1",
                    "explanation": "predict_proba returns a 2-column array: column 0 = probability of class 0, column 1 = probability of class 1. Use [:, 1] to extract the positive class probability."
                }
            ],
            "challenge": {
                "instructions": "Build an email spam classifier. Data: num_links (number of links in email), has_promotion_word (1/0), sender_known (1/0), and spam (0 or 1). Fit a LogisticRegression. Print: (1) hard predictions on test set, (2) spam probability scores rounded to 2 decimal places, (3) overall accuracy. Then predict the probability for a new email with 5 links, has_promotion_word=1, sender_known=0.",
                "starter_code": "import pandas as pd\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\ndata = {\n    'num_links':          [0, 8, 1, 12, 0, 5, 2, 15, 0, 7, 1, 10],\n    'has_promo_word':     [0, 1, 0,  1, 0, 1, 0,  1, 0, 1, 0,  1],\n    'sender_known':       [1, 0, 1,  0, 1, 0, 1,  0, 1, 0, 1,  0],\n    'spam':               [0, 1, 0,  1, 0, 1, 0,  1, 0, 1, 0,  1]\n}\ndf = pd.DataFrame(data)\n\n# Create X and y\n\n# Split 80/20 random_state=42\n\n# Fit LogisticRegression (max_iter=1000)\n\n# Print hard predictions\n\n# Print spam probability scores\n\n# Print accuracy\n\n# Predict for new email: 5 links, promo=1, sender_known=0\n",
                "tests": [
                    {"type": "code_contains", "value": "LogisticRegression"},
                    {"type": "code_contains", "value": "predict_proba"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\ndata={'num_links':[0,8,1,12,0,5,2,15,0,7,1,10],'has_promo_word':[0,1,0,1,0,1,0,1,0,1,0,1],'sender_known':[1,0,1,0,1,0,1,0,1,0,1,0],'spam':[0,1,0,1,0,1,0,1,0,1,0,1]}\ndf=pd.DataFrame(data)\nX=df.drop('spam',axis=1)\ny=df['spam']\nX_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)\nmodel=LogisticRegression(max_iter=1000)\nmodel.fit(X_train,y_train)\npreds=model.predict(X_test)\nproba=model.predict_proba(X_test)[:,1]\nprint('Predictions:',preds)\nprint('Spam proba:',proba.round(2))\nprint(f'Accuracy: {accuracy_score(y_test,preds):.1%}')\nnew_email=[[5,1,0]]\nprint(f'New email spam probability: {model.predict_proba(new_email)[0,1]:.1%}')"
            },
            "challenge_variations": [
                "Variation 1: Predict customer churn (0/1) from tenure, monthly_charges, and num_support_calls. Print accuracy and churn probabilities.",
                "Variation 2: Classify loan default (0/1) from credit_score, income, and debt_to_income_ratio. Identify the 3 highest-risk applicants by probability.",
                "Variation 3: Predict employee attrition from years_at_company, satisfaction_score, and salary_growth. Use predict_proba to rank employees by risk.",
                "Variation 4: Classify job applications as interview/reject using gpa, years_exp, and skills_match_score. Set threshold at 0.6 instead of 0.5.",
                "Variation 5: Predict whether a marketing email leads to a click (0/1). Use 4 features. Print predictions and probabilities side by side.",
                "Variation 6: Build a medical screening model (disease/no_disease) from age, bmi, and blood_pressure. Print probabilities for 5 new patients.",
                "Variation 7: Classify product reviews as positive/negative using word_count, num_exclamations, and star_rating. Report accuracy.",
                "Variation 8: Predict whether a student passes (0/1) using attendance_pct, assignment_score, and midterm_score. Compare LogisticRegression to a simple rule.",
                "Variation 9: Create a fraud detection model from transaction_amount, is_international, and time_since_last_transaction. Print fraud probability for 5 transactions.",
                "Variation 10: Build a binary classifier and manually change the threshold from 0.5 to 0.3. Show how predictions change and discuss the business implication."
            ]
        },

        # ─────────────────────────────────────────────
        # LESSON 8
        # ─────────────────────────────────────────────
        {
            "id": "m4-l8",
            "title": "Evaluating Classification — Accuracy and Beyond",
            "order": 8,
            "duration_min": 20,
            "real_world_context": "A fraud detection model that flags NO transactions as fraud will have 99.9% accuracy — because 99.9% of transactions are legitimate. But it catches zero frauds. Accuracy alone can be dangerously misleading.",
            "concept": """**Why Accuracy Lies**

```python
# Medical test: does patient have rare disease? (1% of people do)
# Model that ALWAYS predicts "No Disease":
predictions = ["No Disease"] * 1000  # predict no disease for everyone
actual       = ["No Disease"] * 990 + ["Disease"] * 10

accuracy = 990 / 1000
print(f"Accuracy: {accuracy:.1%}")  # Accuracy: 99.0%
# But it never catches a single sick patient!
```

This is the **imbalanced dataset problem**. You need better metrics.

**The Four Metrics That Matter**

**Precision** — "When I say 'Yes', how often am I right?"
> Of all the times I predicted fraud, what fraction were actually fraud?
```python
from sklearn.metrics import precision_score
precision = precision_score(y_test, preds)
# 0.80 → 80% of flagged fraud cases were really fraud
# (20% were false alarms — annoyed innocent customers)
```

**Recall (Sensitivity)** — "Of all actual positives, how many did I catch?"
> Of all actual frauds, what fraction did I detect?
```python
from sklearn.metrics import recall_score
recall = recall_score(y_test, preds)
# 0.70 → caught 70% of real frauds
# (30% of frauds slipped through — that's expensive!)
```

**F1 Score** — The harmonic mean of precision and recall
> Balances both precision and recall into a single number
```python
from sklearn.metrics import f1_score
f1 = f1_score(y_test, preds)
# 0.75 → balanced performance score
```

**When to Use Which Metric:**

| Scenario | Priority Metric | Reason |
|---|---|---|
| Cancer screening | Recall | Missing a case is catastrophic |
| Spam filter | Precision | False positives (legit mail flagged) annoy users |
| Fraud detection | F1 or Recall | Missing fraud is expensive |
| General use | Accuracy | When classes are balanced |

**All Metrics Together:**
```python
from sklearn.metrics import classification_report

print(classification_report(y_test, preds, target_names=["Not Churn", "Churn"]))
```
Output:
```
              precision    recall  f1-score   support
   Not Churn       0.88      0.93      0.90        54
       Churn       0.82      0.72      0.77        25
    accuracy                           0.86        79
   macro avg       0.85      0.83      0.84        79
weighted avg       0.86      0.86      0.86        79
```

**Imbalanced Datasets — Quick Fixes:**
```python
# Option 1: class_weight='balanced' — tells model to care more about rare class
model = LogisticRegression(class_weight='balanced', max_iter=1000)

# Option 2: Change the classification threshold
proba = model.predict_proba(X_test)[:, 1]
preds_custom = (proba >= 0.3).astype(int)  # lower threshold → catch more positives
```""",
            "worked_example": {
                "description": "Comparing accuracy to precision/recall/F1 on a customer churn dataset where accuracy misleads.",
                "code": """import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score,
                              recall_score, f1_score, classification_report)

np.random.seed(0)
n = 200
# Imbalanced: only 20% churn (realistic)
X = pd.DataFrame({
    "tenure":   np.random.randint(1, 60, n),
    "charges":  np.random.uniform(20, 100, n),
    "tickets":  np.random.randint(0, 10, n)
})
y = (np.random.rand(n) < 0.2).astype(int)  # 20% churn

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Model A: predicts "no churn" for everyone (naive baseline)
naive_preds = np.zeros(len(y_test), dtype=int)

# Model B: actual logistic regression
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)
lr_preds = model.predict(X_test)

print("=" * 45)
print(f"{'Metric':<15} {'Naive':>10} {'LogReg':>10}")
print("=" * 45)
print(f"{'Accuracy':<15} {accuracy_score(y_test,naive_preds):>10.1%} {accuracy_score(y_test,lr_preds):>10.1%}")
print(f"{'Precision':<15} {precision_score(y_test,naive_preds,zero_division=0):>10.1%} {precision_score(y_test,lr_preds,zero_division=0):>10.1%}")
print(f"{'Recall':<15} {recall_score(y_test,naive_preds):>10.1%} {recall_score(y_test,lr_preds):>10.1%}")
print(f"{'F1 Score':<15} {f1_score(y_test,naive_preds):>10.1%} {f1_score(y_test,lr_preds):>10.1%}")
# Naive gets ~80% accuracy but 0% recall!
# LogReg gets lower accuracy but actually catches churners""",
                "explanation": "The naive model 'wins' on accuracy but is completely useless. Recall = 0% means it never catches a single churner. The logistic regression has lower accuracy but meaningful recall — it's the useful model."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score",
                    "from sklearn.metrics import classification_report",
                    "print(classification_report(y_test, preds))",
                    "LogisticRegression(class_weight='balanced')  # for imbalanced data",
                    "precision_score(y_test, preds, zero_division=0)"
                ],
                "notes": "In business: always ask 'what is the cost of a false positive vs. false negative?' before choosing your primary metric."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A cancer screening test has 95% precision and 40% recall. What does the recall tell us?",
                    "options": [
                        "95% of healthy patients are correctly cleared",
                        "Only 40% of actual cancer cases are detected",
                        "The model is 40% accurate overall",
                        "40% of positive predictions are wrong"
                    ],
                    "answer": 1,
                    "explanation": "Recall = of all actual positive cases (real cancer), what fraction did the model catch? 40% recall means 60% of cancer patients are missed — dangerous in medical screening."
                },
                {
                    "type": "true_false",
                    "question": "High accuracy always means a classification model is performing well.",
                    "answer": False,
                    "explanation": "On imbalanced datasets (e.g., 99% of data is class 0), predicting class 0 for everything gives 99% accuracy but is completely useless. Always check precision, recall, and F1 for imbalanced classes."
                },
                {
                    "type": "fill_blank",
                    "question": "To print a full classification report with precision, recall, and F1, use: print(classification_report(y_test, ___))",
                    "template": "print(classification_report(y_test, ___))",
                    "answer": "preds",
                    "explanation": "classification_report() takes the true labels and predicted labels, then prints precision, recall, F1, and support for every class."
                }
            ],
            "challenge": {
                "instructions": "Build a fraud detection classifier. The dataset is imbalanced — only 15% of transactions are fraud. Use LogisticRegression(class_weight='balanced'). Print: accuracy, precision, recall, F1. Then print the full classification_report. Finally, answer this question with a print statement: 'For fraud detection, which metric matters most and why?'",
                "starter_code": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import (accuracy_score, precision_score,\n                              recall_score, f1_score, classification_report)\n\nnp.random.seed(1)\nn = 300\nX = pd.DataFrame({\n    'amount':        np.random.uniform(10, 5000, n),\n    'is_foreign':    np.random.randint(0, 2, n),\n    'time_of_day':   np.random.randint(0, 24, n)\n})\ny = (np.random.rand(n) < 0.15).astype(int)  # 15% fraud\n\n# Split with stratify=y\n\n# Fit LogisticRegression(class_weight='balanced', max_iter=1000)\n\n# Print all 4 metrics\n\n# Print classification_report\n\n# Print which metric matters most for fraud\n",
                "tests": [
                    {"type": "code_contains", "value": "classification_report"},
                    {"type": "code_contains", "value": "recall_score"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,classification_report\nnp.random.seed(1)\nn=300\nX=pd.DataFrame({'amount':np.random.uniform(10,5000,n),'is_foreign':np.random.randint(0,2,n),'time_of_day':np.random.randint(0,24,n)})\ny=(np.random.rand(n)<0.15).astype(int)\nX_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)\nmodel=LogisticRegression(class_weight='balanced',max_iter=1000)\nmodel.fit(X_train,y_train)\npreds=model.predict(X_test)\nprint(f'Accuracy: {accuracy_score(y_test,preds):.1%}')\nprint(f'Precision: {precision_score(y_test,preds):.1%}')\nprint(f'Recall: {recall_score(y_test,preds):.1%}')\nprint(f'F1: {f1_score(y_test,preds):.1%}')\nprint(classification_report(y_test,preds,target_names=['Legit','Fraud']))\nprint('For fraud: recall matters most — missing real fraud is far more costly than false alarms.')"
            },
            "challenge_variations": [
                "Variation 1: Build a spam classifier. Argue whether precision or recall is more important for spam filtering vs. fraud detection.",
                "Variation 2: Compare classification_report between LogisticRegression and a naive 'always predict 0' model. Show which metrics expose the naive model.",
                "Variation 3: Predict employee attrition (10% leave). Compare accuracy vs. F1 on this imbalanced target.",
                "Variation 4: Train two models — one without class_weight and one with class_weight='balanced'. Compare their recall scores.",
                "Variation 5: For a disease screening model, lower the classification threshold to 0.3. How does recall change? How does precision change?",
                "Variation 6: Create a 3-class problem (low/medium/high priority ticket). Print classification_report and explain the 'macro avg' row.",
                "Variation 7: Compute precision and recall manually (without sklearn) using counts of TP, FP, FN from y_test and predictions.",
                "Variation 8: What F1 score would a model achieve if it had 90% precision but 10% recall? Calculate it.",
                "Variation 9: Build a churn model. Write a business memo (as print statements) explaining the model's precision and recall to a non-technical VP.",
                "Variation 10: Find the threshold value (between 0 and 1) that maximizes F1 score for a logistic regression model by testing thresholds [0.3, 0.4, 0.5, 0.6, 0.7]."
            ]
        },
        {
            "id": "m4-l9",
            "title": "Confusion Matrix — Seeing Exactly Where Your Model Fails",
            "subtitle": "Break down predictions into TP, FP, TN, FN",
            "difficulty": "intermediate",
            "business_context": "Your classifier says 95% accuracy, but is it catching actual fraud cases? A confusion matrix shows exactly which types of errors you're making — false positives (flagging innocent transactions) vs. false negatives (missing real fraud).",
            "concept": {
                "theory": "A confusion matrix is a 2x2 table (for binary classification) showing: True Positives (predicted positive, actually positive), True Negatives (predicted negative, actually negative), False Positives (predicted positive, actually negative), False Negatives (predicted negative, actually positive). All metrics — accuracy, precision, recall, F1 — derive from these four numbers.",
                "business_angle": "The cost of FP vs FN differs by domain: in fraud detection, FN (missing fraud) is catastrophic; in spam filtering, FP (blocking legitimate email) is worse. Visualizing the confusion matrix makes the error tradeoff tangible for stakeholders.",
                "worked_example_intro": "We'll build a classifier, print the confusion matrix, and manually compute all metrics from the raw TP/FP/TN/FN counts.",
                "key_insight": "Always look at the confusion matrix, not just accuracy. A model that predicts 'not fraud' for every transaction gets 99% accuracy on an imbalanced dataset — but has a perfect confusion matrix column of false negatives."
            },
            "worked_example": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib
matplotlib.use('Agg')

np.random.seed(42)
n = 400
X = np.column_stack([np.random.randn(n), np.random.randn(n)])
y = (X[:,0] + X[:,1] > 0.5).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)

cm = confusion_matrix(y_test, preds)
print("Confusion Matrix:")
print(cm)
print()

tn, fp, fn, tp = cm.ravel()
print(f"True Negatives  (TN): {tn}  — correctly predicted negative")
print(f"False Positives (FP): {fp}  — predicted positive, actually negative")
print(f"False Negatives (FN): {fn}  — predicted negative, actually positive")
print(f"True Positives  (TP): {tp}  — correctly predicted positive")
print()
print(f"Accuracy  = (TP+TN)/(all)       = {(tp+tn)/(tp+tn+fp+fn):.1%}")
print(f"Precision = TP/(TP+FP)           = {tp/(tp+fp):.1%}")
print(f"Recall    = TP/(TP+FN)           = {tp/(tp+fn):.1%}")
print(f"F1        = 2*P*R/(P+R)          = {2*tp/(2*tp+fp+fn):.1%}")
print(f"Specificity = TN/(TN+FP)         = {tn/(tn+fp):.1%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "from sklearn.metrics import confusion_matrix",
                        "cm = confusion_matrix(y_test, preds)",
                        "tn, fp, fn, tp = cm.ravel()  -- unpack 2x2 matrix",
                        "cm[0][0]=TN, cm[0][1]=FP, cm[1][0]=FN, cm[1][1]=TP"
                    ],
                    "notes": "sklearn's confusion_matrix uses rows=actual, columns=predicted. cm[1][1] is always TP for the positive class."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "A spam filter has 90 TP, 10 FP, 5 FN, 895 TN. What is the precision?", "options": ["90/95 = 94.7%","90/100 = 90%","90/895 = 10%","90/1000 = 9%"], "answer": 0, "explanation": "Precision = TP/(TP+FP) = 90/(90+10) = 90/100 = 90%. Wait — actually 90/(90+10) = 90%. But the option says 90/95. Let me recalculate: TP=90, FP=10, so TP+FP=100, precision=90/100=90%. The answer should be B. Precision = TP/(TP+FP) = 90/(90+10) = 90%."},
                    {"type": "true_false", "question": "A model with 0 False Negatives has perfect recall.", "answer": True, "explanation": "Recall = TP/(TP+FN). If FN=0, recall = TP/TP = 100%. The model catches every actual positive case — none slip through as false negatives."},
                    {"type": "fill_blank", "question": "To unpack a 2x2 confusion matrix: tn, fp, fn, tp = cm.___", "template": "tn, fp, fn, tp = cm.___", "answer": "ravel()", "explanation": "cm.ravel() flattens the 2x2 matrix to a 1D array [TN, FP, FN, TP] in row-major order. This is the standard pattern for unpacking sklearn's confusion matrix."}
                ]
            },
            "challenge": {
                "instructions": "Build a disease screening model on imbalanced data (10% positive). Print the confusion matrix, manually compute all 5 metrics (accuracy, precision, recall, F1, specificity). Then compare with a 'predict always negative' baseline — show why accuracy alone is misleading.",
                "starter_code": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

np.random.seed(1)
n = 1000
X = np.column_stack([np.random.randn(n), np.random.randn(n)])
y = (np.random.rand(n) < 0.10).astype(int)  # 10% positive (disease cases)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model with class_weight='balanced'

# Print confusion matrix

# Compute TP, FP, FN, TN and print all 5 metrics

# Compare: what accuracy does a 'predict all negative' baseline get?
print("\\n=== Baseline (always predict 0) ===")
# Print its confusion matrix and accuracy
""",
                "tests": [{"type": "code_contains", "value": "confusion_matrix"}, {"type": "code_contains", "value": "ravel"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
np.random.seed(1)
n=1000
X=np.column_stack([np.random.randn(n),np.random.randn(n)])
y=(np.random.rand(n)<0.10).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
model=LogisticRegression(class_weight='balanced',max_iter=1000)
model.fit(X_train,y_train); preds=model.predict(X_test)
cm=confusion_matrix(y_test,preds)
print("Model CM:"); print(cm)
tn,fp,fn,tp=cm.ravel()
print(f"Accuracy:{(tp+tn)/(tp+tn+fp+fn):.1%} Precision:{tp/(tp+fp+1e-9):.1%} Recall:{tp/(tp+fn+1e-9):.1%} F1:{2*tp/(2*tp+fp+fn+1e-9):.1%} Spec:{tn/(tn+fp+1e-9):.1%}")
print("\\n=== Baseline ===")
base=np.zeros(len(y_test),dtype=int)
cm2=confusion_matrix(y_test,base); print(cm2)
print(f"Baseline accuracy: {(y_test==base).mean():.1%} (misleadingly high!)")""",
                "challenge_variations": [
                    "Plot the confusion matrix using ConfusionMatrixDisplay.from_predictions().",
                    "Build a 3-class confusion matrix (low/medium/high risk) and interpret the off-diagonal cells.",
                    "Show how lowering the classification threshold changes TP/FP/TN/FN counts.",
                    "Calculate Matthews Correlation Coefficient from TP/FP/TN/FN manually.",
                    "Build a 'confusion matrix tracker' that shows how the matrix changes as you add more training data.",
                    "Compare confusion matrices of 3 different models on the same dataset side by side.",
                    "Calculate the cost of errors: each FN costs $500, each FP costs $50. Which threshold minimizes total cost?",
                    "Build a multi-class confusion matrix for digit classification and identify which digits get confused most.",
                    "Normalize the confusion matrix by rows (recall per class) and by columns (precision per class).",
                    "Extract the confusion matrix from a RandomForest with cross-validation using cross_val_predict."
                ]
            }
        },
        {
            "id": "m4-l10",
            "title": "Decision Trees — Rules Your Manager Can Actually Read",
            "subtitle": "Build flowchart models that explain every prediction",
            "difficulty": "intermediate",
            "business_context": "Your boss asks why the model denied a loan application. A neural network says 'I don't know.' A decision tree says 'Because income < $45,000 AND debt ratio > 0.4.' Decision trees are the gold standard for explainable AI.",
            "concept": {
                "theory": "A decision tree splits data at each node using the feature and threshold that best separates the classes. It picks splits by minimizing impurity — Gini impurity (default in sklearn) or entropy. At each split, it asks: 'which single rule reduces uncertainty the most?' It keeps splitting until it hits max_depth or a minimum sample threshold.",
                "business_angle": "Decision trees excel in regulated industries (banking, healthcare, insurance) where you must explain every decision. The tree's if-then rules can be read aloud: 'If income > $60k AND credit score > 650, approve.' They're also excellent for discovering which features matter most.",
                "worked_example_intro": "We'll train a decision tree to predict customer churn, print the decision rules, and visualize feature importance.",
                "key_insight": "Depth controls complexity. max_depth=2 gives you a simple, readable tree. max_depth=None gives a tree that memorizes training data (overfitting). Always tune max_depth with cross-validation."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 600
df = pd.DataFrame({
    'tenure_months': np.random.randint(1, 60, n),
    'monthly_charge': np.random.uniform(20, 120, n),
    'support_calls': np.random.randint(0, 10, n),
    'contract_type': np.random.choice([0,1,2], n),  # 0=month, 1=1yr, 2=2yr
})
df['churn'] = ((df['support_calls'] > 4) |
               ((df['monthly_charge'] > 80) & (df['contract_type'] == 0)) |
               (df['tenure_months'] < 6)).astype(int)

X = df.drop('churn', axis=1)
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Simple interpretable tree
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
preds = tree.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, preds):.1%}")
print(f"\\nDecision Rules:")
print(export_text(tree, feature_names=list(X.columns)))

print("Feature Importances:")
for feat, imp in sorted(zip(X.columns, tree.feature_importances_), key=lambda x: -x[1]):
    bar = '█' * int(imp * 30)
    print(f"  {feat:<18} {imp:.3f} {bar}")

# Compare depths
for depth in [1, 2, 3, 5, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=42)
    t.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, t.predict(X_train))
    test_acc  = accuracy_score(y_test,  t.predict(X_test))
    print(f"  depth={str(depth):<5} train={train_acc:.1%}  test={test_acc:.1%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "DecisionTreeClassifier(max_depth=3, random_state=42)",
                        "tree.fit(X_train, y_train)",
                        "export_text(tree, feature_names=['col1','col2'])",
                        "tree.feature_importances_  -- array of importance per feature",
                        "DecisionTreeRegressor  -- for continuous targets"
                    ],
                    "notes": "max_depth is the most important hyperparameter. Start with 3-5 for interpretability. Use cross-validation to find the optimal depth."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "What does max_depth=None mean in a DecisionTreeClassifier?", "options": ["The tree has no splits","The tree grows until all leaves are pure or have min_samples_leaf samples","Depth is limited to 10 by default","The tree uses entropy instead of Gini"], "answer": 1, "explanation": "max_depth=None means no depth limit — the tree grows until every leaf is pure (perfect training accuracy) or hits min_samples_split/min_samples_leaf. This almost always overfits. Set max_depth=3-5 for generalizable trees."},
                    {"type": "true_false", "question": "Decision trees can only be used for classification, not regression.", "answer": False, "explanation": "sklearn has both DecisionTreeClassifier (predicts classes) and DecisionTreeRegressor (predicts continuous values). The algorithm is the same — the difference is in how leaf node predictions are computed (majority class vs. mean value)."},
                    {"type": "fill_blank", "question": "Print a text representation of tree rules: print(___(tree, feature_names=cols))", "template": "print(___(tree, feature_names=cols))", "answer": "export_text", "explanation": "export_text() from sklearn.tree renders the decision tree as readable if-then rules in text format. Great for explaining the model to stakeholders who can't read code."}
                ]
            },
            "challenge": {
                "instructions": "Build a loan approval decision tree. The dataset has income, credit_score, debt_ratio, employment_years. Train a tree with max_depth=4. Print: accuracy, the decision rules, and feature importances. Then compare train vs test accuracy at depths 2, 4, 6, 10 to show overfitting behavior.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(7)
n = 800
df = pd.DataFrame({
    'income':           np.random.uniform(20000, 150000, n),
    'credit_score':     np.random.randint(450, 850, n),
    'debt_ratio':       np.random.uniform(0.1, 0.9, n),
    'employment_years': np.random.randint(0, 20, n),
})
df['approved'] = ((df['credit_score'] > 650) &
                  (df['debt_ratio'] < 0.4) &
                  (df['income'] > 40000)).astype(int)

X = df.drop('approved', axis=1)
y = df['approved']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train tree with max_depth=4

# Print accuracy, rules, feature importances

print("\\n=== Overfitting Analysis ===")
# Compare train vs test accuracy at depths 2, 4, 6, 10
""",
                "tests": [{"type": "code_contains", "value": "DecisionTreeClassifier"}, {"type": "code_contains", "value": "export_text"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
np.random.seed(7)
n=800
df=pd.DataFrame({'income':np.random.uniform(20000,150000,n),'credit_score':np.random.randint(450,850,n),'debt_ratio':np.random.uniform(0.1,0.9,n),'employment_years':np.random.randint(0,20,n)})
df['approved']=((df['credit_score']>650)&(df['debt_ratio']<0.4)&(df['income']>40000)).astype(int)
X=df.drop('approved',axis=1); y=df['approved']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
tree=DecisionTreeClassifier(max_depth=4,random_state=42)
tree.fit(X_train,y_train)
print(f"Accuracy: {accuracy_score(y_test,tree.predict(X_test)):.1%}")
print(export_text(tree,feature_names=list(X.columns)))
for f,i in sorted(zip(X.columns,tree.feature_importances_),key=lambda x:-x[1]):
    print(f"  {f:<20} {i:.3f}")
print("\\n=== Overfitting Analysis ===")
for d in [2,4,6,10]:
    t=DecisionTreeClassifier(max_depth=d,random_state=42);t.fit(X_train,y_train)
    print(f"  depth={d:>2}  train={accuracy_score(y_train,t.predict(X_train)):.1%}  test={accuracy_score(y_test,t.predict(X_test)):.1%}")""",
                "challenge_variations": [
                    "Use DecisionTreeRegressor to predict house prices and compare RMSE at different max_depth values.",
                    "Visualize the tree using sklearn.tree.plot_tree() and save to PNG.",
                    "Add min_samples_leaf=20 and compare overfitting to the default.",
                    "Extract specific rules as Python if-statements from a trained tree.",
                    "Build a tree on the Iris dataset and print which flower species each branch leads to.",
                    "Use cross_val_score to find the optimal max_depth with 5-fold CV.",
                    "Train a tree on text data (TF-IDF features) for document classification.",
                    "Build a cost-sensitive tree: set class_weight to penalize FN 5x more than FP.",
                    "Compare Gini vs entropy criterion on the same dataset — how different are the results?",
                    "Implement a simple decision stump (max_depth=1) and explain when it's actually useful."
                ]
            }
        },
        {
            "id": "m4-l11",
            "title": "Random Forests — Wisdom of the Crowd for ML",
            "subtitle": "Hundreds of diverse trees vote together for more accurate, robust predictions",
            "difficulty": "intermediate",
            "business_context": "A single decision tree is like asking one analyst for an opinion — fast but risky. A random forest is like polling 100 analysts independently, each seeing different data. Their collective vote is almost always better than any individual.",
            "concept": {
                "theory": "Random forests build many decision trees, each trained on a random bootstrap sample of the data with a random subset of features at each split. Predictions are made by majority vote (classification) or averaging (regression). This ensemble approach dramatically reduces overfitting compared to a single tree.",
                "business_angle": "Random forests are the workhorse of industry ML: they handle missing data well, require minimal preprocessing, provide feature importance rankings, and are hard to overfit. They're often the first model to try after logistic regression.",
                "worked_example_intro": "We'll compare a single decision tree vs random forest on the same dataset — showing accuracy and variance improvements.",
                "key_insight": "Two key hyperparameters: n_estimators (more trees = better, diminishing returns after ~200) and max_features (number of features to consider at each split — 'sqrt' of total features is the default and usually best)."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'age':        np.random.randint(18, 70, n),
    'income':     np.random.uniform(20000, 120000, n),
    'credit':     np.random.randint(450, 850, n),
    'debt_ratio': np.random.uniform(0.1, 0.8, n),
    'missed_payments': np.random.randint(0, 5, n),
})
df['default'] = ((df['credit'] < 600) | (df['missed_payments'] > 2) |
                 ((df['debt_ratio'] > 0.6) & (df['income'] < 40000))).astype(int)

X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Single tree vs Random Forest
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
rf   = RandomForestClassifier(n_estimators=100, random_state=42)

tree.fit(X_train, y_train)
rf.fit(X_train, y_train)

print(f"Decision Tree  — test: {accuracy_score(y_test, tree.predict(X_test)):.1%}")
print(f"Random Forest  — test: {accuracy_score(y_test, rf.predict(X_test)):.1%}")

# Cross-validation (5-fold) shows variance
tree_cv = cross_val_score(tree, X, y, cv=5)
rf_cv   = cross_val_score(rf,   X, y, cv=5)
print(f"\\nTree  CV: {tree_cv.mean():.1%} ± {tree_cv.std():.1%}")
print(f"Forest CV: {rf_cv.mean():.1%} ± {rf_cv.std():.1%}")

# Feature importance
print("\\nFeature Importances (RF):")
for feat, imp in sorted(zip(X.columns, rf.feature_importances_), key=lambda x: -x[1]):
    bar = '█' * int(imp * 40)
    print(f"  {feat:<18} {imp:.3f} {bar}")

# Effect of n_estimators
print("\\nAccuracy vs n_estimators:")
for n_est in [10, 50, 100, 200]:
    rf_n = RandomForestClassifier(n_estimators=n_est, random_state=42)
    rf_n.fit(X_train, y_train)
    print(f"  n={n_est:<4}: {accuracy_score(y_test, rf_n.predict(X_test)):.1%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "RandomForestClassifier(n_estimators=100, random_state=42)",
                        "RandomForestRegressor(n_estimators=100)",
                        "rf.feature_importances_  -- mean decrease in impurity per feature",
                        "rf.n_estimators  -- number of trees"
                    ],
                    "notes": "n_estimators=100 is a safe default. More trees never hurt accuracy (only speed). Set random_state for reproducibility."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why do random forests outperform single decision trees?", "options": ["They use deeper trees","They use gradient boosting","Diverse trees trained on different data subsets reduce variance when averaged","They preprocess features better"], "answer": 2, "explanation": "Each tree is trained on a bootstrapped sample with random feature subsets, making each tree different. Their errors are uncorrelated, so averaging them cancels out individual errors — reducing variance without increasing bias. This is the bias-variance tradeoff in action."},
                    {"type": "true_false", "question": "Adding more trees (n_estimators) to a random forest can cause overfitting.", "answer": False, "explanation": "Unlike increasing tree depth, adding more trees to a forest does NOT cause overfitting. More trees only reduce variance and improve stability. The only cost is computational time. After ~200 trees, accuracy improvements become negligible."},
                    {"type": "fill_blank", "question": "Get feature importance from a trained random forest: importances = rf.___", "template": "importances = rf.___", "answer": "feature_importances_", "explanation": "feature_importances_ is an array of the same length as the number of features. Each value is the mean decrease in Gini impurity from that feature across all trees, normalized to sum to 1."}
                ]
            },
            "challenge": {
                "instructions": "Build a random forest for employee attrition prediction. Compare with a single decision tree. Print: both accuracies, CV scores, and feature importances. Identify the top 2 predictors of attrition.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

np.random.seed(99)
n = 1200
df = pd.DataFrame({
    'years_at_company':   np.random.randint(0, 20, n),
    'monthly_salary':     np.random.uniform(2000, 12000, n),
    'overtime_hours':     np.random.randint(0, 20, n),
    'manager_rating':     np.random.randint(1, 6, n),
    'promotions_5yr':     np.random.randint(0, 4, n),
    'distance_from_home': np.random.randint(1, 50, n),
})
df['attrition'] = ((df['overtime_hours'] > 10) |
                   ((df['manager_rating'] < 3) & (df['years_at_company'] < 3)) |
                   (df['promotions_5yr'] == 0) & (df['years_at_company'] > 10)).astype(int)

X = df.drop('attrition', axis=1)
y = df['attrition']

# Split data

# Train both models

# Print comparison

# Print feature importances

""",
                "tests": [{"type": "code_contains", "value": "RandomForestClassifier"}, {"type": "code_contains", "value": "feature_importances_"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
np.random.seed(99)
n=1200
df=pd.DataFrame({'years_at_company':np.random.randint(0,20,n),'monthly_salary':np.random.uniform(2000,12000,n),'overtime_hours':np.random.randint(0,20,n),'manager_rating':np.random.randint(1,6,n),'promotions_5yr':np.random.randint(0,4,n),'distance_from_home':np.random.randint(1,50,n)})
df['attrition']=((df['overtime_hours']>10)|((df['manager_rating']<3)&(df['years_at_company']<3))|(df['promotions_5yr']==0)&(df['years_at_company']>10)).astype(int)
X=df.drop('attrition',axis=1); y=df['attrition']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
tree=DecisionTreeClassifier(max_depth=5,random_state=42); tree.fit(X_train,y_train)
rf=RandomForestClassifier(n_estimators=100,random_state=42); rf.fit(X_train,y_train)
print(f"Tree  test acc: {accuracy_score(y_test,tree.predict(X_test)):.1%}")
print(f"RF    test acc: {accuracy_score(y_test,rf.predict(X_test)):.1%}")
print(f"Tree  CV: {cross_val_score(tree,X,y,cv=5).mean():.1%}")
print(f"RF    CV: {cross_val_score(rf,X,y,cv=5).mean():.1%}")
print("\\nFeature Importances:")
for f,i in sorted(zip(X.columns,rf.feature_importances_),key=lambda x:-x[1]):
    print(f"  {f:<22} {i:.3f}")""",
                "challenge_variations": [
                    "Use RandomForestRegressor to predict salary and report RMSE and R² score.",
                    "Extract one tree from a forest using rf.estimators_[0] and visualize it.",
                    "Use permutation_importance for a more reliable feature importance estimate.",
                    "Compare RandomForest vs GradientBoostingClassifier on the same dataset.",
                    "Use OOB (out-of-bag) score: RandomForestClassifier(oob_score=True) — explain what it measures.",
                    "Tune n_estimators and max_features together using GridSearchCV.",
                    "Build a forest where each tree votes with different weights based on its OOB accuracy.",
                    "Plot learning curves: accuracy vs. training set size for forest vs single tree.",
                    "Use RandomForest for multi-class classification (3+ classes) and print per-class importances.",
                    "Implement a 'forest insight' report: for each top feature, show the threshold value where most trees split."
                ]
            }
        },
        {
            "id": "m4-l12",
            "title": "K-Nearest Neighbors — 'Show Me Your Friends'",
            "subtitle": "Classify by majority vote of the k most similar training examples",
            "difficulty": "intermediate",
            "business_context": "Netflix's early recommendation engine was pure KNN: 'find the 10 users most similar to you, recommend what they liked.' KNN requires no training phase — it memorizes all data and makes predictions by proximity at query time.",
            "concept": {
                "theory": "KNN classifies a new point by finding the k nearest training points (by Euclidean distance, usually) and taking a majority vote. For regression, it averages those k neighbors. KNN is a lazy learner: no model is built during training — prediction requires scanning all training data. This makes prediction slow for large datasets but training instant.",
                "business_angle": "KNN is intuitive for stakeholders ('we recommend based on similar customers') and excellent for recommendation systems, anomaly detection, and small-to-medium datasets. Its main weakness: slow prediction on large data and sensitive to irrelevant features.",
                "worked_example_intro": "We'll classify customers by risk segment using KNN, experiment with different k values, and see the impact of feature scaling.",
                "key_insight": "KNN is extremely sensitive to feature scale. If income ranges from $20k-$200k and age ranges from 18-70, income dominates the distance calculation. ALWAYS scale features before KNN with StandardScaler or MinMaxScaler."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
X = pd.DataFrame({
    'credit_score': np.random.randint(450, 850, n),
    'income':       np.random.uniform(20000, 150000, n),
    'age':          np.random.randint(18, 70, n),
    'debt_ratio':   np.random.uniform(0.1, 0.8, n),
})
y = ((X['credit_score'] > 650) & (X['debt_ratio'] < 0.4)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# WITHOUT scaling (bad for KNN)
knn_raw = KNeighborsClassifier(n_neighbors=5)
knn_raw.fit(X_train, y_train)
print(f"KNN without scaling: {accuracy_score(y_test, knn_raw.predict(X_test)):.1%}")

# WITH scaling (proper approach)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
print(f"KNN with scaling:    {accuracy_score(y_test, knn.predict(X_test_scaled)):.1%}")

# Find optimal k
print("\\nAccuracy by k value:")
for k in [1, 3, 5, 10, 20, 50]:
    knn_k = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn_k, X_train_scaled, y_train, cv=5).mean()
    print(f"  k={k:<4}: {score:.1%}")

# Predict a new customer
new_customer = scaler.transform([[720, 85000, 35, 0.3]])
print(f"\\nNew customer prediction: {'Low Risk' if knn.predict(new_customer)[0] == 1 else 'High Risk'}")
proba = knn.predict_proba(new_customer)[0]
print(f"Confidence: {proba.max():.0%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "KNeighborsClassifier(n_neighbors=5)",
                        "KNeighborsRegressor(n_neighbors=5)",
                        "scaler = StandardScaler(); X_scaled = scaler.fit_transform(X_train)",
                        "knn.predict_proba(X)  -- probability estimates"
                    ],
                    "notes": "Always scale before KNN. Use cross_val_score to find best k. Odd k avoids ties in binary classification."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why must you scale features before using KNN?", "options": ["KNN only works with normalized data","Features with large ranges dominate the distance metric","Scaling makes training faster","KNN requires feature values between 0 and 1"], "answer": 1, "explanation": "KNN computes Euclidean distance. A feature with range 0-100,000 contributes much more to distance than a feature with range 0-1, effectively ignoring the smaller-range feature. StandardScaler makes all features contribute equally."},
                    {"type": "true_false", "question": "A very small k (e.g., k=1) in KNN tends to overfit to training data.", "answer": True, "explanation": "k=1 means 'predict based on the single nearest neighbor.' This memorizes training data perfectly (0% training error) but is extremely sensitive to noise. Large k smooths predictions but can underfit. Typically k=5 or k=7 is a good starting point."},
                    {"type": "fill_blank", "question": "To get class probability estimates from KNN: proba = knn.___(X_test)", "template": "proba = knn.___(X_test)", "answer": "predict_proba", "explanation": "predict_proba() returns the fraction of k neighbors belonging to each class. For k=5, if 4 neighbors are class 1 and 1 is class 0, predict_proba returns [0.2, 0.8]. This is a simple but valid confidence estimate."}
                ]
            },
            "challenge": {
                "instructions": "Build a KNN classifier for product recommendation (will a customer buy category X?). Compare accuracy with and without scaling. Find the optimal k using cross-validation. Print the confusion matrix and a prediction with confidence for a new customer.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

np.random.seed(5)
n = 1000
X = pd.DataFrame({
    'age':            np.random.randint(18, 70, n),
    'avg_order_value': np.random.uniform(20, 500, n),
    'visits_per_month': np.random.randint(1, 30, n),
    'days_since_last': np.random.randint(1, 365, n),
})
y = ((X['avg_order_value'] > 200) & (X['visits_per_month'] > 10)).astype(int)

# Split, scale, train KNN

# Compare unscaled vs scaled

# Find best k (k=1,3,5,10,15,20) with 5-fold CV

# Predict new customer: age=30, avg_order=250, visits=15, days_since=10
""",
                "tests": [{"type": "code_contains", "value": "KNeighborsClassifier"}, {"type": "code_contains", "value": "StandardScaler"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
np.random.seed(5)
n=1000
X=pd.DataFrame({'age':np.random.randint(18,70,n),'avg_order_value':np.random.uniform(20,500,n),'visits_per_month':np.random.randint(1,30,n),'days_since_last':np.random.randint(1,365,n)})
y=((X['avg_order_value']>200)&(X['visits_per_month']>10)).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
scaler=StandardScaler()
Xs_train=scaler.fit_transform(X_train); Xs_test=scaler.transform(X_test)
knn_raw=KNeighborsClassifier(5); knn_raw.fit(X_train,y_train)
knn=KNeighborsClassifier(5); knn.fit(Xs_train,y_train)
print(f"Unscaled: {accuracy_score(y_test,knn_raw.predict(X_test)):.1%}")
print(f"Scaled:   {accuracy_score(y_test,knn.predict(Xs_test)):.1%}")
print("Best k:"); best_k,best_s=5,0
for k in [1,3,5,10,15,20]:
    s=cross_val_score(KNeighborsClassifier(k),Xs_train,y_train,cv=5).mean()
    if s>best_s: best_k,best_s=k,s
    print(f"  k={k}: {s:.1%}")
knn_best=KNeighborsClassifier(best_k); knn_best.fit(Xs_train,y_train)
new=scaler.transform([[30,250,15,10]])
print(f"New customer: {'Will Buy' if knn_best.predict(new)[0] else 'Will Not Buy'} ({knn_best.predict_proba(new)[0].max():.0%} conf)")""",
                "challenge_variations": [
                    "Use KNeighborsRegressor to predict customer lifetime value.",
                    "Implement KNN with different distance metrics: 'euclidean', 'manhattan', 'chebyshev'.",
                    "Build a KNN-based anomaly detector: flag points whose k-NN distance is more than 2 std devs above mean.",
                    "Use weights='distance' in KNN (closer neighbors vote more) — compare with uniform weights.",
                    "Build a KNN recommendation system: for a user, find 5 most similar users and recommend items they liked.",
                    "Implement KNN from scratch using only NumPy (compute distances, sort, take k nearest).",
                    "Compare KNN to LogisticRegression and RandomForest — when does KNN win?",
                    "Use MinMaxScaler instead of StandardScaler with KNN — compare results.",
                    "Plot decision boundaries for KNN with k=1, 5, 20 on a 2D dataset.",
                    "Build a face-match system using KNN on image feature vectors."
                ]
            }
        },
        {
            "id": "m4-l13",
            "title": "K-Means Clustering — Find the Natural Groups",
            "subtitle": "Unsupervised learning: discover hidden segments without labeled data",
            "difficulty": "intermediate",
            "business_context": "Marketing wants to segment 50,000 customers into groups for targeted campaigns — but there's no 'correct' answer to guide training. K-Means finds natural clusters without needing any labels. It's how companies discover their customer archetypes.",
            "concept": {
                "theory": "K-Means partitions data into k clusters by iterating: (1) assign each point to its nearest centroid, (2) move each centroid to the mean of its assigned points. Repeat until centroids stop moving. The result: k groups where points within a group are similar to each other and different from other groups.",
                "business_angle": "K-Means powers customer segmentation, document grouping, image compression, and anomaly detection. The key business skill: choosing k (the number of clusters) and interpreting what each cluster means in business terms.",
                "worked_example_intro": "We'll cluster customers by spending behavior, use the elbow method to choose k, and profile each cluster with business-meaningful labels.",
                "key_insight": "K-Means requires you to specify k in advance. Use the elbow method (plot inertia vs k and find the bend) or silhouette score to choose. Always scale features — K-Means uses Euclidean distance, same as KNN."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 500
df = pd.DataFrame({
    'annual_spend':    np.concatenate([np.random.normal(5000,1000,150), np.random.normal(25000,3000,200), np.random.normal(80000,10000,150)]),
    'purchase_freq':   np.concatenate([np.random.normal(2,1,150), np.random.normal(8,2,200), np.random.normal(20,3,150)]),
    'avg_order_value': np.concatenate([np.random.normal(80,20,150), np.random.normal(200,40,200), np.random.normal(600,100,150)]),
})

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Elbow method: find optimal k
print("Elbow Method (inertia vs k):")
for k in range(2, 9):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    print(f"  k={k}: inertia={km.inertia_:.0f}")

# Fit with k=3 (natural 3 segments)
km = KMeans(n_clusters=3, random_state=42, n_init=10)
df['segment'] = km.fit_predict(X_scaled)

# Profile each cluster
print("\\nCluster Profiles:")
profile = df.groupby('segment')[['annual_spend','purchase_freq','avg_order_value']].mean()
profile['count'] = df.groupby('segment').size()
for seg, row in profile.iterrows():
    label = ['Budget Shoppers','Regular Customers','Premium Buyers'][seg]
    print(f"  Cluster {seg} ({label}): {row['count']:.0f} customers | spend=${row['annual_spend']:,.0f} | freq={row['purchase_freq']:.1f}x/yr | avg=${row['avg_order_value']:.0f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "KMeans(n_clusters=3, random_state=42, n_init=10)",
                        "labels = km.fit_predict(X_scaled)",
                        "km.inertia_  -- sum of squared distances to nearest centroid",
                        "km.cluster_centers_  -- centroid coordinates"
                    ],
                    "notes": "Always scale features before K-Means. Set n_init=10 to run 10 random initializations and keep the best. random_state ensures reproducibility."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "What does the 'elbow method' help determine in K-Means?", "options": ["The optimal learning rate","The optimal number of clusters k","Whether the data is clusterable","The scale of features"], "answer": 1, "explanation": "The elbow method plots inertia (sum of squared distances to centroids) vs k. Inertia always decreases as k increases. The 'elbow' — where the rate of decrease sharply slows — suggests the optimal k, balancing cluster compactness vs. simplicity."},
                    {"type": "true_false", "question": "K-Means clustering requires labeled training data.", "answer": False, "explanation": "K-Means is unsupervised — it finds patterns without any labels. This is both its power (works on any unlabeled dataset) and limitation (you must interpret what the clusters mean in business terms after the algorithm runs)."},
                    {"type": "fill_blank", "question": "To get cluster assignments for new data: labels = km.___(X_scaled)", "template": "labels = km.___(X_scaled)", "answer": "fit_predict", "explanation": "fit_predict() fits the K-Means model and returns cluster labels in one step. Alternatively, fit() then predict() separately — useful when you want to assign new data to existing clusters without refitting."}
                ]
            },
            "challenge": {
                "instructions": "Segment website users by behavior: session duration, pages viewed, bounce rate, conversion. Use the elbow method to choose k. Fit K-Means, label clusters, and print a business-readable segment report. Identify which segment to target for a premium product campaign.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(7)
n = 600
df = pd.DataFrame({
    'avg_session_mins':  np.concatenate([np.random.normal(2,1,200), np.random.normal(8,2,250), np.random.normal(20,4,150)]),
    'pages_per_session': np.concatenate([np.random.normal(2,1,200), np.random.normal(6,1,250), np.random.normal(15,3,150)]),
    'bounce_rate':       np.concatenate([np.random.normal(0.8,0.1,200), np.random.normal(0.4,0.1,250), np.random.normal(0.1,0.05,150)]),
    'conversion_rate':   np.concatenate([np.random.normal(0.01,0.005,200), np.random.normal(0.05,0.01,250), np.random.normal(0.15,0.02,150)]),
})
df = df.clip(lower=0)

# Scale features

# Elbow method (k = 2 to 8)

# Fit with best k

# Profile clusters and name them

print("\\n=== Campaign Target ===")
# Which segment to target with premium product?
""",
                "tests": [{"type": "code_contains", "value": "KMeans"}, {"type": "code_contains", "value": "inertia_"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
np.random.seed(7)
n=600
df=pd.DataFrame({'avg_session_mins':np.concatenate([np.random.normal(2,1,200),np.random.normal(8,2,250),np.random.normal(20,4,150)]),'pages_per_session':np.concatenate([np.random.normal(2,1,200),np.random.normal(6,1,250),np.random.normal(15,3,150)]),'bounce_rate':np.concatenate([np.random.normal(0.8,0.1,200),np.random.normal(0.4,0.1,250),np.random.normal(0.1,0.05,150)]),'conversion_rate':np.concatenate([np.random.normal(0.01,0.005,200),np.random.normal(0.05,0.01,250),np.random.normal(0.15,0.02,150)])})
df=df.clip(lower=0)
scaler=StandardScaler(); X=scaler.fit_transform(df)
print("Elbow:")
for k in range(2,9):
    km=KMeans(n_clusters=k,random_state=42,n_init=10); km.fit(X)
    print(f"  k={k}: {km.inertia_:.0f}")
km=KMeans(n_clusters=3,random_state=42,n_init=10); df['seg']=km.fit_predict(X)
names={};
for s,grp in df.groupby('seg'):
    avg=grp.mean()
    name='Casual' if avg['avg_session_mins']<5 else ('Engaged' if avg['avg_session_mins']<12 else 'Power User')
    names[s]=name
    print(f"  Seg {s} ({name}): n={len(grp)} conv={avg['conversion_rate']:.1%}")
target=[k for k,v in names.items() if 'Power' in v][0]
print(f"\\n=== Campaign Target: Segment {target} ({names[target]}) ===")""",
                "challenge_variations": [
                    "Use silhouette_score to choose k instead of the elbow method.",
                    "Apply DBSCAN instead of K-Means and compare cluster shapes.",
                    "Cluster documents using TF-IDF features and K-Means — print top terms per cluster.",
                    "Apply K-Means to color quantization: compress an image to 16 colors.",
                    "Use hierarchical clustering (AgglomerativeClustering) on the same dataset.",
                    "Build a customer lifecycle model: assign new customers to existing clusters with km.predict().",
                    "Add cluster labels as a new feature to a classification model — does it improve accuracy?",
                    "Visualize clusters using PCA to reduce to 2D for plotting.",
                    "Compare K-Means stability: run 5 times with different random states — how consistent are the clusters?",
                    "Build a 'segment migration tracker': cluster customers at two time points and see who moved between segments."
                ]
            }
        },
        {
            "id": "m4-l14",
            "title": "Feature Scaling — Putting All Features on Equal Footing",
            "subtitle": "StandardScaler vs MinMaxScaler and when each is right",
            "difficulty": "beginner",
            "business_context": "Income ranges $20k-$200k while age ranges 18-70. Distance-based models (KNN, SVM, K-Means) and gradient-based models treat these very differently without scaling. A dollar sign in your data should not outweigh a year.",
            "concept": {
                "theory": "StandardScaler transforms each feature to mean=0 and std=1 (z-score normalization). MinMaxScaler scales to [0,1] range. RobustScaler uses median and IQR — resistant to outliers. Tree-based models (Decision Tree, Random Forest) don't need scaling. Neural networks, KNN, SVM, Logistic Regression, and K-Means all benefit significantly.",
                "business_angle": "Feature scaling is preprocessing hygiene. Forgetting it is one of the most common mistakes that causes models to underperform — especially in competitions and production. Always fit the scaler on training data only, then transform both train and test.",
                "worked_example_intro": "We'll demonstrate the impact of scaling on KNN and logistic regression, and show the critical train-fit/test-transform pattern.",
                "key_insight": "NEVER fit the scaler on the full dataset before splitting. Fit ONLY on training data, then transform test data. Fitting on test data is 'data leakage' — it lets test data influence your model, giving falsely optimistic accuracy estimates."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 600
X = pd.DataFrame({
    'income':  np.random.uniform(20000, 200000, n),
    'age':     np.random.randint(18, 70, n),
    'score':   np.random.uniform(300, 850, n),
    'ratio':   np.random.uniform(0.1, 0.9, n),
})
y = ((X['score'] > 600) & (X['ratio'] < 0.5)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Unscaled
knn = KNeighborsClassifier(5)
knn.fit(X_train, y_train)
print(f"Unscaled accuracy: {accuracy_score(y_test, knn.predict(X_test)):.1%}")

# StandardScaler — CORRECT pattern: fit on train, transform both
std = StandardScaler()
X_train_s = std.fit_transform(X_train)   # fit+transform on train
X_test_s  = std.transform(X_test)        # transform only on test (no fit!)

knn.fit(X_train_s, y_train)
print(f"StandardScaler:    {accuracy_score(y_test, knn.predict(X_test_s)):.1%}")

# MinMaxScaler
mm = MinMaxScaler()
X_train_m = mm.fit_transform(X_train)
X_test_m  = mm.transform(X_test)
knn.fit(X_train_m, y_train)
print(f"MinMaxScaler:      {accuracy_score(y_test, knn.predict(X_test_m)):.1%}")

# Show what scaling does to the values
print("\\nBefore vs After StandardScaler:")
print(f"  income: mean={X_train['income'].mean():,.0f}, std={X_train['income'].std():,.0f}")
print(f"  scaled: mean={X_train_s[:,0].mean():.2f}, std={X_train_s[:,0].std():.2f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "scaler = StandardScaler()",
                        "X_train_s = scaler.fit_transform(X_train)  -- fit+transform",
                        "X_test_s  = scaler.transform(X_test)       -- transform only!",
                        "MinMaxScaler()  -- scale to [0,1]",
                        "RobustScaler()  -- scale using median/IQR (outlier-resistant)"
                    ],
                    "notes": "Models that DO need scaling: KNN, SVM, Logistic Regression, Neural Nets, K-Means. Models that DON'T: Decision Trees, Random Forests, Gradient Boosting."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why should you fit the scaler ONLY on training data?", "options": ["It's faster","Fitting on test data leaks test information into the model, giving falsely optimistic results","Scalers can only handle one dataset","Test data may have different dimensions"], "answer": 1, "explanation": "Fitting the scaler on test data computes mean/std including test values. The model then 'sees' test data statistics during training — data leakage. In production, you'd be computing a scaler with future data you don't have yet. Always: fit on train, transform on test."},
                    {"type": "true_false", "question": "Random Forest models require feature scaling to perform well.", "answer": False, "explanation": "Tree-based models split on feature thresholds, not distances. Whether income is $50,000 or 0.5 (scaled), the tree finds the same relative threshold. Scaling has zero effect on tree-based models — but don't skip it for KNN, SVM, or neural networks."},
                    {"type": "fill_blank", "question": "To scale test data AFTER fitting on train: X_test_s = scaler.___(X_test)", "template": "X_test_s = scaler.___(X_test)", "answer": "transform", "explanation": "After scaler.fit_transform(X_train), use scaler.transform(X_test) — NOT fit_transform. This applies the exact same mean/std computed from training data to the test data, maintaining the correct relationship."}
                ]
            },
            "challenge": {
                "instructions": "Compare model performance with and without scaling on 3 algorithms: KNN, Logistic Regression, and Random Forest. Show which models benefit from scaling and which don't. Print a comparison table.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(3)
n = 800
X = pd.DataFrame({
    'salary':   np.random.uniform(30000, 150000, n),
    'age':      np.random.randint(22, 65, n),
    'score':    np.random.randint(400, 850, n),
    'years':    np.random.randint(0, 30, n),
})
y = ((X['score'] > 650) & (X['salary'] > 60000)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'KNN': KNeighborsClassifier(5),
    'LogReg': LogisticRegression(max_iter=1000),
    'RandomForest': RandomForestClassifier(100, random_state=42),
}

print(f"{'Model':<15} {'Unscaled':>10} {'Scaled':>10} {'Benefit':>10}")
print("-" * 48)
# For each model, train/test with and without scaling
# Print results
""",
                "tests": [{"type": "code_contains", "value": "StandardScaler"}, {"type": "code_contains", "value": "transform"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
np.random.seed(3)
n=800
X=pd.DataFrame({'salary':np.random.uniform(30000,150000,n),'age':np.random.randint(22,65,n),'score':np.random.randint(400,850,n),'years':np.random.randint(0,30,n)})
y=((X['score']>650)&(X['salary']>60000)).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
scaler=StandardScaler(); Xs_train=scaler.fit_transform(X_train); Xs_test=scaler.transform(X_test)
models={'KNN':KNeighborsClassifier(5),'LogReg':LogisticRegression(max_iter=1000),'RandomForest':RandomForestClassifier(100,random_state=42)}
print(f"{'Model':<15} {'Unscaled':>10} {'Scaled':>10} {'Benefit':>10}")
print("-"*48)
for name,m in models.items():
    m.fit(X_train,y_train); raw=accuracy_score(y_test,m.predict(X_test))
    m.fit(Xs_train,y_train); scaled=accuracy_score(y_test,m.predict(Xs_test))
    print(f"{name:<15} {raw:>10.1%} {scaled:>10.1%} {scaled-raw:>+10.1%}")""",
                "challenge_variations": [
                    "Compare StandardScaler vs RobustScaler when data has outliers (5% of rows with 10x normal values).",
                    "Build a pipeline using sklearn Pipeline to chain scaler + model and avoid leakage.",
                    "Show what happens when you accidentally fit_transform on the full dataset before splitting.",
                    "Use PowerTransformer to normalize skewed features (log-like transformation).",
                    "Apply QuantileTransformer to force a uniform distribution — when is this useful?",
                    "Scale only certain columns using ColumnTransformer.",
                    "Compare scaling impact on SVM classifier — SVM is extremely sensitive to scale.",
                    "Build a custom scaler class that clips outliers before scaling.",
                    "Demonstrate: save a fitted scaler with pickle, load it later, and apply to new data correctly.",
                    "Show the impact of not scaling on neural network training speed and convergence."
                ]
            }
        },
        {
            "id": "m4-l15",
            "title": "Feature Selection — Keep Only What Matters",
            "subtitle": "Remove irrelevant features to improve accuracy and interpretability",
            "difficulty": "intermediate",
            "business_context": "A dataset with 200 columns doesn't mean 200 signals. Many features are redundant, irrelevant, or noisy. Feature selection finds the 10-20 that actually drive predictions — making models faster, more interpretable, and often more accurate.",
            "concept": {
                "theory": "Three approaches: Filter methods (select by statistical correlation before training — fast), Wrapper methods (test feature subsets by model performance — accurate but slow), Embedded methods (model selects features during training — e.g., Lasso L1, tree importance). Variance threshold removes near-zero-variance features. SelectKBest selects top k by F-statistic or mutual information.",
                "business_angle": "Feature selection directly impacts the bottom line: fewer features mean faster predictions (lower inference cost), simpler models (easier to audit), and often better generalization. In regulated industries, being able to say 'the model uses these 5 features' is legally important.",
                "worked_example_intro": "We'll use variance threshold, SelectKBest (filter), and Random Forest importance (embedded) to select features from a noisy dataset.",
                "key_insight": "Adding more features usually hurts when those features are noise. The 'curse of dimensionality' means that in high dimensions, all points appear equidistant. Feature selection is the cure."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
# 5 useful features + 10 noise features
useful = pd.DataFrame({
    'credit_score':  np.random.randint(400, 850, n),
    'income':        np.random.uniform(20000, 150000, n),
    'debt_ratio':    np.random.uniform(0.1, 0.9, n),
    'missed_pmts':   np.random.randint(0, 5, n),
    'employment_yr': np.random.randint(0, 20, n),
})
noise = pd.DataFrame(np.random.randn(n, 10), columns=[f'noise_{i}' for i in range(10)])
X = pd.concat([useful, noise], axis=1)
y = ((useful['credit_score'] > 650) & (useful['debt_ratio'] < 0.4)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestClassifier(100, random_state=42)

# All features
rf.fit(X_train, y_train)
print(f"All 15 features: {accuracy_score(y_test, rf.predict(X_test)):.1%}")

# Variance threshold (remove near-constant features)
vt = VarianceThreshold(threshold=0.01)
X_vt = vt.fit_transform(X_train)
print(f"After VarianceThreshold: {X_vt.shape[1]} features")

# SelectKBest (top 5 by ANOVA F-statistic)
skb = SelectKBest(f_classif, k=5)
X_train_k = skb.fit_transform(X_train, y_train)
X_test_k  = skb.transform(X_test)
selected = [X.columns[i] for i in skb.get_support(indices=True)]
print(f"SelectKBest selected: {selected}")
rf.fit(X_train_k, y_train)
print(f"Top 5 features: {accuracy_score(y_test, rf.predict(X_test_k)):.1%}")

# Feature importance from Random Forest
rf.fit(X_train, y_train)
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\\nTop 6 by RF importance:")
for feat, imp in importances.head(6).items():
    print(f"  {feat:<18} {imp:.3f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "SelectKBest(f_classif, k=5).fit_transform(X_train, y_train)",
                        "VarianceThreshold(threshold=0.01).fit_transform(X)",
                        "rf.feature_importances_  -- embedded selection",
                        "skb.get_support(indices=True)  -- get selected feature indices"
                    ],
                    "notes": "For classification: use f_classif or mutual_info_classif in SelectKBest. For regression: use f_regression or mutual_info_regression."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Which of these is an embedded feature selection method?", "options": ["Removing features with correlation > 0.9","SelectKBest with F-statistic","L1 (Lasso) regularization that zeroes out feature weights","Manually removing features based on domain knowledge"], "answer": 2, "explanation": "Embedded methods select features as part of the model training process. Lasso (L1 regularization) penalizes large weights and drives unimportant feature weights to exactly zero — selecting features while training. Random Forest's feature_importances_ is also embedded."},
                    {"type": "true_false", "question": "Adding more features always improves model performance.", "answer": False, "explanation": "This is false — the 'curse of dimensionality' means more features can hurt. Noise features add irrelevant variation, making it harder for the model to find real patterns. Feature selection often improves both accuracy and training speed."},
                    {"type": "fill_blank", "question": "Select top 10 features by F-score: selector = SelectKBest(f_classif, k=___)", "template": "selector = SelectKBest(f_classif, k=___)", "answer": "10", "explanation": "k specifies how many top features to keep. Use cross-validation to find the optimal k. skb.get_support(indices=True) returns the column indices of selected features."}
                ]
            },
            "challenge": {
                "instructions": "Start with 30 features (5 real + 25 noise). Compare model accuracy using: all features, top 5 by SelectKBest, top 5 by RF importance, and manual selection of the 5 known-good features. Print the comparison.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

np.random.seed(11)
n = 1000
real_feats = pd.DataFrame({
    'credit': np.random.randint(400,850,n), 'income': np.random.uniform(20000,150000,n),
    'debt':   np.random.uniform(0.1,0.9,n), 'missed': np.random.randint(0,5,n),
    'tenure': np.random.randint(0,20,n),
})
noise = pd.DataFrame(np.random.randn(n,25), columns=[f'noise_{i}' for i in range(25)])
X = pd.concat([real_feats, noise], axis=1)
y = ((real_feats['credit'] > 650) & (real_feats['debt'] < 0.4)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestClassifier(100, random_state=42)

print(f"{'Method':<25} {'CV Accuracy':>12}")
print("-" * 38)
# 1. All 30 features
# 2. SelectKBest k=5
# 3. Top 5 RF importance
# 4. Known real features
""",
                "tests": [{"type": "code_contains", "value": "SelectKBest"}, {"type": "code_contains", "value": "feature_importances_"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
np.random.seed(11)
n=1000
real_feats=pd.DataFrame({'credit':np.random.randint(400,850,n),'income':np.random.uniform(20000,150000,n),'debt':np.random.uniform(0.1,0.9,n),'missed':np.random.randint(0,5,n),'tenure':np.random.randint(0,20,n)})
noise=pd.DataFrame(np.random.randn(n,25),columns=[f'noise_{i}' for i in range(25)])
X=pd.concat([real_feats,noise],axis=1); y=((real_feats['credit']>650)&(real_feats['debt']<0.4)).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
rf=RandomForestClassifier(100,random_state=42)
print(f"{'Method':<25} {'CV Accuracy':>12}"); print("-"*38)
# All
rf.fit(X_train,y_train); print(f"{'All 30':<25} {cross_val_score(rf,X,y,cv=5).mean():>12.1%}")
# SelectKBest
skb=SelectKBest(f_classif,k=5); Xk=skb.fit_transform(X,y)
rf.fit(skb.transform(X_train),y_train); print(f"{'SelectKBest k=5':<25} {cross_val_score(rf,Xk,y,cv=5).mean():>12.1%}")
# RF importance
rf.fit(X_train,y_train); top5=pd.Series(rf.feature_importances_,index=X.columns).nlargest(5).index
Xrf=X[top5]; print(f"{'RF Top 5':<25} {cross_val_score(rf,Xrf,y,cv=5).mean():>12.1%}")
# Known real
Xr=X[real_feats.columns]; print(f"{'Known Real':<25} {cross_val_score(rf,Xr,y,cv=5).mean():>12.1%}")""",
                "challenge_variations": [
                    "Use RFECV (Recursive Feature Elimination with CV) to automatically find the optimal number of features.",
                    "Use mutual_info_classif instead of f_classif and compare which features each method selects.",
                    "Compare Lasso (L1) feature selection: train Lasso, check which coefficients are zero.",
                    "Build a feature importance plot sorted by importance with matplotlib.",
                    "Use PermutationImportance for a more robust importance estimate than RF built-in.",
                    "Find and remove highly correlated features (correlation > 0.9) before modeling.",
                    "Use PCA for dimensionality reduction instead of feature selection — compare approaches.",
                    "Build a feature selection pipeline that first removes low-variance, then selects top-k.",
                    "Apply feature selection to a text classification problem with TF-IDF features.",
                    "Run SelectKBest with k=1 through k=20 and plot accuracy vs number of features."
                ]
            }
        },
        {
            "id": "m4-l16",
            "title": "Cross-Validation — Reliable Model Evaluation",
            "subtitle": "Stop gambling on one train-test split — use k-fold CV for trustworthy scores",
            "difficulty": "intermediate",
            "business_context": "Your model scores 92% accuracy. But is that because the model is good, or because you got lucky with which 20% became your test set? Cross-validation uses every data point as both training and testing data — giving you a much more reliable estimate.",
            "concept": {
                "theory": "K-fold cross-validation splits data into k equal folds. For each fold: train on the other k-1 folds, test on this fold. Repeat k times. Average the k scores. The result: a reliable performance estimate with a standard deviation showing consistency. 5-fold and 10-fold are the most common choices.",
                "business_angle": "In a business pitch, 'our model achieves 87% ± 2% accuracy across 5-fold CV' is far more credible than '92% on a single test set.' CV is how you prove a model is genuinely good, not just got lucky on one split.",
                "worked_example_intro": "We'll compare single train-test split accuracy vs 5-fold CV across multiple models and show how CV reveals more reliable estimates.",
                "key_insight": "Use cross_val_score for quick CV. Use StratifiedKFold for imbalanced classification (ensures each fold has the same class ratio). Use cross_validate to get multiple metrics at once."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.model_selection import (train_test_split, cross_val_score,
                                      StratifiedKFold, cross_validate)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
X = np.column_stack([np.random.randn(n, 4)])
y = (X[:,0] + X[:,1] > 0.3).astype(int)

models = {
    'LogReg':   LogisticRegression(max_iter=1000),
    'Tree(5)':  DecisionTreeClassifier(max_depth=5, random_state=42),
    'RF(100)':  RandomForestClassifier(100, random_state=42),
}

print(f"{'Model':<12} {'Single Split':>13} {'5-Fold CV':>12} {'Std Dev':>9}")
print("-" * 50)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
for name, m in models.items():
    m.fit(X_train, y_train)
    single = accuracy_score(y_test, m.predict(X_test))
    cv_scores = cross_val_score(m, X, y, cv=5, scoring='accuracy')
    print(f"{name:<12} {single:>13.1%} {cv_scores.mean():>12.1%} {cv_scores.std():>9.1%}")

# StratifiedKFold for imbalanced data
print("\\nStratifiedKFold (10% positive class):")
y_imbal = (np.random.rand(n) < 0.10).astype(int)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv = cross_val_score(RandomForestClassifier(100,random_state=42,class_weight='balanced'),
                     X, y_imbal, cv=skf, scoring='f1')
print(f"  F1: {cv.mean():.3f} ± {cv.std():.3f}")

# cross_validate: multiple metrics at once
cv_multi = cross_validate(RandomForestClassifier(100,random_state=42), X, y,
                           cv=5, scoring=['accuracy','f1','roc_auc'])
print("\\nMultiple metrics (RF):")
for metric in ['accuracy','f1','roc_auc']:
    vals = cv_multi[f'test_{metric}']
    print(f"  {metric:<12}: {vals.mean():.3f} ± {vals.std():.3f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "cross_val_score(model, X, y, cv=5, scoring='accuracy')",
                        "cross_validate(model, X, y, cv=5, scoring=['accuracy','f1'])",
                        "StratifiedKFold(n_splits=5, shuffle=True, random_state=42)",
                        "scores.mean(), scores.std()  -- summarize CV results"
                    ],
                    "notes": "5-fold CV is the default. 10-fold is better for small datasets. Stratified CV maintains class ratios in each fold — always use it for classification."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "What is the main advantage of 5-fold CV over a single train-test split?", "options": ["It's faster to compute","Every data point is used for both training and testing, giving a more reliable estimate","It prevents overfitting","It automatically tunes hyperparameters"], "answer": 1, "explanation": "With a single split, your accuracy estimate depends heavily on which 20% happened to be in the test set. 5-fold CV uses every point as a test sample exactly once across 5 runs, giving a more stable and unbiased estimate of true model performance."},
                    {"type": "true_false", "question": "StratifiedKFold ensures each fold has the same proportion of each class.", "answer": True, "explanation": "StratifiedKFold preserves the class distribution across folds. For a dataset with 10% positives, each fold also contains approximately 10% positives. This is critical for imbalanced datasets — otherwise some folds might have no positive examples at all."},
                    {"type": "fill_blank", "question": "Run 5-fold CV and get accuracy scores: scores = ___(model, X, y, cv=5)", "template": "scores = ___(model, X, y, cv=5)", "answer": "cross_val_score", "explanation": "cross_val_score returns an array of k scores (one per fold). Use .mean() for the average and .std() for consistency. The default scoring depends on the estimator type — pass scoring='accuracy' or scoring='f1' explicitly."}
                ]
            },
            "challenge": {
                "instructions": "Compare 3 models using 5-fold stratified CV on an imbalanced dataset (15% positive). Report accuracy, F1, and ROC-AUC for each. Identify which model is truly best when you look at all three metrics.",
                "starter_code": """import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

np.random.seed(42)
n = 1000
X = np.column_stack([np.random.randn(n, 5)])
y = (np.random.rand(n) < 0.15).astype(int)

models = {
    'LogReg':    LogisticRegression(class_weight='balanced', max_iter=1000),
    'RF':        RandomForestClassifier(100, class_weight='balanced', random_state=42),
    'GBM':       GradientBoostingClassifier(100, random_state=42),
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
metrics = ['accuracy', 'f1', 'roc_auc']

print(f"{'Model':<12} {'Accuracy':>10} {'F1':>8} {'ROC-AUC':>10}")
print("-" * 44)
# Run cross_validate for each model and print results
""",
                "tests": [{"type": "code_contains", "value": "cross_validate"}, {"type": "code_contains", "value": "StratifiedKFold"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
np.random.seed(42)
n=1000
X=np.column_stack([np.random.randn(n,5)])
y=(np.random.rand(n)<0.15).astype(int)
models={'LogReg':LogisticRegression(class_weight='balanced',max_iter=1000),'RF':RandomForestClassifier(100,class_weight='balanced',random_state=42),'GBM':GradientBoostingClassifier(100,random_state=42)}
skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
print(f"{'Model':<12} {'Accuracy':>10} {'F1':>8} {'ROC-AUC':>10}"); print("-"*44)
for name,m in models.items():
    cv=cross_validate(m,X,y,cv=skf,scoring=['accuracy','f1','roc_auc'])
    print(f"{name:<12} {cv['test_accuracy'].mean():>10.1%} {cv['test_f1'].mean():>8.3f} {cv['test_roc_auc'].mean():>10.3f}")""",
                "challenge_variations": [
                    "Use LeaveOneOut CV on a tiny dataset (n=50) and compare to 5-fold CV.",
                    "Use TimeSeriesSplit for temporal data instead of random K-fold.",
                    "Build a nested CV: outer CV for evaluation, inner CV for hyperparameter tuning.",
                    "Use cross_val_predict to get out-of-fold predictions for a full dataset.",
                    "Compare 5-fold vs 10-fold CV — when does the extra computation of 10-fold matter?",
                    "Run CV on a pipeline (scaler + model) to ensure scaler is refit on each fold.",
                    "Use GroupKFold when you have groups (e.g., same customer across multiple rows) that shouldn't split across folds.",
                    "Bootstrap sampling: implement your own bootstrap evaluation (sample with replacement 100 times).",
                    "Visualize the variance of CV scores across 5 folds with a box plot.",
                    "Compare a tree's CV score with and without StratifiedKFold on heavily imbalanced data."
                ]
            }
        },
        {
            "id": "m4-l17",
            "title": "Overfitting & Underfitting — The Bias-Variance Tradeoff",
            "subtitle": "Why your training accuracy is misleading and how to fix it",
            "difficulty": "intermediate",
            "business_context": "Your model scores 99% training accuracy but only 62% on new data. It memorized the training set instead of learning the pattern. This is overfitting — the #1 reason ML models fail in production.",
            "concept": {
                "theory": "Overfitting: model is too complex, memorizes training data, fails on new data (high variance). Underfitting: model is too simple, misses the real pattern, performs poorly on both train and test (high bias). The sweet spot: a model complex enough to capture the real signal but simple enough to generalize. Diagnosed with learning curves.",
                "business_angle": "The gap between training and test accuracy is your overfitting meter. If a model scores 99% in dev but 70% in production, the business impact is real. Overfitting is avoided with: proper train/test split, cross-validation, regularization, early stopping, and more data.",
                "worked_example_intro": "We'll plot learning curves showing train vs test accuracy as a function of model complexity and training size.",
                "key_insight": "Learning curve diagnosis: if training accuracy is high but test accuracy is low → overfitting (need simpler model or more data). If both are low → underfitting (need more complex model). If both are similar and high → good fit."
            },
            "worked_example": """import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, learning_curve, cross_val_score
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 1000
X = np.column_stack([np.random.randn(n, 5)])
y = (X[:,0] + 0.5*X[:,1] - 0.3*X[:,2] > 0.2).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("=== Model Complexity vs Overfitting ===")
print(f"{'Depth':<8} {'Train Acc':>10} {'Test Acc':>10} {'Gap':>8} {'Status':>15}")
print("-" * 55)
for depth in [1, 2, 3, 5, 8, 15, None]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    tr = accuracy_score(y_train, m.predict(X_train))
    te = accuracy_score(y_test, m.predict(X_test))
    gap = tr - te
    if gap > 0.15:
        status = 'OVERFIT'
    elif te < 0.70:
        status = 'UNDERFIT'
    else:
        status = 'Good fit'
    print(f"{str(depth):<8} {tr:>10.1%} {te:>10.1%} {gap:>8.1%} {status:>15}")

# Learning curve: accuracy vs training set size
print("\\n=== Learning Curves (depth=5 tree) ===")
train_sizes, train_scores, test_scores = learning_curve(
    DecisionTreeClassifier(max_depth=5, random_state=42),
    X, y, cv=5, train_sizes=[0.1, 0.2, 0.4, 0.6, 0.8, 1.0])
print(f"{'Train Size':>12} {'Train Acc':>12} {'CV Acc':>12}")
for sz, tr, te in zip(train_sizes, train_scores.mean(axis=1), test_scores.mean(axis=1)):
    print(f"{sz:>12} {tr:>12.1%} {te:>12.1%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "learning_curve(model, X, y, cv=5, train_sizes=[0.1,...,1.0])",
                        "High train acc + low test acc → overfitting (reduce complexity)",
                        "Low train acc + low test acc → underfitting (increase complexity)",
                        "Similar train & test + high → good generalization"
                    ],
                    "notes": "The primary fixes for overfitting: add more data, reduce model complexity, add regularization, use cross-validation. For underfitting: increase complexity, add features, reduce regularization."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "A model has 98% train accuracy and 64% test accuracy. This indicates:", "options": ["Underfitting — both accuracies should be higher","Good generalization — 64% is fine","Overfitting — the model memorized training data","Data imbalance — need more positive examples"], "answer": 2, "explanation": "A 34-point gap between train (98%) and test (64%) is classic overfitting. The model learned the specific noise and idiosyncrasies of the training set rather than the underlying pattern. Fix: reduce model complexity, add regularization, or get more training data."},
                    {"type": "true_false", "question": "Adding more training data always reduces overfitting.", "answer": True, "explanation": "More data makes it harder for the model to memorize — there's simply more variety to generalize from. Learning curves showing the gap between train and test accuracy narrowing as data increases is the signature of overfitting that more data can fix."},
                    {"type": "fill_blank", "question": "Generate learning curves: train_sizes, train_scores, test_scores = ___(model, X, y, cv=5)", "template": "train_sizes, train_scores, test_scores = ___(model, X, y, cv=5)", "answer": "learning_curve", "explanation": "learning_curve() from sklearn.model_selection trains the model on increasing fractions of the data and returns train/test scores at each size. The gap between train and test curves reveals overfitting vs underfitting."}
                ]
            },
            "challenge": {
                "instructions": "Demonstrate overfitting and underfitting on a classification task. Build learning curves for a shallow tree (depth=2), deep tree (depth=20), and random forest. For each: print train/test accuracy and diagnose the fit status. Print recommendations.",
                "starter_code": """import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

np.random.seed(99)
n = 600
X = np.column_stack([np.random.randn(n, 6)])
y = (X[:,0] + 0.7*X[:,1] - 0.4*X[:,3] > 0.1).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

models = {
    'Shallow Tree (depth=2)': DecisionTreeClassifier(max_depth=2, random_state=42),
    'Deep Tree (depth=20)':   DecisionTreeClassifier(max_depth=20, random_state=42),
    'Random Forest (100)':    RandomForestClassifier(100, random_state=42),
}

print(f"{'Model':<28} {'Train':>8} {'Test':>8} {'Gap':>7} {'Diagnosis':>15}")
print("-" * 72)
# Train each, compute gap, diagnose
# Print recommendation for the overfitting model
""",
                "tests": [{"type": "code_contains", "value": "DecisionTreeClassifier"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
np.random.seed(99)
n=600
X=np.column_stack([np.random.randn(n,6)])
y=(X[:,0]+0.7*X[:,1]-0.4*X[:,3]>0.1).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=42)
models={'Shallow Tree (depth=2)':DecisionTreeClassifier(max_depth=2,random_state=42),'Deep Tree (depth=20)':DecisionTreeClassifier(max_depth=20,random_state=42),'Random Forest (100)':RandomForestClassifier(100,random_state=42)}
print(f"{'Model':<28} {'Train':>8} {'Test':>8} {'Gap':>7} {'Diagnosis':>15}"); print("-"*72)
for name,m in models.items():
    m.fit(X_train,y_train); tr=accuracy_score(y_train,m.predict(X_train)); te=accuracy_score(y_test,m.predict(X_test))
    diag='OVERFIT' if tr-te>0.15 else ('UNDERFIT' if te<0.70 else 'Good fit')
    print(f"{name:<28} {tr:>8.1%} {te:>8.1%} {tr-te:>7.1%} {diag:>15}")
print("\\nRecommendation: Deep tree overfits — reduce max_depth or use Random Forest.")""",
                "challenge_variations": [
                    "Plot learning curves for all 3 models and identify where each crosses.",
                    "Add dropout rate experiment: train on 100, 200, 500, 1000, 2000 samples and see when overfitting resolves.",
                    "Compare validation curves: model accuracy vs max_depth (1 through 25).",
                    "Apply early stopping to a GradientBoosting model: monitor val score and stop when it starts declining.",
                    "Show how adding irrelevant features increases overfitting.",
                    "Demonstrate: a polynomial regression with degree=1 (underfit) vs degree=10 (overfit) vs degree=3 (good).",
                    "Use regularization (C parameter in LogisticRegression) to control overfitting — plot accuracy vs C.",
                    "Build a bias-variance decomposition experiment: sample different training sets, measure variance in predictions.",
                    "Show how increasing training set size narrows the train-test accuracy gap for an overfit model.",
                    "Compare RandomForest (low overfitting) to a deep single tree (high overfitting) with the same max_depth."
                ]
            }
        },
        {
            "id": "m4-l18",
            "title": "Regularization — Penalizing Complexity to Prevent Overfitting",
            "subtitle": "L1 (Lasso) and L2 (Ridge) add a complexity tax that forces models to stay simple",
            "difficulty": "intermediate",
            "business_context": "Your logistic regression model has 500 features but only learns noise. Regularization adds a penalty for large weights, forcing the model to rely on fewer, stronger signals. L1 (Lasso) zeros out unimportant features. L2 (Ridge) shrinks all weights toward zero.",
            "concept": {
                "theory": "Regularization adds a penalty term to the loss function: L1 adds sum(|weights|), L2 adds sum(weights²). The strength is controlled by C in sklearn (smaller C = stronger regularization). L1 produces sparse models (many exact zeros = feature selection). L2 handles correlated features better. ElasticNet combines both.",
                "business_angle": "Regularization is the standard fix for overfitting in linear models. It's also standard practice in production ML — unregularized models trained on real data almost always overfit. The C parameter is typically tuned with cross-validation.",
                "worked_example_intro": "We'll compare no regularization vs L1 vs L2, showing how each affects model coefficients and generalization.",
                "key_insight": "In sklearn's LogisticRegression: C is the INVERSE of regularization strength. C=1.0 is default (moderate). C=0.01 is strong regularization (aggressive shrinkage). C=100 is weak regularization (approaches no regularization)."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
# 5 real features + 15 noisy features
X_real = np.random.randn(n, 5)
X_noise = np.random.randn(n, 15) * 0.3
X = np.column_stack([X_real, X_noise])
y = (X_real[:,0] + 0.8*X_real[:,1] - 0.5*X_real[:,2] > 0.2).astype(int)
cols = [f'real_{i}' for i in range(5)] + [f'noise_{i}' for i in range(15)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

print("=== Regularization Comparison ===")
configs = [
    ('No reg (C=1000)', LogisticRegression(C=1000, max_iter=1000)),
    ('L2 Ridge (C=1)', LogisticRegression(C=1.0, max_iter=1000)),
    ('L2 Ridge (C=0.1)', LogisticRegression(C=0.1, max_iter=1000)),
    ('L1 Lasso (C=0.1)', LogisticRegression(C=0.1, penalty='l1', solver='liblinear', max_iter=1000)),
]
for name, m in configs:
    m.fit(X_train_s, y_train)
    tr = accuracy_score(y_train, m.predict(X_train_s))
    te = accuracy_score(y_test,  m.predict(X_test_s))
    zeros = (abs(m.coef_[0]) < 0.001).sum()
    print(f"  {name:<22}: train={tr:.1%}  test={te:.1%}  zero_coefs={zeros}")

# L1 does feature selection (sparse coefficients)
lasso = LogisticRegression(C=0.05, penalty='l1', solver='liblinear', max_iter=1000)
lasso.fit(X_train_s, y_train)
nonzero = [(cols[i], round(lasso.coef_[0][i],3)) for i in range(20) if abs(lasso.coef_[0][i]) > 0.01]
print(f"\\nL1 kept {len(nonzero)} non-zero features:")
for feat, coef in sorted(nonzero, key=lambda x: -abs(x[1]))[:8]:
    print(f"  {feat}: {coef:+.3f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "LogisticRegression(C=1.0)  -- default L2, C=inverse of strength",
                        "LogisticRegression(penalty='l1', solver='liblinear')  -- L1 Lasso",
                        "LogisticRegression(penalty='elasticnet', l1_ratio=0.5, solver='saga')",
                        "Ridge(alpha=1.0)  -- for regression (alpha=inverse of C)"
                    ],
                    "notes": "Smaller C = more regularization. L1 creates sparsity (zeros). L2 shrinks all equally. Always scale before regularization — regularization penalizes large coefficients, which depend on feature scale."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "What does L1 regularization (Lasso) do to unimportant feature weights?", "options": ["Makes them very small but never exactly zero","Sets them to exactly zero (sparse model)","Makes them negative","Removes those features from the dataset"], "answer": 1, "explanation": "L1 penalizes the sum of absolute values of weights. The geometry of L1 creates corners at zero — optimization naturally drives unimportant weights to exactly zero. This makes L1 perform implicit feature selection, unlike L2 which only shrinks weights."},
                    {"type": "true_false", "question": "Increasing C in LogisticRegression increases the strength of regularization.", "answer": False, "explanation": "In sklearn, C is the INVERSE of regularization strength. C=0.01 = strong regularization (many coefficients near zero). C=100 = weak regularization (approaches no penalty). This is the opposite of alpha in Ridge/Lasso where larger alpha = more regularization."},
                    {"type": "fill_blank", "question": "To use L1 Lasso regularization with LogisticRegression: LogisticRegression(penalty='___', solver='liblinear')", "template": "LogisticRegression(penalty='___', solver='liblinear')", "answer": "l1", "explanation": "penalty='l1' selects Lasso. The solver must be changed to 'liblinear' or 'saga' because the default 'lbfgs' doesn't support L1. ElasticNet (penalty='elasticnet') combines L1 and L2."}
                ]
            },
            "challenge": {
                "instructions": "Build a regularization experiment on a high-dimensional dataset (50 features, only 8 are real signals). Compare L1 at C=0.01, 0.1, 1.0 and L2 at C=0.01, 0.1, 1.0. Report train/test accuracy and number of non-zero coefficients for each. Identify the best C for L1.",
                "starter_code": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

np.random.seed(5)
n = 600
X_real = np.random.randn(n, 8)
X_noise = np.random.randn(n, 42)
X = np.column_stack([X_real, X_noise])
y = (X_real[:,0] + X_real[:,1] - 0.5*X_real[:,3] > 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

print(f"{'Model':<20} {'C':>6} {'Train':>8} {'Test':>8} {'Non-zero':>10}")
print("-" * 56)
# Try L1 at C = 0.01, 0.1, 1.0
# Try L2 at C = 0.01, 0.1, 1.0
# For each: print train acc, test acc, non-zero coefficients
""",
                "tests": [{"type": "code_contains", "value": "penalty"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
np.random.seed(5)
n=600
X_real=np.random.randn(n,8); X_noise=np.random.randn(n,42)
X=np.column_stack([X_real,X_noise]); y=(X_real[:,0]+X_real[:,1]-0.5*X_real[:,3]>0).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
scaler=StandardScaler(); Xs=scaler.fit_transform(X_train); Xt=scaler.transform(X_test)
print(f"{'Model':<20} {'C':>6} {'Train':>8} {'Test':>8} {'Non-zero':>10}"); print("-"*56)
for pen,sol in [('l1','liblinear'),('l2','lbfgs')]:
    for c in [0.01,0.1,1.0]:
        m=LogisticRegression(penalty=pen,C=c,solver=sol,max_iter=1000); m.fit(Xs,y_train)
        nz=(abs(m.coef_[0])>0.001).sum()
        print(f"{f'L{pen[-1]} {pen}':<20} {c:>6} {accuracy_score(y_train,m.predict(Xs)):>8.1%} {accuracy_score(y_test,m.predict(Xt)):>8.1%} {nz:>10}")""",
                "challenge_variations": [
                    "Apply Ridge regression (Ridge(alpha=...)) to a continuous target and compare RMSE vs regularization strength.",
                    "Use Lasso for automatic feature selection: after fitting, print which features have non-zero coefficients.",
                    "Apply ElasticNet (penalty='elasticnet', l1_ratio=0.5) and compare with pure L1 and L2.",
                    "Use RidgeCV or LassoCV to automatically select the best regularization strength.",
                    "Show that without scaling, regularization penalizes high-range features unfairly.",
                    "Compare regularization in neural networks (weight_decay in PyTorch or kernel_regularizer in Keras) conceptually.",
                    "Apply dropout conceptually: explain how dropout acts like regularization for neural networks.",
                    "Use cross_val_score to find the optimal C for LogisticRegression with L1.",
                    "Build a path plot: show how L1 coefficients go from non-zero to zero as C decreases.",
                    "Compare regularized vs unregularized model performance as you reduce training data size."
                ]
            }
        },
        {
            "id": "m4-l19",
            "title": "Hyperparameter Tuning — Finding Your Model's Sweet Spot",
            "subtitle": "GridSearchCV and RandomizedSearchCV to find optimal settings",
            "difficulty": "intermediate",
            "business_context": "You've built a Random Forest, but which combination of n_estimators, max_depth, and min_samples_leaf produces the best predictions? Manually guessing is inefficient. Grid search systematically tests every combination; random search efficiently samples a large space.",
            "concept": {
                "theory": "Hyperparameters are model settings not learned from data (e.g., max_depth, n_estimators, C). GridSearchCV exhaustively tests every combination in a parameter grid, using cross-validation to score each. RandomizedSearchCV samples random combinations — faster for large search spaces. Both return the best_params_ and best_score_.",
                "business_angle": "Hyperparameter tuning is often the difference between a 78% model and an 84% model. A few percentage points can translate to millions in revenue in applications like fraud detection, pricing, or customer targeting. It's the highest-ROI step in the ML workflow.",
                "worked_example_intro": "We'll tune a Random Forest with GridSearchCV, then use RandomizedSearchCV for a larger parameter space.",
                "key_insight": "Always tune inside cross-validation to avoid overfitting to the test set. The test set should be used ONCE — only to report final performance. Use CV for ALL tuning decisions."
            },
            "worked_example": """import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
X = np.column_stack([np.random.randn(n, 6)])
y = (X[:,0] + 0.7*X[:,1] - 0.4*X[:,3] > 0.1).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# GridSearchCV: exhaustive over a small grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth':    [3, 5, 10, None],
    'min_samples_leaf': [1, 5, 10],
}
gs = GridSearchCV(RandomForestClassifier(random_state=42), param_grid,
                  cv=5, scoring='accuracy', n_jobs=-1)
gs.fit(X_train, y_train)
print(f"GridSearchCV best params: {gs.best_params_}")
print(f"Best CV score:  {gs.best_score_:.1%}")
print(f"Test accuracy:  {accuracy_score(y_test, gs.predict(X_test)):.1%}")

# RandomizedSearchCV: efficient over a larger space
from scipy.stats import randint
param_dist = {
    'n_estimators':     randint(50, 300),
    'max_depth':        [3, 5, 7, 10, None],
    'min_samples_leaf': randint(1, 20),
    'max_features':     ['sqrt', 'log2', 0.5],
}
rs = RandomizedSearchCV(RandomForestClassifier(random_state=42), param_dist,
                        n_iter=20, cv=5, scoring='accuracy', random_state=42, n_jobs=-1)
rs.fit(X_train, y_train)
print(f"\\nRandomizedSearchCV best params: {rs.best_params_}")
print(f"Best CV score:  {rs.best_score_:.1%}")
print(f"Test accuracy:  {accuracy_score(y_test, rs.predict(X_test)):.1%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "GridSearchCV(model, param_grid, cv=5, scoring='accuracy')",
                        "RandomizedSearchCV(model, param_dist, n_iter=20, cv=5)",
                        "search.best_params_  -- winning parameter combination",
                        "search.best_score_   -- best CV score",
                        "search.best_estimator_  -- the fitted model with best params"
                    ],
                    "notes": "Use n_jobs=-1 to parallelize across CPU cores. GridSearchCV is O(n_combinations × cv_folds). For >50 combinations, switch to RandomizedSearchCV."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "GridSearchCV with 4 values for n_estimators, 3 for max_depth, and 5-fold CV runs how many model fits?", "options": ["12","60","4+3=7","60 × 5 = 300"], "answer": 1, "explanation": "Grid search tests every combination: 4 × 3 = 12 combinations. Each combination is evaluated with 5-fold CV: 12 × 5 = 60 model fits. This grows exponentially — with 5 parameters at 4 values each: 4^5 = 1024 combinations, × 5 folds = 5120 fits."},
                    {"type": "true_false", "question": "After finding the best hyperparameters with GridSearchCV, you should re-train on the full training+test data.", "answer": False, "explanation": "The test set must remain completely unseen until final evaluation. Re-train the best model on the full training data (which GridSearchCV does internally via best_estimator_), but NEVER include test data in the training pipeline."},
                    {"type": "fill_blank", "question": "To get the best parameters found by grid search: params = gs.___", "template": "params = gs.___", "answer": "best_params_", "explanation": "best_params_ is a dict of the parameter combination with the highest CV score. best_score_ is that score. best_estimator_ is the actual fitted model with those parameters — ready for predictions."}
                ]
            },
            "challenge": {
                "instructions": "Tune a LogisticRegression for a churn classification task. Use GridSearchCV to tune C and penalty. Then use RandomizedSearchCV on a Random Forest with 4 hyperparameters. Compare the best models. Print final test accuracy for both.",
                "starter_code": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from scipy.stats import randint

np.random.seed(42)
n = 1000
X = np.column_stack([np.random.randn(n, 5)])
y = (X[:,0] + X[:,1] - 0.5*X[:,2] > 0.3).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale for logistic regression
scaler = StandardScaler()
Xs_train = scaler.fit_transform(X_train)
Xs_test  = scaler.transform(X_test)

# 1. Grid search LogisticRegression: C=[0.01,0.1,1,10], penalty=['l1','l2']
# Hint: use solver='liblinear' for L1+L2 support

# 2. RandomizedSearch RandomForest: n_iter=15
# params: n_estimators=randint(50,300), max_depth=[3,5,7,None], min_samples_leaf=randint(1,15)

print("Best LogReg:", ...)
print("Best RF:", ...)
""",
                "tests": [{"type": "code_contains", "value": "GridSearchCV"}, {"type": "code_contains", "value": "RandomizedSearchCV"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from scipy.stats import randint
np.random.seed(42)
n=1000; X=np.column_stack([np.random.randn(n,5)]); y=(X[:,0]+X[:,1]-0.5*X[:,2]>0.3).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
scaler=StandardScaler(); Xs=scaler.fit_transform(X_train); Xt=scaler.transform(X_test)
gs=GridSearchCV(LogisticRegression(solver='liblinear',max_iter=1000),{'C':[0.01,0.1,1,10],'penalty':['l1','l2']},cv=5,scoring='accuracy')
gs.fit(Xs,y_train); print(f"Best LogReg: {gs.best_params_} → test={accuracy_score(y_test,gs.predict(Xt)):.1%}")
rs=RandomizedSearchCV(RandomForestClassifier(random_state=42),{'n_estimators':randint(50,300),'max_depth':[3,5,7,None],'min_samples_leaf':randint(1,15)},n_iter=15,cv=5,scoring='accuracy',random_state=42,n_jobs=-1)
rs.fit(X_train,y_train); print(f"Best RF: {rs.best_params_} → test={accuracy_score(y_test,rs.predict(X_test)):.1%}")""",
                "challenge_variations": [
                    "Use GridSearchCV to tune an SVM's C and kernel parameters.",
                    "Build a Pipeline (scaler + model) and tune both the scaler and model in one GridSearchCV.",
                    "Use Bayesian optimization (optuna or scikit-optimize) for more efficient hyperparameter search.",
                    "Plot the GridSearchCV results: heatmap of CV score by C and max_depth.",
                    "Tune n_estimators using a simple loop with cross_val_score — compare to GridSearchCV.",
                    "Use halving_search (HalvingGridSearchCV) for faster tuning on large datasets.",
                    "Show the risk of test set contamination: tune on test set intentionally and show the inflation.",
                    "Tune a GradientBoostingClassifier (n_estimators, learning_rate, max_depth) with RandomizedSearchCV.",
                    "Build an automated ML baseline: try 5 models with default params + 2 tuned — print a comparison table.",
                    "Use joblib.Memory to cache GridSearchCV fits and resume interrupted searches."
                ]
            }
        },
        {
            "id": "m4-l20",
            "title": "ML Pipelines — Reproducible, Leak-Proof Workflows",
            "subtitle": "Chain preprocessing and modeling into a single object",
            "difficulty": "intermediate",
            "business_context": "You trained a model: scaled the data, then fit the classifier. In production, when a new customer arrives, how do you remember to apply the same scaling? A sklearn Pipeline packages preprocessing + model together — one object that transforms and predicts correctly every time.",
            "concept": {
                "theory": "sklearn.pipeline.Pipeline chains estimators sequentially. Each step's output feeds the next step's input. The key benefit: the Pipeline respects train/test boundaries — when you call pipeline.fit(X_train), all preprocessing fits on training data only. When you call pipeline.predict(X_test), preprocessing transforms using training statistics.",
                "business_angle": "Pipelines prevent data leakage (the #1 subtle ML mistake), make deployment simple (one object to save), ensure consistency between training and serving, and make experiments reproducible. Any production ML system should use pipelines.",
                "worked_example_intro": "We'll build a pipeline with StandardScaler + LogisticRegression, show it prevents leakage, and tune it with GridSearchCV.",
                "key_insight": "With a Pipeline, you can pass the entire pipeline to GridSearchCV or cross_val_score. This means the scaler is refit on each CV fold's training data — the correct, leakage-free approach. Naming convention: use __ (double underscore) to reference step parameters: 'classifier__C'."
            },
            "worked_example": """import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
X = np.column_stack([np.random.randn(n, 5) * [100, 0.5, 1000, 5, 0.1]])  # very different scales!
y = (X[:,0]/100 + X[:,1] - X[:,2]/1000 > 0).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a pipeline
pipe = Pipeline([
    ('scaler',     StandardScaler()),
    ('classifier', LogisticRegression(max_iter=1000)),
])

# Fit and predict — ONE object handles both preprocessing and prediction
pipe.fit(X_train, y_train)
print(f"Pipeline accuracy: {accuracy_score(y_test, pipe.predict(X_test)):.1%}")

# Cross-validation on the pipeline — scaler refit on each fold's train data (no leakage!)
cv_scores = cross_val_score(pipe, X, y, cv=5)
print(f"Pipeline CV: {cv_scores.mean():.1%} ± {cv_scores.std():.1%}")

# GridSearchCV on pipeline — use __ to access step parameters
param_grid = {
    'classifier__C': [0.01, 0.1, 1.0, 10.0],
    'classifier__penalty': ['l1', 'l2'],
}
gs = GridSearchCV(
    Pipeline([('scaler', StandardScaler()),
              ('classifier', LogisticRegression(solver='liblinear', max_iter=1000))]),
    param_grid, cv=5)
gs.fit(X_train, y_train)
print(f"Best pipeline params: {gs.best_params_}")
print(f"Best test accuracy:   {accuracy_score(y_test, gs.predict(X_test)):.1%}")

# Save and load pipeline
import pickle
with open('/tmp/pipeline.pkl', 'wb') as f:
    pickle.dump(gs.best_estimator_, f)
with open('/tmp/pipeline.pkl', 'rb') as f:
    loaded = pickle.load(f)
print(f"Loaded pipeline prediction: {loaded.predict(X_test[:1])}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "Pipeline([('step_name', estimator), ...])",
                        "pipe.fit(X_train, y_train)  -- fits all steps",
                        "pipe.predict(X_test)  -- transforms + predicts",
                        "step__param  -- GridSearchCV parameter naming"
                    ],
                    "notes": "Name steps descriptively. Last step must be an estimator (has predict). All other steps must be transformers (have transform). Use make_pipeline() for auto-naming."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why does using Pipeline with cross_val_score prevent data leakage?", "options": ["Pipelines automatically scale all data uniformly","The pipeline is refit from scratch on each CV fold's training data, so the scaler never sees the test fold","Pipelines skip preprocessing on test data","Pipeline automatically handles missing values"], "answer": 1, "explanation": "Without Pipeline, you might fit a scaler on all data before CV, which lets test data influence preprocessing — leakage. With Pipeline in cross_val_score, the entire pipeline (including scaler) is fit only on the training fold, applied to the test fold. This is the correct approach."},
                    {"type": "true_false", "question": "In a Pipeline, you access GridSearchCV parameters using a single underscore: 'classifier_C'.", "answer": False, "explanation": "GridSearchCV parameter names use DOUBLE underscore to reference pipeline steps: 'classifier__C' (two underscores between step name and parameter name). Single underscore is used for other things in sklearn. Example: pipe.set_params(scaler__with_mean=False)."},
                    {"type": "fill_blank", "question": "To name steps: pipe = Pipeline([('___(', StandardScaler()), ('model', LogisticRegression())])", "template": "pipe = Pipeline([('___', StandardScaler()), ('model', LogisticRegression())])", "answer": "scaler", "explanation": "Step names can be any string — choose descriptive names like 'scaler', 'imputer', 'selector', 'classifier'. Names are used to access steps (pipe['scaler']), set parameters in GridSearchCV ('scaler__with_mean'), and for debugging."}
                ]
            },
            "challenge": {
                "instructions": "Build a production-ready pipeline: SimpleImputer (handle missing values) → StandardScaler → RandomForestClassifier. Add 5% missing values to the data. Tune the RF's n_estimators and max_depth via GridSearchCV on the pipeline. Save the best pipeline to disk and load it back for prediction.",
                "starter_code": """import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import pickle

np.random.seed(42)
n = 800
X = np.column_stack([np.random.randn(n, 5)])
y = (X[:,0] + X[:,1] > 0.3).astype(int)

# Add 5% missing values
mask = np.random.rand(*X.shape) < 0.05
X[mask] = np.nan

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline: imputer → scaler → classifier

# GridSearchCV to tune 'classifier__n_estimators' and 'classifier__max_depth'

# Save best pipeline and load back

print("Test accuracy:", ...)
""",
                "tests": [{"type": "code_contains", "value": "Pipeline"}, {"type": "code_contains", "value": "pickle"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import pickle
np.random.seed(42)
n=800; X=np.column_stack([np.random.randn(n,5)]); y=(X[:,0]+X[:,1]>0.3).astype(int)
mask=np.random.rand(*X.shape)<0.05; X[mask]=np.nan
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
pipe=Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler()),('classifier',RandomForestClassifier(random_state=42))])
gs=GridSearchCV(pipe,{'classifier__n_estimators':[50,100],'classifier__max_depth':[5,10,None]},cv=5,n_jobs=-1)
gs.fit(X_train,y_train)
print(f"Best params: {gs.best_params_}")
with open('/tmp/pipe.pkl','wb') as f: pickle.dump(gs.best_estimator_,f)
with open('/tmp/pipe.pkl','rb') as f: loaded=pickle.load(f)
print(f"Test accuracy: {accuracy_score(y_test,loaded.predict(X_test)):.1%}")""",
                "challenge_variations": [
                    "Add a SelectKBest step to the pipeline and tune k in GridSearchCV.",
                    "Use ColumnTransformer inside a pipeline to apply different preprocessing to numerical and categorical columns.",
                    "Build a pipeline that includes PolynomialFeatures for non-linear logistic regression.",
                    "Add a custom transformer step by creating a class inheriting from BaseEstimator and TransformerMixin.",
                    "Use joblib instead of pickle to save/load the pipeline.",
                    "Build a pipeline for text data: CountVectorizer → TfidfTransformer → MultinomialNB.",
                    "Compare: manual preprocessing (bug risk) vs Pipeline (safe) on a CV experiment — show the score difference.",
                    "Use make_pipeline() for quick pipeline creation without naming steps.",
                    "Chain 3 transformers before a model: imputer → scaler → PCA → classifier.",
                    "Deploy the pipeline as a simple REST API using Flask: POST /predict returns model output."
                ]
            }
        },
        {
            "id": "m4-l21",
            "title": "ROC Curve & AUC — Evaluating at Every Threshold",
            "subtitle": "AUC-ROC is the gold standard for comparing binary classifiers",
            "difficulty": "intermediate",
            "business_context": "Your fraud model predicts probabilities (0.0–1.0). At what threshold do you flag a transaction? 0.5? 0.3? The ROC curve shows model performance at EVERY possible threshold — and AUC summarizes it in a single number that lets you compare models fairly.",
            "concept": {
                "theory": "The ROC (Receiver Operating Characteristic) curve plots True Positive Rate (Recall) vs False Positive Rate at every classification threshold from 0 to 1. AUC (Area Under Curve) ranges from 0.5 (random) to 1.0 (perfect). AUC measures: 'given a random positive and negative example, how often does the model score the positive higher?' — threshold-independent.",
                "business_angle": "AUC is the preferred metric when: (1) class thresholds will be tuned after deployment, (2) comparing models fairly regardless of threshold, (3) imbalanced datasets where accuracy is misleading. In fraud, medical, and credit scoring, AUC is the primary evaluation metric.",
                "worked_example_intro": "We'll compute ROC curves for multiple models, compare their AUC scores, and choose the optimal threshold for a specific business cost structure.",
                "key_insight": "AUC = 0.5 means the model is no better than random guessing. AUC = 0.7 is acceptable for hard problems. AUC > 0.8 is good. AUC > 0.9 is excellent. AUC = 1.0 is perfect (usually means data leakage)."
            },
            "worked_example": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve

np.random.seed(42)
n = 1000
X = np.column_stack([np.random.randn(n, 4)])
y = (np.random.rand(n) < 1/(1 + np.exp(-(X[:,0] + 0.8*X[:,1])))).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'LogReg': LogisticRegression(max_iter=1000),
    'RF':     RandomForestClassifier(100, random_state=42),
    'Random': None,  # baseline: random predictions
}

print("=== AUC-ROC Comparison ===")
for name, m in models.items():
    if m is None:
        proba = np.random.rand(len(y_test))
    else:
        m.fit(X_train, y_train)
        proba = m.predict_proba(X_test)[:,1]
    auc = roc_auc_score(y_test, proba)
    print(f"  {name:<10}: AUC = {auc:.4f}")

# ROC curve details for best model
rf = RandomForestClassifier(100, random_state=42)
rf.fit(X_train, y_train)
proba = rf.predict_proba(X_test)[:,1]
fpr, tpr, thresholds = roc_curve(y_test, proba)

print("\\nROC Curve sample points (FPR, TPR, threshold):")
idxs = [0, len(thresholds)//4, len(thresholds)//2, 3*len(thresholds)//4, -1]
for i in idxs:
    print(f"  FPR={fpr[i]:.2f}  TPR={tpr[i]:.2f}  threshold={thresholds[i] if i<len(thresholds) else 0:.2f}")

# Find threshold that maximizes TPR - FPR (Youden's J)
j_scores = tpr - fpr
best_idx = j_scores.argmax()
print(f"\\nOptimal threshold (Youden's J): {thresholds[best_idx]:.3f}")
print(f"At this threshold: TPR={tpr[best_idx]:.1%}, FPR={fpr[best_idx]:.1%}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "roc_auc_score(y_test, model.predict_proba(X_test)[:,1])",
                        "fpr, tpr, thresholds = roc_curve(y_test, proba)",
                        "AUC = 0.5 → random; AUC = 1.0 → perfect",
                        "Use predict_proba[:,1] for positive class probability"
                    ],
                    "notes": "ROC-AUC requires probability scores, not binary predictions. Use predict_proba(), not predict(). For multi-class: roc_auc_score with multi_class='ovr'."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "A model has AUC = 0.52. What does this tell you?", "options": ["It correctly classifies 52% of cases","It's barely better than random guessing","It has 52% recall","It makes 48% false positives"], "answer": 1, "explanation": "AUC = 0.5 is exactly random (a coin flip). AUC = 0.52 means the model is only marginally better than random. For business use, you typically want AUC > 0.75 for meaningful predictions."},
                    {"type": "true_false", "question": "AUC-ROC is independent of the classification threshold.", "answer": True, "explanation": "AUC evaluates the model's ranking ability across ALL possible thresholds simultaneously. This makes it ideal for comparing models even when the optimal threshold hasn't been decided yet."},
                    {"type": "fill_blank", "question": "Compute AUC score: auc = roc_auc_score(y_test, model.___(X_test)[:,1])", "template": "auc = roc_auc_score(y_test, model.___(X_test)[:,1])", "answer": "predict_proba", "explanation": "predict_proba() returns probability estimates — a 2D array where column 1 is the positive class probability. roc_auc_score needs continuous probabilities (not binary predictions) to compute the curve across all thresholds."}
                ]
            },
            "challenge": {
                "instructions": "Build an ROC analysis for a medical test (imbalanced: 8% disease). Compare 3 models by AUC. Find the optimal threshold for each using Youden's J statistic. Print the confusion matrix at the optimal threshold for the best model.",
                "starter_code": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix

np.random.seed(42)
n = 2000
X = np.column_stack([np.random.randn(n, 5)])
y = (np.random.rand(n) < 0.08).astype(int)  # 8% disease

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    'LogReg': LogisticRegression(class_weight='balanced', max_iter=1000),
    'RF':     RandomForestClassifier(100, class_weight='balanced', random_state=42),
    'GBM':    GradientBoostingClassifier(100, random_state=42),
}

# Compare AUC for all models

# For the best model: find optimal threshold using Youden's J

# Print confusion matrix at optimal threshold
""",
                "tests": [{"type": "code_contains", "value": "roc_auc_score"}, {"type": "code_contains", "value": "roc_curve"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix
np.random.seed(42)
n=2000; X=np.column_stack([np.random.randn(n,5)]); y=(np.random.rand(n)<0.08).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
models={'LogReg':LogisticRegression(class_weight='balanced',max_iter=1000),'RF':RandomForestClassifier(100,class_weight='balanced',random_state=42),'GBM':GradientBoostingClassifier(100,random_state=42)}
best_auc,best_proba,best_name=0,None,''
for name,m in models.items():
    m.fit(X_train,y_train); p=m.predict_proba(X_test)[:,1]; auc=roc_auc_score(y_test,p)
    print(f"{name}: AUC={auc:.4f}")
    if auc>best_auc: best_auc,best_proba,best_name=auc,p,name
fpr,tpr,thresh=roc_curve(y_test,best_proba)
j=tpr-fpr; best_t=thresh[j.argmax()]
print(f"\\nBest model: {best_name}, optimal threshold: {best_t:.3f}")
preds=(best_proba>=best_t).astype(int); print(confusion_matrix(y_test,preds))""",
                "challenge_variations": [
                    "Plot ROC curves for all 3 models on the same chart using matplotlib.",
                    "Compute Average Precision Score (area under precision-recall curve) — better for very imbalanced data.",
                    "Use roc_auc_score with cross_val_score: scoring='roc_auc'.",
                    "Find the threshold that achieves 95% recall (minimum) while maximizing precision.",
                    "Build a cost-benefit analysis: at each threshold, compute total cost using FN=$1000 and FP=$100.",
                    "Compare AUC of predict_proba vs predict_proba calibrated with CalibratedClassifierCV.",
                    "For a multi-class problem (3 classes): compute AUC with multi_class='ovr'.",
                    "Show how class_weight='balanced' changes AUC on an imbalanced dataset.",
                    "Compute bootstrapped confidence interval for AUC (sample with replacement 100 times).",
                    "Build a threshold selector widget: for a given cost structure, recommend the optimal threshold."
                ]
            }
        },
        {
            "id": "m4-l22",
            "title": "Saving & Loading Models — From Training to Production",
            "subtitle": "Pickle and joblib: persist your trained model for later use",
            "difficulty": "beginner",
            "business_context": "You trained a model that took 2 hours. You're not retraining it every time someone visits your website. Model serialization saves the trained model to disk so it can be loaded instantly in production — minutes later, or months later.",
            "concept": {
                "theory": "sklearn models (and full Pipelines) can be saved with Python's pickle module or joblib. joblib is preferred for sklearn models because it's more efficient with large numpy arrays. The saved file contains the model's learned parameters — all coefficients, splits, feature importances. Loading restores the model ready to predict.",
                "business_angle": "In any production ML system, training and serving are separate. You train once (expensive), save the model, and load it for every prediction request (cheap and fast). Model versioning is critical — you need to know which model version made which prediction.",
                "worked_example_intro": "We'll train a pipeline, save it with joblib, load it back, and verify predictions are identical.",
                "key_insight": "Save the entire Pipeline, not just the model. The scaler's fit parameters (mean, std from training data) are part of the model — if you only save the classifier, you'll forget to apply the same scaling in production and get garbage predictions."
            },
            "worked_example": """import numpy as np
import joblib
import pickle
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 600
X = np.column_stack([np.random.randn(n, 4)])
y = (X[:,0] + X[:,1] > 0.3).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train pipeline
pipe = Pipeline([('scaler', StandardScaler()), ('clf', RandomForestClassifier(100, random_state=42))])
pipe.fit(X_train, y_train)
original_preds = pipe.predict(X_test)
print(f"Original accuracy: {accuracy_score(y_test, original_preds):.1%}")

# Save with joblib (recommended for sklearn)
joblib.dump(pipe, '/tmp/model_v1.joblib')
print(f"Model saved ({os.path.getsize('/tmp/model_v1.joblib')/1024:.1f} KB)")

# Save with pickle (standard Python)
with open('/tmp/model_v1.pkl', 'wb') as f:
    pickle.dump(pipe, f)

# Load and verify predictions are identical
loaded_joblib = joblib.load('/tmp/model_v1.joblib')
loaded_preds  = loaded_joblib.predict(X_test)
print(f"Loaded accuracy:   {accuracy_score(y_test, loaded_preds):.1%}")
print(f"Predictions identical: {(original_preds == loaded_preds).all()}")

# Model metadata — always save with the model
metadata = {
    'model_version': '1.0',
    'training_date': '2024-03-01',
    'features': ['feature_0','feature_1','feature_2','feature_3'],
    'cv_score': 0.847,
    'training_rows': len(X_train),
}
import json
with open('/tmp/model_v1_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"\\nMetadata saved. Version: {metadata['model_version']}")
print("Features:", metadata['features'])""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "joblib.dump(model, 'model.joblib')  -- save",
                        "model = joblib.load('model.joblib')  -- load",
                        "pickle.dump(model, open('model.pkl','wb'))",
                        "model = pickle.load(open('model.pkl','rb'))"
                    ],
                    "notes": "joblib is faster than pickle for large numpy arrays. Save the full Pipeline, not just the classifier. Always version your models and save metadata."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why should you save the entire Pipeline rather than just the classifier?", "options": ["Pipelines are smaller than individual models","The scaler contains fitted parameters (mean/std from training) that must be applied to new data","Pipelines automatically version themselves","You can only load Pipelines, not individual models"], "answer": 1, "explanation": "The StandardScaler inside a Pipeline contains the mean and std computed from training data. If you save only the classifier, you lose the scaling parameters — in production, you'd need to know these exact values to correctly scale new inputs. Save the full Pipeline to get a self-contained prediction unit."},
                    {"type": "true_false", "question": "A model trained on Python 3.9 can always be loaded on Python 3.11 without issues.", "answer": False, "explanation": "Python pickle format is version-dependent, and sklearn models require the same sklearn version for loading. Best practice: always record the Python version, sklearn version, and numpy version in model metadata. Version mismatches can cause loading errors or silent incorrect predictions."},
                    {"type": "fill_blank", "question": "Load a saved model: model = joblib.___(\"model.joblib\")", "template": "model = joblib.___('model.joblib')", "answer": "load", "explanation": "joblib.load() deserializes the model from disk, reconstructing the full object with all fitted parameters. After loading, use model.predict() exactly as if you just trained it."}
                ]
            },
            "challenge": {
                "instructions": "Build a complete model versioning system: train two model versions (v1: LogReg, v2: RandomForest), save each with metadata JSON. Build a load_model(version) function. Compare predictions and accuracy between versions. Print a model registry showing both versions.",
                "starter_code": """import numpy as np
import joblib
import json
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 800
X = np.column_stack([np.random.randn(n, 5)])
y = (X[:,0] + X[:,1] - 0.5*X[:,2] > 0.2).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

MODEL_DIR = '/tmp/model_registry'
os.makedirs(MODEL_DIR, exist_ok=True)

def save_model(model, version, metadata):
    # Save model and metadata
    pass

def load_model(version):
    # Load model by version
    pass

# Train and save v1 (LogReg) and v2 (RandomForest)

print("=== Model Registry ===")
# Show both versions with their metadata
""",
                "tests": [{"type": "code_contains", "value": "joblib"}, {"type": "code_contains", "value": "json"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import joblib, json, os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
np.random.seed(42); n=800
X=np.column_stack([np.random.randn(n,5)]); y=(X[:,0]+X[:,1]-0.5*X[:,2]>0.2).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
MODEL_DIR='/tmp/model_registry'; os.makedirs(MODEL_DIR,exist_ok=True)
def save_model(model,version,meta):
    joblib.dump(model,f'{MODEL_DIR}/model_v{version}.joblib')
    with open(f'{MODEL_DIR}/model_v{version}_meta.json','w') as f: json.dump(meta,f)
def load_model(version):
    m=joblib.load(f'{MODEL_DIR}/model_v{version}.joblib')
    with open(f'{MODEL_DIR}/model_v{version}_meta.json') as f: meta=json.load(f)
    return m, meta
for v,(name,clf) in enumerate([('LogReg',LogisticRegression(max_iter=1000)),('RandomForest',RandomForestClassifier(100,random_state=42))],1):
    p=Pipeline([('s',StandardScaler()),('c',clf)]); cv=cross_val_score(p,X_train,y_train,cv=5).mean(); p.fit(X_train,y_train)
    save_model(p,v,{'name':name,'cv_score':round(cv,4),'test_acc':round(accuracy_score(y_test,p.predict(X_test)),4)})
print("=== Model Registry ===")
for v in [1,2]:
    _,meta=load_model(v); print(f"  v{v}: {meta['name']:<16} CV={meta['cv_score']:.1%}  Test={meta['test_acc']:.1%}")""",
                "challenge_variations": [
                    "Add model A/B testing: load both versions, split traffic 50/50, compare live accuracy.",
                    "Build a model rollback function: if new model's CV score drops > 2%, keep old version.",
                    "Add input validation to your loaded model: check feature count and dtypes before predict.",
                    "Save feature names with the model metadata and validate them at prediction time.",
                    "Build a simple Flask endpoint that loads the model and serves predictions via POST /predict.",
                    "Use mlflow.log_model() to track model experiments instead of manual saving.",
                    "Build a scheduled retraining script: if 30 days old, retrain and save new version.",
                    "Compress the model with joblib.dump(model, file, compress=3) — compare file sizes.",
                    "Save model with dill instead of pickle for models that contain lambda functions.",
                    "Build a model comparison report: load all saved versions and print a performance table."
                ]
            }
        },
        {
            "id": "m4-l23",
            "title": "Imbalanced Data — When Your Classes Are Unequal",
            "subtitle": "SMOTE, class weights, and threshold tuning for skewed datasets",
            "difficulty": "advanced",
            "business_context": "Fraud is 0.1% of transactions. Disease affects 2% of patients. Churn is 5% of customers. If you train a normal classifier on these datasets, it learns to predict 'not fraud' always — 99.9% accuracy, zero fraud caught. This is the imbalanced data problem.",
            "concept": {
                "theory": "Three approaches: (1) Class weights — tell the model 'penalize missing a positive 10x more': class_weight='balanced' or {0:1, 1:10}. (2) Resampling — SMOTE oversamples the minority class by creating synthetic examples; random undersampling removes majority class rows. (3) Threshold tuning — lower the prediction threshold from 0.5 to 0.2 to catch more positives.",
                "business_angle": "Imbalanced data is the norm in business ML: fraud, churn, disease, default. Always report F1, recall, and AUC — not accuracy — on imbalanced datasets. The business usually cares more about one error type (FN in fraud = missed fraud) so tune accordingly.",
                "worked_example_intro": "We'll compare: no correction, class_weight='balanced', SMOTE, and threshold tuning on a 5% positive dataset.",
                "key_insight": "Start with class_weight='balanced' — it's one parameter and often gives 80% of the benefit. SMOTE is more complex and sometimes hurts. Threshold tuning is always useful once you have a good probability model."
            },
            "worked_example": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score

np.random.seed(42)
n = 2000
X = np.column_stack([np.random.randn(n, 4)])
y = (np.random.rand(n) < 0.05).astype(int)  # 5% positive
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Class distribution: {y_train.sum()} positive / {(y_train==0).sum()} negative")

# 1. No correction — bad!
m1 = LogisticRegression(max_iter=1000)
m1.fit(X_train, y_train)
p1 = m1.predict(X_test)
print(f"\\nNo correction:    F1={f1_score(y_test,p1):.3f}")

# 2. class_weight='balanced'
m2 = LogisticRegression(class_weight='balanced', max_iter=1000)
m2.fit(X_train, y_train)
p2 = m2.predict(X_test)
print(f"Balanced weight:  F1={f1_score(y_test,p2):.3f}")

# 3. SMOTE (requires imbalanced-learn)
try:
    from imblearn.over_sampling import SMOTE
    sm = SMOTE(random_state=42)
    X_sm, y_sm = sm.fit_resample(X_train, y_train)
    m3 = LogisticRegression(max_iter=1000); m3.fit(X_sm, y_sm)
    p3 = m3.predict(X_test)
    print(f"SMOTE:            F1={f1_score(y_test,p3):.3f}")
except ImportError:
    print("(install imbalanced-learn for SMOTE)")

# 4. Threshold tuning
proba = m2.predict_proba(X_test)[:,1]
for thresh in [0.5, 0.3, 0.2, 0.1]:
    preds = (proba >= thresh).astype(int)
    print(f"Threshold={thresh}: F1={f1_score(y_test,preds):.3f}  recall={f1_score(y_test,preds,pos_label=1, average='binary', zero_division=0):.2f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "LogisticRegression(class_weight='balanced')  -- automatic weights",
                        "LogisticRegression(class_weight={0:1, 1:10})  -- manual weights",
                        "from imblearn.over_sampling import SMOTE",
                        "X_res, y_res = SMOTE().fit_resample(X_train, y_train)",
                        "preds = (proba >= 0.3).astype(int)  -- lower threshold"
                    ],
                    "notes": "Start with class_weight='balanced'. Evaluate with F1 and recall, not accuracy. SMOTE only applies to training data — never test."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "On a 99% negative / 1% positive dataset, a model predicting all-negative achieves what accuracy?", "options": ["50%","1%","99%","Cannot be determined"], "answer": 2, "explanation": "If 99% of examples are negative and the model always predicts negative, it's correct 99% of the time — 99% accuracy. This is why accuracy is useless for imbalanced datasets. Use F1, recall, precision, or AUC instead."},
                    {"type": "true_false", "question": "SMOTE should be applied to both training and test data.", "answer": False, "explanation": "SMOTE is a data augmentation technique for TRAINING ONLY. It creates synthetic minority examples to balance training. The test set must remain untouched and represent the real class distribution — applying SMOTE to test data would give falsely optimistic results."},
                    {"type": "fill_blank", "question": "Tell a model to weight the positive class 10x more: LogisticRegression(class_weight={0: 1, 1: ___})", "template": "LogisticRegression(class_weight={0: 1, 1: ___})", "answer": "10", "explanation": "class_weight={0:1, 1:10} makes misclassifying a positive example 10x more costly than a negative. This pushes the model to catch more positives (higher recall) at the cost of more false positives (lower precision)."}
                ]
            },
            "challenge": {
                "instructions": "Handle a severely imbalanced fraud dataset (2% fraud). Compare 4 approaches: default, balanced weights, SMOTE (if available), and threshold=0.3. Report precision, recall, F1 for each. Determine which is best if the cost of missing fraud is 20x the cost of a false alarm.",
                "starter_code": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

np.random.seed(42)
n = 3000
X = np.column_stack([np.random.randn(n, 5)])
y = (np.random.rand(n) < 0.02).astype(int)  # 2% fraud

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

print(f"{'Method':<22} {'Precision':>10} {'Recall':>8} {'F1':>8} {'Cost':>10}")
print("-" * 62)
# FN cost = 20, FP cost = 1
# For each method, compute cost = FN_count*20 + FP_count*1

# 1. Default (no correction)
# 2. class_weight='balanced'
# 3. Threshold=0.3 on balanced model
# 4. Try SMOTE if available
""",
                "tests": [{"type": "code_contains", "value": "class_weight"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
np.random.seed(42); n=3000
X=np.column_stack([np.random.randn(n,5)]); y=(np.random.rand(n)<0.02).astype(int)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)
print(f"{'Method':<22} {'Precision':>10} {'Recall':>8} {'F1':>8} {'Cost':>10}"); print("-"*62)
def report(name,preds,y_test):
    tn,fp,fn,tp=confusion_matrix(y_test,preds).ravel()
    cost=fn*20+fp*1
    print(f"{name:<22} {precision_score(y_test,preds,zero_division=0):>10.1%} {recall_score(y_test,preds,zero_division=0):>8.1%} {f1_score(y_test,preds,zero_division=0):>8.3f} {cost:>10}")
m1=LogisticRegression(max_iter=1000); m1.fit(X_train,y_train); report('Default',m1.predict(X_test),y_test)
m2=LogisticRegression(class_weight='balanced',max_iter=1000); m2.fit(X_train,y_train); report('Balanced',m2.predict(X_test),y_test)
p=m2.predict_proba(X_test)[:,1]; report('Threshold=0.3',(p>=0.3).astype(int),y_test)""",
                "challenge_variations": [
                    "Sweep thresholds from 0.1 to 0.9 and find the one minimizing total business cost.",
                    "Use NearMiss (undersampling) instead of SMOTE — compare results.",
                    "Apply imbalanced handling to a Random Forest: class_weight='balanced_subsample'.",
                    "Build a confusion matrix for each method and calculate FN/FP counts explicitly.",
                    "Combine SMOTE + class_weight and compare to each alone.",
                    "Generate a precision-recall curve and find the optimal threshold from it.",
                    "Use ensemble method BalancedBaggingClassifier from imbalanced-learn.",
                    "Test EasyEnsembleClassifier vs standard RF on a 1% positive dataset.",
                    "Build a cost-benefit calculator: for each threshold, compute expected profit/loss.",
                    "Simulate production: deploy threshold=0.3 model for 1000 transactions, count caught fraud vs false alarms."
                ]
            }
        },
        {
            "id": "m4-l24",
            "title": "Churn Prediction — A Complete End-to-End Business ML Problem",
            "subtitle": "Feature engineering, modeling, and business interpretation for real churn",
            "difficulty": "advanced",
            "business_context": "Acquiring a new customer costs 5-7x more than retaining an existing one. Predicting which customers will churn in the next 30 days lets you intervene before they leave. This lesson builds a complete churn prediction system from raw features to business recommendations.",
            "concept": {
                "theory": "Churn prediction is a binary classification problem with imbalanced classes (typically 5-15% churn). The full pipeline: feature engineering from raw usage data → preprocessing → model training with class balancing → threshold optimization → business output (risk scores, recommended interventions).",
                "business_angle": "The output of a churn model isn't just 'will churn' or 'won't churn' — it's a risk score (0-100) that enables prioritization. The top 100 highest-risk customers get a proactive call. The next 500 get a discount offer. The model's business value comes from the action it enables.",
                "worked_example_intro": "We'll build a full churn prediction pipeline with feature engineering, model training, risk scoring, and a customer intervention report.",
                "key_insight": "Feature engineering is usually more impactful than model choice. 'Days since last login', 'change in usage month-over-month', 'support ticket count' often predict churn better than demographic features. Domain knowledge creates better features than any algorithm."
            },
            "worked_example": """import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score

np.random.seed(42)
n = 2000

# Simulate customer usage data
df = pd.DataFrame({
    'customer_id':      range(1, n+1),
    'tenure_months':    np.random.randint(1, 60, n),
    'monthly_charge':   np.random.uniform(20, 120, n),
    'total_charges':    np.random.uniform(100, 8000, n),
    'support_calls_3m': np.random.randint(0, 8, n),
    'logins_30d':       np.random.randint(0, 30, n),
    'logins_60d':       np.random.randint(0, 60, n),
    'features_used':    np.random.randint(1, 10, n),
    'contract_type':    np.random.choice(['monthly','annual','biannual'], n, p=[0.5,0.3,0.2]),
    'payment_method':   np.random.choice(['auto','manual','credit'], n),
})

# Feature engineering
df['usage_trend']       = df['logins_30d'] - df['logins_60d'] / 2  # MoM usage change
df['charge_per_login']  = df['monthly_charge'] / (df['logins_30d'] + 0.1)
df['support_rate']      = df['support_calls_3m'] / (df['tenure_months'] + 1)
df['contract_monthly']  = (df['contract_type'] == 'monthly').astype(int)

# Churn label (domain-driven: high support + low login + monthly contract)
df['churn'] = (
    (df['support_calls_3m'] > 3) |
    ((df['logins_30d'] < 3) & (df['contract_monthly'] == 1)) |
    ((df['tenure_months'] < 6) & (df['monthly_charge'] > 80))
).astype(int)

print(f"Churn rate: {df['churn'].mean():.1%}")

features = ['tenure_months','monthly_charge','support_calls_3m','logins_30d',
            'features_used','usage_trend','charge_per_login','support_rate','contract_monthly']
X = df[features]
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42)),
])
pipe.fit(X_train, y_train)

print(f"AUC: {roc_auc_score(y_test, pipe.predict_proba(X_test)[:,1]):.4f}")
print(f"CV AUC: {cross_val_score(pipe, X, y, cv=5, scoring='roc_auc').mean():.4f}")
print("\\nClassification Report:")
print(classification_report(y_test, pipe.predict(X_test), target_names=['Retained','Churned']))

# Business output: churn risk scores
df_test = X_test.copy()
df_test['churn_prob']  = pipe.predict_proba(X_test)[:,1]
df_test['risk_score']  = (df_test['churn_prob'] * 100).round(1)
df_test['segment']     = pd.cut(df_test['churn_prob'], bins=[0,.3,.6,.8,1],
                                labels=['Low','Medium','High','Critical'])
print("\\nIntervention Segments:")
print(df_test['segment'].value_counts())
print("\\nTop 5 highest-risk customers:")
print(df_test.nlargest(5, 'churn_prob')[['tenure_months','support_calls_3m','logins_30d','risk_score','segment']])""",
            "quiz": {
                "reference": {
                    "key_syntax": ["Full pipeline: feature engineering → scaling → GBM → threshold tuning", "proba = pipe.predict_proba(X)[:,1]", "pd.cut(proba, bins=[0,.3,.6,1], labels=['Low','Med','High'])", "cross_val_score with scoring='roc_auc' for imbalanced data"],
                    "notes": "Feature engineering drives most of churn model improvement. Domain knowledge matters more than model complexity."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why output a churn risk score (0-100) rather than just 'will churn'/'won't churn'?", "options": ["Risk scores are easier to compute","Risk scores enable prioritization — top 100 highest risk get personal calls; next 500 get email offers","Risk scores avoid regulatory issues","Risk scores are required by sklearn"], "answer": 1, "explanation": "A binary prediction (churn/no churn) forces a single threshold on all customers. A continuous risk score lets the business apply tiered interventions: personalized calls for Critical, automated discounts for High, email nurture for Medium. Different interventions have different costs."},
                    {"type": "true_false", "question": "Engineered features (like 'usage_trend' or 'support_rate') usually matter more than raw features for churn.", "answer": True, "explanation": "Raw features like 'logins_30d' and 'logins_60d' don't directly show the trend. But 'logins_30d - logins_60d/2' shows declining engagement — a strong churn signal. Domain-driven feature engineering transforms raw data into business-meaningful signals that models can use more effectively."},
                    {"type": "fill_blank", "question": "Segment customers by risk level: df['segment'] = pd.___(df['prob'], bins=[0,.3,.6,1], labels=['Low','Med','High'])", "template": "df['segment'] = pd.___(df['prob'], bins=[0,.3,.6,1], labels=['Low','Med','High'])", "answer": "cut", "explanation": "pd.cut() bins continuous probability scores into labeled segments. This transforms a 0-1 probability into actionable business segments. The bins define the threshold boundaries for each segment."}
                ]
            },
            "challenge": {
                "instructions": "Build a complete churn prediction system for a telecom company. Include: feature engineering (usage trends, support rate), Pipeline with GBM, threshold optimization for recall ≥ 70%, customer segmentation, and a business recommendation report showing which customers to contact and why.",
                "starter_code": """import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score, recall_score, classification_report

np.random.seed(7)
n = 3000
df = pd.DataFrame({
    'customer_id': range(n),
    'months_active': np.random.randint(1, 72, n),
    'monthly_bill':  np.random.uniform(25, 150, n),
    'calls_to_support': np.random.randint(0, 10, n),
    'app_logins_last30': np.random.randint(0, 40, n),
    'app_logins_prev30': np.random.randint(0, 40, n),
    'plan': np.random.choice(['basic','standard','premium'], n),
    'has_autopay': np.random.randint(0, 2, n),
})

# TODO: Engineer features (usage_drop, support_intensity, etc.)

# TODO: Create churn label (your logic)

# TODO: Build and train Pipeline

# TODO: Find threshold achieving recall >= 70%

# TODO: Generate risk segments and intervention report
print("=== Churn Intervention Report ===")
""",
                "tests": [{"type": "code_contains", "value": "Pipeline"}, {"type": "code_contains", "value": "predict_proba"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score, recall_score
np.random.seed(7); n=3000
df=pd.DataFrame({'customer_id':range(n),'months_active':np.random.randint(1,72,n),'monthly_bill':np.random.uniform(25,150,n),'calls_to_support':np.random.randint(0,10,n),'app_logins_last30':np.random.randint(0,40,n),'app_logins_prev30':np.random.randint(0,40,n),'plan':np.random.choice(['basic','standard','premium'],n),'has_autopay':np.random.randint(0,2,n)})
df['usage_drop']=df['app_logins_prev30']-df['app_logins_last30']
df['support_intensity']=df['calls_to_support']/(df['months_active']+1)
df['is_basic']=(df['plan']=='basic').astype(int)
df['churn']=((df['calls_to_support']>4)|((df['app_logins_last30']<3)&(df['is_basic']==1))|((df['usage_drop']>10)&(df['months_active']<12))).astype(int)
feats=['months_active','monthly_bill','calls_to_support','app_logins_last30','usage_drop','support_intensity','is_basic','has_autopay']
X=df[feats]; y=df['churn']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)
pipe=Pipeline([('s',StandardScaler()),('m',GradientBoostingClassifier(100,random_state=42))]); pipe.fit(X_train,y_train)
print(f"AUC: {roc_auc_score(y_test,pipe.predict_proba(X_test)[:,1]):.4f}")
proba=pipe.predict_proba(X_test)[:,1]
for t in [0.5,0.4,0.3,0.2]:
    if recall_score(y_test,(proba>=t).astype(int),zero_division=0)>=0.70: best_t=t; break
print(f"Optimal threshold: {best_t}")
df_out=X_test.copy(); df_out['prob']=proba; df_out['risk']=pd.cut(proba,[0,.3,.6,.8,1],labels=['Low','Medium','High','Critical'])
print("=== Churn Intervention Report ===")
for seg in ['Critical','High','Medium']:
    g=df_out[df_out['risk']==seg]; print(f"  {seg}: {len(g)} customers — avg prob={g['prob'].mean():.0%}")""",
                "challenge_variations": [
                    "Add product revenue to the model: weight high-value customers more in the cost function.",
                    "Build a cohort analysis: does churn rate differ by months_active cohort?",
                    "Add SHAP values to explain individual churn predictions.",
                    "Build a retention ROI calculator: intervention_cost vs customer_lifetime_value.",
                    "Create a churn dashboard with a text-based table showing segment counts and average risk.",
                    "Compare GBM vs XGBoost (if installed) on the churn dataset.",
                    "Add temporal validation: train on months 1-9, test on months 10-12.",
                    "Build a personalized recommendation: for each at-risk customer, print the top risk factor.",
                    "Simulate the A/B test: intervention group (model-targeted) vs control group — estimate lift.",
                    "Build a monthly retraining scheduler that retrains the model when new data arrives."
                ]
            }
        },
        {
            "id": "m4-l25",
            "title": "Deploying ML Models — From Notebook to Production",
            "subtitle": "Serve your model via a REST API so any app can use it",
            "difficulty": "advanced",
            "business_context": "You trained the perfect model. Now what? A model in a Jupyter notebook helps no one. Deployment means packaging your model as a service other systems can call — a web API that accepts customer data and returns predictions in milliseconds.",
            "concept": {
                "theory": "The standard ML deployment pattern: (1) train and save model, (2) build a REST API (Flask/FastAPI) that loads the model on startup, (3) define a /predict endpoint that accepts JSON input, runs the pipeline, and returns prediction + confidence. The model runs in a server process, handling hundreds of requests per second.",
                "business_angle": "A deployed model directly drives business outcomes: approve/deny a loan application in real-time, flag a transaction as fraud before it processes, personalize a product recommendation as the page loads. The gap between 'a trained model' and 'a deployed model' is where most academic ML falls short.",
                "worked_example_intro": "We'll build a complete Flask API that serves our churn prediction model, with input validation, error handling, and response formatting.",
                "key_insight": "The deployment isn't the end — it's the beginning of the model lifecycle. Monitor prediction distributions, track model drift (when the real world changes from training data), set up retraining triggers. A model that was 85% accurate at launch can degrade to 70% within months if not monitored."
            },
            "worked_example": """import numpy as np
import joblib
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# Step 1: Train and save the model
np.random.seed(42)
n = 1000
X = np.column_stack([np.random.randn(n, 5)])
y = (X[:,0] + X[:,1] > 0.3).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([('scaler', StandardScaler()), ('model', GradientBoostingClassifier(100, random_state=42))])
pipe.fit(X_train, y_train)
joblib.dump(pipe, '/tmp/churn_model.joblib')
print("Model saved to /tmp/churn_model.joblib")

# Step 2: Flask API (conceptual — runs if Flask installed)
flask_app_code = '''
from flask import Flask, request, jsonify
import joblib, numpy as np

app = Flask(__name__)
model = joblib.load('/tmp/churn_model.joblib')  # load once at startup
FEATURES = ['tenure', 'bill', 'support_calls', 'logins', 'usage_trend']

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_version': '1.0'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Validate input
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    # Prepare features
    X = np.array([[data[f] for f in FEATURES]])
    prob = float(model.predict_proba(X)[0, 1])
    return jsonify({
        'churn_probability': round(prob, 4),
        'risk_segment': 'High' if prob > 0.6 else 'Medium' if prob > 0.3 else 'Low',
        'should_intervene': prob > 0.5,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
'''

print("\\nFlask API code:")
print(flask_app_code)

# Step 3: Simulate prediction requests
loaded = joblib.load('/tmp/churn_model.joblib')
test_customers = [
    {'tenure':2, 'bill':95, 'support_calls':6, 'logins':2, 'usage_trend':-8},
    {'tenure':36, 'bill':45, 'support_calls':0, 'logins':20, 'usage_trend':3},
]
print("\\nSimulated API Predictions:")
for i, cust in enumerate(test_customers, 1):
    X = np.array([[cust[k] for k in ['tenure','bill','support_calls','logins','usage_trend']]])
    prob = float(loaded.predict_proba(X)[0,1])
    segment = 'High' if prob > 0.6 else 'Medium' if prob > 0.3 else 'Low'
    print(f"  Customer {i}: prob={prob:.3f}  segment={segment}  intervene={'YES' if prob>0.5 else 'no'}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "joblib.dump(pipe, 'model.joblib')  -- save pipeline",
                        "model = joblib.load('model.joblib')  -- load once at startup",
                        "prob = model.predict_proba(X)[0,1]  -- positive class probability",
                        "Flask: @app.route('/predict', methods=['POST'])"
                    ],
                    "notes": "Load the model once at server startup — not on every request. Validate input fields before predicting. Return probability + segment + action, not just 'yes/no'."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Why load the model once at server startup rather than on each request?", "options": ["Models can only be loaded once","Loading a model takes milliseconds to seconds — loading per request would be too slow","Flask requires it","You can't reload a saved model"], "answer": 1, "explanation": "Model loading deserializes a potentially large file and reconstructs all parameters in memory. This takes 0.1-5 seconds depending on model size. Loading once at startup means every prediction request gets sub-millisecond inference. Loading per request would make a production API unusably slow."},
                    {"type": "true_false", "question": "Model monitoring is important after deployment because real-world data distributions can change over time.", "answer": True, "explanation": "Model drift: the statistical properties of input data change over time (customer behavior evolves, economy shifts, fraud tactics change). A model trained in January may perform significantly worse in December. Monitoring prediction distributions and periodically evaluating against labeled data catches drift before it causes business damage."},
                    {"type": "fill_blank", "question": "To serve predictions via a POST endpoint in Flask: @app.route('/predict', methods=___)", "template": "@app.route('/predict', methods=___)", "answer": "['POST']", "explanation": "REST conventions: POST for creating/submitting data (sending features for prediction). GET for retrieving data (model health status). The methods parameter takes a list of allowed HTTP methods."}
                ]
            },
            "challenge": {
                "instructions": "Build a complete mock deployment system: (1) train and save a loan approval model, (2) write a prediction function that validates input, runs the model, and returns a structured response with probability, decision, and reason, (3) test with 5 customer profiles including edge cases (missing data, out-of-range values).",
                "starter_code": """import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Train and save model
np.random.seed(42); n=1000
X = np.column_stack([np.random.randn(n, 4)])
y = (X[:,0] + X[:,1] > 0.3).astype(int)
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
pipe = Pipeline([('s', StandardScaler()), ('m', RandomForestClassifier(100, random_state=42))])
pipe.fit(X_train, y_train)
joblib.dump(pipe, '/tmp/loan_model.joblib')

FEATURES = ['income_k', 'credit_score', 'debt_ratio', 'employment_yrs']
RANGES = {'income_k': (10,500), 'credit_score': (300,850), 'debt_ratio': (0,1), 'employment_yrs': (0,40)}

def predict_loan(data: dict) -> dict:
    # Validate: check all features present
    # Validate: check ranges using RANGES
    # Run model: return {'approved': bool, 'probability': float, 'confidence': str, 'reason': str}
    pass

# Test 5 customers including one with missing field and one with out-of-range value
test_cases = [
    {'income_k':85, 'credit_score':720, 'debt_ratio':0.3, 'employment_yrs':5},
    {'income_k':30, 'credit_score':520, 'debt_ratio':0.7, 'employment_yrs':1},
    {'income_k':120, 'credit_score':800, 'employment_yrs':10},       # missing debt_ratio
    {'income_k':200, 'credit_score':950, 'debt_ratio':0.2, 'employment_yrs':15}, # credit > 850
    {'income_k':65, 'credit_score':670, 'debt_ratio':0.4, 'employment_yrs':8},
]
for i, case in enumerate(test_cases, 1):
    result = predict_loan(case)
    print(f"Customer {i}: {result}")
""",
                "tests": [{"type": "code_contains", "value": "joblib"}, {"type": "code_contains", "value": "predict_proba"}, {"type": "runs_without_error"}],
                "solution": """import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
np.random.seed(42); n=1000
X=np.column_stack([np.random.randn(n,4)]); y=(X[:,0]+X[:,1]>0.3).astype(int)
X_train,_,y_train,_=train_test_split(X,y,test_size=0.2,random_state=42)
pipe=Pipeline([('s',StandardScaler()),('m',RandomForestClassifier(100,random_state=42))]); pipe.fit(X_train,y_train); joblib.dump(pipe,'/tmp/loan_model.joblib')
model=joblib.load('/tmp/loan_model.joblib')
FEATURES=['income_k','credit_score','debt_ratio','employment_yrs']
RANGES={'income_k':(10,500),'credit_score':(300,850),'debt_ratio':(0,1),'employment_yrs':(0,40)}
def predict_loan(data):
    missing=[f for f in FEATURES if f not in data]
    if missing: return {'error':f'Missing: {missing}'}
    for f,(lo,hi) in RANGES.items():
        if not lo<=data[f]<=hi: return {'error':f'{f}={data[f]} out of range [{lo},{hi}]'}
    X=np.array([[data[f] for f in FEATURES]]); prob=float(model.predict_proba(X)[0,1])
    approved=prob>0.5; conf='High' if prob>0.75 or prob<0.25 else 'Medium'
    reason='Low risk profile' if approved else 'High debt ratio or low credit'
    return {'approved':approved,'probability':round(prob,3),'confidence':conf,'reason':reason}
for i,case in enumerate([{'income_k':85,'credit_score':720,'debt_ratio':0.3,'employment_yrs':5},{'income_k':30,'credit_score':520,'debt_ratio':0.7,'employment_yrs':1},{'income_k':120,'credit_score':800,'employment_yrs':10},{'income_k':200,'credit_score':950,'debt_ratio':0.2,'employment_yrs':15},{'income_k':65,'credit_score':670,'debt_ratio':0.4,'employment_yrs':8}],1):
    print(f"Customer {i}: {predict_loan(case)}")""",
                "challenge_variations": [
                    "Add request logging: save every prediction request with timestamp, input, and output to a SQLite database.",
                    "Add model drift detection: alert if the average predicted probability shifts more than 10% from training baseline.",
                    "Build A/B routing: route 10% of requests to model_v2, 90% to model_v1.",
                    "Add async prediction using asyncio for handling multiple simultaneous requests.",
                    "Deploy the Flask app in a Docker container (write the Dockerfile).",
                    "Add API key authentication: reject requests without a valid key in the header.",
                    "Implement prediction caching: if the exact same input was seen recently, return the cached result.",
                    "Build a monitoring endpoint /metrics that shows: total predictions, avg probability, error rate.",
                    "Add batch prediction endpoint: accept a list of customers and return predictions for all.",
                    "Implement graceful degradation: if model fails to load, return a rule-based fallback prediction."
                ]
            }
        },
        {
            "id": "m4-capstone",
            "title": "Module 4 Capstone — Build a Complete ML System",
            "subtitle": "End-to-end: feature engineering, model selection, tuning, evaluation, and deployment",
            "difficulty": "advanced",
            "business_context": "You've been hired by a bank to build their loan default prediction model. Using customer data, build the best possible model, evaluate it rigorously, compare alternatives, tune it, and present the results as a business report — including ROI estimate.",
            "concept": {
                "theory": "This capstone integrates all Module 4 skills: EDA, feature engineering, multiple model comparison, cross-validation, class imbalance handling, hyperparameter tuning, ROC-AUC evaluation, confusion matrix analysis, Pipeline, model saving, and business interpretation.",
                "business_angle": "The deliverable isn't code — it's a business recommendation: 'Deploy Model X. At threshold 0.35, it catches 78% of defaults while approving 71% of good loans. Estimated annual savings: $2.3M in prevented defaults.' This is how ML creates business value.",
                "worked_example_intro": "Run the full capstone pipeline from raw data to business report. Every section is a skill from this module.",
                "key_insight": "The end-to-end workflow is: explore → engineer features → build baseline → compare models → tune best → evaluate rigorously → interpret for business → deploy. Each step builds on the last."
            },
            "worked_example": """import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.metrics import (roc_auc_score, f1_score, classification_report,
                              confusion_matrix, roc_curve)

np.random.seed(42)
n = 3000

# === 1. GENERATE DATA ===
df = pd.DataFrame({
    'age':           np.random.randint(18, 70, n),
    'income':        np.random.uniform(20000, 150000, n),
    'credit_score':  np.random.randint(450, 850, n),
    'debt_ratio':    np.random.uniform(0.1, 0.8, n),
    'loan_amount':   np.random.uniform(5000, 100000, n),
    'employment_yr': np.random.randint(0, 30, n),
    'missed_pmts':   np.random.randint(0, 5, n),
    'loan_purpose':  np.random.choice(['home','car','personal','business'], n),
})

# Feature engineering
df['income_to_loan']  = df['income'] / df['loan_amount']
df['monthly_burden']  = df['loan_amount'] * 0.05 / (df['income'] / 12)
df['credit_risk_flag']= (df['credit_score'] < 600).astype(int)
df['purpose_personal']= (df['loan_purpose'] == 'personal').astype(int)

# Default label (domain-driven)
df['default'] = (
    (df['credit_score'] < 580) |
    ((df['debt_ratio'] > 0.6) & (df['income'] < 40000)) |
    (df['missed_pmts'] > 2) |
    ((df['loan_amount'] > df['income']) & (df['employment_yr'] < 2))
).astype(int)

print(f"Default rate: {df['default'].mean():.1%}")

features = ['age','income','credit_score','debt_ratio','loan_amount','employment_yr',
            'missed_pmts','income_to_loan','monthly_burden','credit_risk_flag']
X = df[features]
y = df['default']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# === 2. MODEL COMPARISON ===
models = {
    'Decision Tree':   DecisionTreeClassifier(max_depth=5, class_weight='balanced', random_state=42),
    'Logistic Reg':    LogisticRegression(class_weight='balanced', max_iter=1000),
    'Random Forest':   RandomForestClassifier(100, class_weight='balanced', random_state=42),
    'Gradient Boost':  GradientBoostingClassifier(100, random_state=42),
}
skf = StratifiedKFold(5, shuffle=True, random_state=42)
print("\\n=== Model Comparison (5-fold Stratified CV) ===")
print(f"{'Model':<18} {'AUC':>8} {'F1':>8}")
best_auc, best_model = 0, None
for name, m in models.items():
    pipe = Pipeline([('s', StandardScaler()), ('m', m)])
    auc = cross_val_score(pipe, X, y, cv=skf, scoring='roc_auc').mean()
    f1  = cross_val_score(pipe, X, y, cv=skf, scoring='f1').mean()
    print(f"  {name:<18} {auc:>8.4f} {f1:>8.4f}")
    if auc > best_auc: best_auc, best_model = auc, (name, m)

# === 3. TUNE BEST MODEL ===
print(f"\\nTuning {best_model[0]}...")
best_pipe = Pipeline([('s', StandardScaler()), ('m', best_model[1])])
if 'Random Forest' in best_model[0]:
    param_grid = {'m__n_estimators':[100,200], 'm__max_depth':[5,10,None], 'm__min_samples_leaf':[1,5]}
elif 'Gradient' in best_model[0]:
    param_grid = {'m__n_estimators':[100,200], 'm__max_depth':[3,5], 'm__learning_rate':[0.05,0.1]}
else:
    param_grid = {}
if param_grid:
    gs = GridSearchCV(best_pipe, param_grid, cv=skf, scoring='roc_auc', n_jobs=-1)
    gs.fit(X_train, y_train)
    best_fitted = gs.best_estimator_
    print(f"Best params: {gs.best_params_}")
else:
    best_fitted = best_pipe.fit(X_train, y_train)

# === 4. EVALUATE ===
proba = best_fitted.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test, proba)
fpr, tpr, thresholds = roc_curve(y_test, proba)
j = tpr - fpr
opt_thresh = thresholds[j.argmax()]
preds = (proba >= opt_thresh).astype(int)
tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

print(f"\\n=== Final Model Evaluation ===")
print(f"AUC: {auc:.4f} | Optimal threshold: {opt_thresh:.3f}")
print(f"Recall (caught defaults): {tp/(tp+fn):.1%}")
print(f"Precision: {tp/(tp+fp):.1%}")
print(f"False approval rate: {fp/(fp+tn):.1%}")

# === 5. BUSINESS REPORT ===
avg_loss_per_default = 15000
annual_defaults = 500
print(f"\\n=== Business Report ===")
caught = tp / (tp + fn)
print(f"At threshold {opt_thresh:.2f}:")
print(f"  Defaults caught per 100: {caught*100:.0f}")
print(f"  False declines per 100 good loans: {fp/(fp+tn)*100:.1f}")
print(f"  Estimated annual savings: ${caught * annual_defaults * avg_loss_per_default:,.0f}")
print(f"  False decline cost (lost revenue): ${fp/(fp+tn) * 1000 * 2000:,.0f} (est.)")

# Save
joblib.dump(best_fitted, '/tmp/loan_default_model.joblib')
print(f"\\nModel saved. Deployment recommendation: {best_model[0]}")""",
            "quiz": {
                "reference": {
                    "key_syntax": ["Full pipeline: EDA → feature eng → compare → tune → evaluate → report → save", "StratifiedKFold for imbalanced evaluation", "Youden's J for optimal threshold", "Business ROI = recall × defaults × avg_loss"],
                    "notes": "The business report is as important as the model. Translate recall into dollars to justify deployment."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "In the capstone workflow, at which step do you look at test set metrics for the first time?", "options": ["During model comparison","During hyperparameter tuning","After tuning, for the final evaluation only","As soon as you split the data"], "answer": 2, "explanation": "The test set is used exactly ONCE — for the final evaluation report. All model comparison and tuning uses cross-validation on the training data only. Looking at test metrics during tuning would contaminate the results (you'd overfit to the test set)."},
                    {"type": "true_false", "question": "A model with AUC=0.91 but recall=0.40 may be unacceptable for fraud/default detection.", "answer": True, "explanation": "High AUC means the model ranks positives higher than negatives on average. But a recall of 40% means 60% of actual defaults slip through undetected. If the business defines success as 'catch at least 70% of defaults,' a model with 40% recall fails, regardless of AUC."},
                    {"type": "fill_blank", "question": "To find the threshold that maximizes (TPR - FPR): j = tpr - fpr; opt_thresh = thresholds[j.___()]", "template": "j = tpr - fpr; opt_thresh = thresholds[j.___()]", "answer": "argmax", "explanation": "argmax() returns the index of the maximum value. j = tpr - fpr is Youden's J statistic — it peaks at the threshold where you gain the most true positives relative to false positives. thresholds[j.argmax()] gives the actual probability cutoff."}
                ]
            },
            "challenge": {
                "instructions": "Run the full capstone above. Then extend it with: (1) Feature importance report from the best model, (2) A prediction function for a new loan application with full validation, (3) Calculate the minimum recall needed to break even given: avg_loss=$20k, intervention_cost=$200 per reviewed application, 10,000 loans/year with 5% default rate.",
                "starter_code": """# Run the full capstone code above, then add:

print("\\n=== Feature Importance Report ===")
# Extract and print top 5 most important features

print("\\n=== New Loan Application Prediction ===")
def predict_application(model, applicant_data):
    # Validate input, compute engineered features, predict
    pass

# Test with a borderline applicant
applicant = {
    'age': 35, 'income': 55000, 'credit_score': 630,
    'debt_ratio': 0.45, 'loan_amount': 25000, 'employment_yr': 4, 'missed_pmts': 1
}
print(predict_application(best_fitted, applicant))

print("\\n=== Break-Even Analysis ===")
# At what recall does intervention_cost = losses_prevented?
# Show the math
""",
                "tests": [{"type": "code_contains", "value": "roc_auc_score"}, {"type": "code_contains", "value": "confusion_matrix"}, {"type": "runs_without_error"}],
                "solution": """# After capstone: feature importance
if hasattr(best_fitted['m'], 'feature_importances_'):
    fi=pd.Series(best_fitted['m'].feature_importances_,index=features).sort_values(ascending=False)
    print("\\n=== Feature Importance Report ===")
    for f,v in fi.head(5).items(): print(f"  {f}: {v:.3f}")
# New prediction
def predict_application(model, d):
    d['income_to_loan']=d['income']/d['loan_amount']
    d['monthly_burden']=d['loan_amount']*0.05/(d['income']/12)
    d['credit_risk_flag']=int(d['credit_score']<600)
    feats=['age','income','credit_score','debt_ratio','loan_amount','employment_yr','missed_pmts','income_to_loan','monthly_burden','credit_risk_flag']
    X=np.array([[d[f] for f in feats]])
    prob=float(model.predict_proba(X)[0,1])
    return {'default_prob':round(prob,3),'decision':'DECLINE' if prob>opt_thresh else 'APPROVE','risk':'High' if prob>0.6 else 'Low'}
applicant={'age':35,'income':55000,'credit_score':630,'debt_ratio':0.45,'loan_amount':25000,'employment_yr':4,'missed_pmts':1}
print(predict_application(best_fitted, applicant))
print("\\n=== Break-Even Analysis ===")
N=10000; default_rate=0.05; avg_loss=20000; cost_per_review=200
defaults=N*default_rate; loss_if_none=defaults*avg_loss
for recall in [0.3,0.5,0.7,0.9]:
    reviews=N*(default_rate*recall+(1-default_rate)*0.2); savings=recall*defaults*avg_loss; costs=reviews*200; net=savings-costs
    print(f"  Recall {recall:.0%}: savings=${savings:,.0f}  review_cost=${costs:,.0f}  NET=${net:,.0f}")""",
                "challenge_variations": [
                    "Add SHAP values to explain why each loan application was approved or declined.",
                    "Build a fairness analysis: compare default rates and approval rates across age groups.",
                    "Implement model monitoring: simulate 6 months of drift and detect when performance degrades.",
                    "Add a second target: build a 'default severity' regression model predicting expected loss given default.",
                    "Compare AutoML (TPOT or auto-sklearn) performance against your manually tuned model.",
                    "Build a model card documenting: intended use, training data, performance, limitations.",
                    "Add temporal validation: train on 70% earliest records, validate on middle 15%, test on latest 15%.",
                    "Implement ensemble stacking: use predictions from RF+GBM+LogReg as features for a meta-learner.",
                    "Create a full MLOps simulation: training script, saved model, served API, monitoring dashboard.",
                    "Present the capstone as a business executive summary (printed text): problem, model, results, recommendation."
                ]
            }
        }
    ]
}
