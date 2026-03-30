MODULE_2 = {
    "id": "module2",
    "title": "Data Analytics with Python",
    "description": "Learn to work with real data using NumPy and Pandas — the core libraries of every data scientist's toolkit.",
    "course": "MSBX 5415 · Data Analytics w/AI",
    "order": 2,
    "locked": True,
    "lessons": [
        {
            "id": "m2-l1",
            "title": "NumPy — Fast Number Crunching",
            "order": 1,
            "duration_min": 20,
            "concept": """**NumPy** (Numerical Python) is the foundation of data science in Python. It provides fast, efficient arrays for numerical computation.

```python
import numpy as np

# Create an array
scores = np.array([85, 92, 78, 96, 88])

# Fast math operations (no loops needed!)
print(scores.mean())   # 87.8
print(scores.std())    # 6.18 (standard deviation)
print(scores.min())    # 78
print(scores.max())    # 96
print(scores.sum())    # 439
```

**Why NumPy over plain lists?**
- 50x faster for large datasets
- Built-in statistical functions
- Foundation of Pandas, scikit-learn, and TensorFlow

**Array creation:**
```python
np.zeros(5)           # [0. 0. 0. 0. 0.]
np.ones(5)            # [1. 1. 1. 1. 1.]
np.arange(0, 10, 2)  # [0 2 4 6 8]
np.linspace(0, 1, 5) # [0. 0.25 0.5 0.75 1.]
```

**Broadcasting — math on whole arrays:**
```python
scores = np.array([85, 92, 78])
curved = scores + 5   # [90, 97, 83] — adds 5 to every element
pct = scores / 100    # [0.85, 0.92, 0.78]
```

**Boolean indexing — filter arrays:**
```python
high = scores[scores >= 90]  # [92, 96]
```""",
            "reference": {
                "key_syntax": [
                    "import numpy as np",
                    "np.array([...])",
                    "arr.mean() .std() .min() .max()",
                    "arr[arr > value]  # boolean filter",
                    "np.zeros(n) np.ones(n) np.arange()"
                ],
                "notes": "NumPy arrays must contain one data type (all numbers or all strings, not mixed)."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does np.array([1,2,3]).mean() return?",
                    "options": ["1", "2.0", "3", "6"],
                    "answer": 1,
                    "explanation": "The mean (average) of [1, 2, 3] is (1+2+3)/3 = 2.0."
                },
                {
                    "type": "fill_blank",
                    "question": "Import NumPy using the standard alias",
                    "template": "import numpy ___ np",
                    "answer": "as",
                    "explanation": "'as' creates an alias. 'import numpy as np' lets you write np.array() instead of numpy.array()."
                },
                {
                    "type": "true_false",
                    "question": "arr + 10 adds 10 to every element in a NumPy array.",
                    "answer": True,
                    "explanation": "This is called broadcasting — NumPy applies operations element-wise across the entire array."
                }
            ],
            "challenge": {
                "instructions": "Create a NumPy array of 8 exam scores. Then print: the mean, standard deviation (std), the highest score, the lowest score, and finally a filtered array containing only scores above 80.",
                "starter_code": "import numpy as np\n\nscores = np.array([72, 95, 88, 61, 79, 93, 85, 70])\n\n# Print mean, std, max, min\n\n# Print scores above 80\n",
                "tests": [
                    {"type": "output_contains", "value": "80."},
                    {"type": "code_contains", "value": "np.array"}
                ],
                "solution": "import numpy as np\nscores = np.array([72, 95, 88, 61, 79, 93, 85, 70])\nprint('Mean:', scores.mean())\nprint('Std:', scores.std())\nprint('Max:', scores.max())\nprint('Min:', scores.min())\nprint('Above 80:', scores[scores > 80])"
            }
        },
        {
            "id": "m2-l2",
            "title": "Pandas — DataFrames for Real Data",
            "order": 2,
            "duration_min": 25,
            "concept": """**Pandas** is the most important library for data analysis. It gives you the **DataFrame** — a table with rows and columns, like Excel but in Python.

```python
import pandas as pd

# Create a DataFrame from a dictionary
data = {
    "name":   ["Alice", "Bob", "Carol", "Dave"],
    "score":  [92, 78, 95, 81],
    "grade":  ["A", "C", "A", "B"],
    "passed": [True, True, True, True]
}
df = pd.DataFrame(data)
print(df)
```

Output:
```
    name  score grade  passed
0  Alice     92     A    True
1    Bob     78     C    True
2  Carol     95     A    True
3   Dave     81     B    True
```

**Exploring a DataFrame:**
```python
df.head()        # First 5 rows
df.tail()        # Last 5 rows
df.shape         # (rows, columns)
df.columns       # Column names
df.dtypes        # Data types per column
df.describe()    # Summary stats (mean, std, min, max)
df.info()        # Overview + memory usage
```

**Accessing data:**
```python
df["score"]              # Column as Series
df[["name", "score"]]    # Multiple columns
df.iloc[0]               # Row by index number
df.loc[df["score"] > 80] # Rows where score > 80
```""",
            "reference": {
                "key_syntax": [
                    "import pandas as pd",
                    "pd.DataFrame(dict)",
                    "df.head() / .tail() / .shape",
                    'df["column"]',
                    'df.loc[df["col"] > value]'
                ],
                "notes": "df.describe() is your best friend for a quick overview of numerical columns."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does df.shape return?",
                    "options": [
                        "The column names",
                        "A tuple of (rows, columns)",
                        "The data types",
                        "The first 5 rows"
                    ],
                    "answer": 1,
                    "explanation": "df.shape returns a tuple (number_of_rows, number_of_columns)."
                },
                {
                    "type": "fill_blank",
                    "question": "Filter a DataFrame to rows where 'age' is greater than 30",
                    "template": 'df.___(df["age"] > 30)',
                    "answer": "loc",
                    "explanation": "df.loc[] is used for label-based filtering. df.loc[df['age'] > 30] returns rows where the condition is True."
                },
                {
                    "type": "true_false",
                    "question": "df.describe() only works on text (string) columns.",
                    "answer": False,
                    "explanation": "df.describe() works on numerical columns by default, showing stats like mean, std, min, and max."
                }
            ],
            "challenge": {
                "instructions": "Create a DataFrame with at least 5 students (name, gpa, year, major). Print its shape, then filter and print only students with GPA >= 3.5. Finally, print the average GPA of ALL students.",
                "starter_code": "import pandas as pd\n\n# Create your DataFrame\ndata = {\n    # add your data here\n}\ndf = pd.DataFrame(data)\n\n# Print shape\n\n# Print students with GPA >= 3.5\n\n# Print average GPA\n",
                "tests": [
                    {"type": "code_contains", "value": "pd.DataFrame"},
                    {"type": "code_contains", "value": "gpa"},
                    {"type": "runs_without_error"}
                ],
                "solution": 'import pandas as pd\ndata = {\n    "name": ["Alice","Bob","Carol","Dave","Eve"],\n    "gpa": [3.8, 3.2, 3.9, 2.9, 3.6],\n    "year": [1, 2, 1, 3, 2],\n    "major": ["BA","CS","BA","Econ","BA"]\n}\ndf = pd.DataFrame(data)\nprint(df.shape)\nprint(df.loc[df["gpa"] >= 3.5])\nprint("Average GPA:", df["gpa"].mean())'
            }
        },
        {
            "id": "m2-l3",
            "title": "Reading Data — CSV and JSON Files",
            "order": 3,
            "duration_min": 20,
            "concept": """Real data lives in files. CSV (Comma-Separated Values) and JSON are the two most common formats you'll encounter.

**Reading a CSV file:**
```python
import pandas as pd

df = pd.read_csv("students.csv")
print(df.head())
```

**Writing a CSV file:**
```python
df.to_csv("output.csv", index=False)  # index=False skips row numbers
```

**Reading a JSON file:**
```python
df = pd.read_json("data.json")

# Or read raw JSON with Python's built-in json module:
import json
with open("data.json", "r") as f:
    data = json.load(f)
```

**Reading from a URL (common in analytics):**
```python
url = "https://example.com/data.csv"
df = pd.read_csv(url)
```

**Useful read_csv options:**
```python
pd.read_csv("data.csv",
    sep=";",              # delimiter (default is comma)
    header=0,             # which row is the header (0 = first)
    usecols=["a", "b"],  # only load specific columns
    nrows=100,            # only load first 100 rows
    encoding="utf-8"      # text encoding
)
```

**Quick inspection after loading:**
```python
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())   # Count missing values per column
print(df.head())
```""",
            "reference": {
                "key_syntax": [
                    'pd.read_csv("file.csv")',
                    'df.to_csv("file.csv", index=False)',
                    'pd.read_json("file.json")',
                    "df.isnull().sum()  # missing values"
                ],
                "notes": "Always check df.isnull().sum() after loading data to spot missing values."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does df.isnull().sum() tell you?",
                    "options": [
                        "The total number of rows",
                        "The number of missing values per column",
                        "The sum of all numeric values",
                        "Which columns are text"
                    ],
                    "answer": 1,
                    "explanation": "isnull() returns True for missing values, and sum() counts them per column."
                },
                {
                    "type": "true_false",
                    "question": "index=False in df.to_csv() prevents the row numbers from being written to the file.",
                    "answer": True,
                    "explanation": "Without index=False, pandas writes an extra column with row numbers (0, 1, 2...). Usually you don't want that."
                },
                {
                    "type": "fill_blank",
                    "question": "Load a CSV file called 'sales.csv' into a DataFrame called df",
                    "template": 'df = pd.___(\"sales.csv\")',
                    "answer": "read_csv",
                    "explanation": "pd.read_csv() is the standard function for loading CSV files into a DataFrame."
                }
            ],
            "challenge": {
                "instructions": "Create a dictionary of sales data (product, quantity, price for at least 4 products), convert it to a DataFrame, save it to 'sales.csv', then read it back and print the total revenue (quantity * price summed for all products).",
                "starter_code": "import pandas as pd\n\n# Create sales data dictionary\ndata = {\n    # add your data\n}\n\n# Create DataFrame\n\n# Save to CSV\n\n# Read it back\n\n# Calculate and print total revenue\n",
                "tests": [
                    {"type": "code_contains", "value": "to_csv"},
                    {"type": "code_contains", "value": "read_csv"},
                    {"type": "runs_without_error"}
                ],
                "solution": 'import pandas as pd\ndata = {\n    "product": ["Apple","Banana","Cherry","Date"],\n    "quantity": [100, 150, 80, 60],\n    "price": [0.5, 0.3, 1.2, 2.0]\n}\ndf = pd.DataFrame(data)\ndf.to_csv("sales.csv", index=False)\ndf2 = pd.read_csv("sales.csv")\ndf2["revenue"] = df2["quantity"] * df2["price"]\nprint("Total revenue:", df2["revenue"].sum())'
            }
        },
        {
            "id": "m2-l4",
            "title": "Data Cleaning — Handling Messy Data",
            "order": 4,
            "duration_min": 25,
            "concept": """In the real world, data is messy. Missing values, duplicates, wrong types, and inconsistent formatting are everywhere. Data cleaning is often 80% of a data analyst's work.

**Handling missing values (NaN):**
```python
df.isnull().sum()              # Count NaN per column
df.dropna()                    # Remove rows with any NaN
df.dropna(subset=["score"])    # Remove rows only if 'score' is NaN
df["score"].fillna(0)          # Replace NaN with 0
df["score"].fillna(df["score"].mean())  # Replace NaN with mean
```

**Removing duplicates:**
```python
df.duplicated().sum()          # Count duplicates
df.drop_duplicates()           # Remove duplicate rows
df.drop_duplicates(subset=["email"])  # Unique by email only
```

**Fixing data types:**
```python
df["age"] = df["age"].astype(int)
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].str.replace("$", "").astype(float)
```

**Cleaning string columns:**
```python
df["name"] = df["name"].str.strip()    # Remove whitespace
df["name"] = df["name"].str.lower()    # Lowercase
df["name"] = df["name"].str.title()    # Title Case
```

**Renaming columns:**
```python
df.rename(columns={"old_name": "new_name"}, inplace=True)
df.columns = ["col1", "col2", "col3"]  # Replace all names
```""",
            "reference": {
                "key_syntax": [
                    "df.dropna() / df.fillna(value)",
                    "df.drop_duplicates()",
                    'df["col"].astype(type)',
                    'df["col"].str.strip() / .lower() / .title()',
                    'df.rename(columns={...}, inplace=True)'
                ],
                "notes": "Always check data quality right after loading. Missing values + wrong types cause silent bugs."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does df.fillna(df['score'].mean()) do?",
                    "options": [
                        "Removes rows with missing scores",
                        "Replaces NaN values with the column mean",
                        "Replaces all values with 0",
                        "Calculates a new mean column"
                    ],
                    "answer": 1,
                    "explanation": "fillna() fills NaN values. Using the column mean is a common strategy to handle missing numerical data."
                },
                {
                    "type": "true_false",
                    "question": "df.drop_duplicates() modifies the original DataFrame in place.",
                    "answer": False,
                    "explanation": "By default, pandas operations return a new DataFrame. Use inplace=True or reassign: df = df.drop_duplicates()."
                },
                {
                    "type": "fill_blank",
                    "question": "Convert a column 'age' from string to integer",
                    "template": 'df["age"] = df["age"].___( ___ )',
                    "answer": "astype(int)",
                    "explanation": ".astype(int) converts the column to integer type."
                }
            ],
            "challenge": {
                "instructions": "The DataFrame below has missing values, duplicates, and inconsistent casing in 'name'. Clean it: fill missing scores with the mean, remove duplicates, and make all names Title Case. Then print the cleaned DataFrame.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\ndata = {\n    'name': ['alice', 'BOB', 'carol', 'alice', 'dave', None],\n    'score': [85, None, 92, 85, 78, 90]\n}\ndf = pd.DataFrame(data)\n\n# Fix names (Title Case)\n\n# Fill missing scores with mean\n\n# Remove duplicates\n\nprint(df)\n",
                "tests": [
                    {"type": "code_contains", "value": "fillna"},
                    {"type": "code_contains", "value": "drop_duplicates"},
                    {"type": "runs_without_error"}
                ],
                "solution": 'import pandas as pd\nimport numpy as np\ndata = {\n    "name": ["alice","BOB","carol","alice","dave",None],\n    "score": [85, None, 92, 85, 78, 90]\n}\ndf = pd.DataFrame(data)\ndf["name"] = df["name"].str.title()\ndf["score"] = df["score"].fillna(df["score"].mean())\ndf = df.drop_duplicates()\ndf = df.dropna(subset=["name"])\nprint(df)'
            }
        },
        {
            "id": "m2-l5",
            "title": "Filtering, Sorting, and Grouping",
            "order": 5,
            "duration_min": 25,
            "concept": """The most common data analysis tasks are filtering (find specific rows), sorting (rank data), and grouping (aggregate by category).

**Filtering:**
```python
# Single condition
high_gpa = df[df["gpa"] >= 3.5]

# Multiple conditions (use & and | with parentheses!)
df[(df["gpa"] >= 3.5) & (df["year"] == 1)]
df[(df["major"] == "CS") | (df["major"] == "BA")]

# String filtering
df[df["name"].str.contains("Jo")]  # contains "Jo"
df[df["major"].isin(["CS", "BA"])]  # in a list
```

**Sorting:**
```python
df.sort_values("gpa")                      # Ascending (low to high)
df.sort_values("gpa", ascending=False)      # Descending (high to low)
df.sort_values(["year", "gpa"])            # Sort by multiple columns
```

**Grouping and aggregation — the heart of analytics:**
```python
# Average GPA by major
df.groupby("major")["gpa"].mean()

# Multiple aggregations
df.groupby("major").agg({
    "gpa": ["mean", "max", "min"],
    "name": "count"
})

# Count students per major
df.groupby("major").size()

# Reset index to get a clean DataFrame
result = df.groupby("major")["gpa"].mean().reset_index()
```""",
            "reference": {
                "key_syntax": [
                    'df[df["col"] > value]',
                    '(condition1) & (condition2)',
                    'df.sort_values("col", ascending=False)',
                    'df.groupby("col")["col2"].mean()',
                    ".reset_index()"
                ],
                "notes": "Always use & (and) and | (or) with parentheses around each condition when filtering DataFrames."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": 'To filter rows where gpa > 3.5 AND year == 2, you write:',
                    "options": [
                        'df[df["gpa"] > 3.5 and df["year"] == 2]',
                        'df[(df["gpa"] > 3.5) & (df["year"] == 2)]',
                        'df[df["gpa"] > 3.5 & df["year"] == 2]',
                        'df.filter(gpa > 3.5, year == 2)'
                    ],
                    "answer": 1,
                    "explanation": "Use & for 'and' and | for 'or' in pandas filtering. Always wrap each condition in parentheses to avoid operator precedence errors."
                },
                {
                    "type": "fill_blank",
                    "question": "Group df by 'department' and get the mean of 'salary'",
                    "template": 'df.groupby("department")["salary"].___( )',
                    "answer": "mean()",
                    "explanation": ".mean() calculates the average. You can also use .sum(), .max(), .min(), .count()."
                },
                {
                    "type": "true_false",
                    "question": "df.sort_values('score') sorts from highest to lowest by default.",
                    "answer": False,
                    "explanation": "sort_values() sorts ascending (low to high) by default. Use ascending=False for high to low."
                }
            ],
            "challenge": {
                "instructions": "Using the sales DataFrame below: (1) Filter to show only sales > 500. (2) Sort by revenue descending. (3) Group by 'region' and print the total revenue per region.",
                "starter_code": "import pandas as pd\n\ndata = {\n    'product': ['A','B','C','D','E','F'],\n    'region':  ['North','South','North','East','South','East'],\n    'units':   [120, 45, 300, 80, 210, 95],\n    'price':   [5, 12, 3, 8, 4, 10]\n}\ndf = pd.DataFrame(data)\ndf['revenue'] = df['units'] * df['price']\n\n# 1. Filter: revenue > 500\n\n# 2. Sort by revenue descending\n\n# 3. Total revenue by region\n",
                "tests": [
                    {"type": "code_contains", "value": "groupby"},
                    {"type": "code_contains", "value": "sort_values"},
                    {"type": "runs_without_error"}
                ],
                "solution": 'import pandas as pd\ndata = {\n    "product": ["A","B","C","D","E","F"],\n    "region": ["North","South","North","East","South","East"],\n    "units": [120,45,300,80,210,95],\n    "price": [5,12,3,8,4,10]\n}\ndf = pd.DataFrame(data)\ndf["revenue"] = df["units"] * df["price"]\nprint(df[df["revenue"] > 500])\nprint(df.sort_values("revenue", ascending=False))\nprint(df.groupby("region")["revenue"].sum())'
            }
        },
        {
            "id": "m2-l6",
            "title": "Data Visualization — Telling Stories with Charts",
            "order": 6,
            "duration_min": 25,
            "concept": """Data visualization turns numbers into insights. Python's **matplotlib** and **seaborn** libraries make it easy to create professional charts.

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Quick pandas plot
df["score"].hist()
plt.show()
```

**Common chart types:**

**Bar chart — compare categories:**
```python
categories = ["A", "B", "C", "D"]
counts = [45, 30, 20, 5]

plt.bar(categories, counts, color="#3b82f6")
plt.title("Grade Distribution")
plt.xlabel("Grade")
plt.ylabel("Count")
plt.show()
```

**Line chart — show trends over time:**
```python
months = [1, 2, 3, 4, 5]
sales = [100, 120, 115, 140, 160]

plt.plot(months, sales, marker='o', color='cyan')
plt.title("Monthly Sales")
plt.show()
```

**Scatter plot — show relationships:**
```python
plt.scatter(df["study_hours"], df["score"], alpha=0.6)
plt.xlabel("Study Hours")
plt.ylabel("Score")
plt.show()
```

**Seaborn — easier, prettier:**
```python
sns.histplot(df["score"], bins=10)  # Histogram
sns.boxplot(x="major", y="gpa", data=df)  # Box plot by group
sns.heatmap(df.corr(), annot=True)  # Correlation matrix
```""",
            "reference": {
                "key_syntax": [
                    "import matplotlib.pyplot as plt",
                    "plt.bar() / plt.plot() / plt.scatter()",
                    "plt.title() / .xlabel() / .ylabel()",
                    "plt.show()",
                    "sns.histplot() / sns.boxplot() / sns.heatmap()"
                ],
                "notes": "Always call plt.show() to display the chart. Save with plt.savefig('chart.png')."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which chart type is best for showing a trend over time?",
                    "options": ["Bar chart", "Line chart", "Scatter plot", "Pie chart"],
                    "answer": 1,
                    "explanation": "Line charts are ideal for showing trends over time because the connected line emphasizes the progression."
                },
                {
                    "type": "true_false",
                    "question": "plt.show() must be called to display a matplotlib chart.",
                    "answer": True,
                    "explanation": "plt.show() renders and displays the chart. Without it, the chart is created in memory but not shown."
                },
                {
                    "type": "fill_blank",
                    "question": "Set the title of a matplotlib chart",
                    "template": 'plt.___("Sales by Region")',
                    "answer": "title",
                    "explanation": "plt.title() sets the chart title. plt.xlabel() and plt.ylabel() set axis labels."
                }
            ],
            "challenge": {
                "instructions": "Create a bar chart showing the average GPA by major using the data below. Add a title, x-label, y-label. Save it as 'gpa_chart.png' using plt.savefig().",
                "starter_code": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndata = {\n    'name': ['Alice','Bob','Carol','Dave','Eve','Frank','Grace'],\n    'major': ['BA','CS','BA','Econ','CS','BA','Econ'],\n    'gpa': [3.8, 3.5, 3.2, 3.9, 3.7, 3.4, 3.1]\n}\ndf = pd.DataFrame(data)\n\n# Calculate average GPA by major\n\n# Create bar chart\n\n# Add title and labels\n\n# Save the chart\nplt.savefig('gpa_chart.png')\nplt.show()\n",
                "tests": [
                    {"type": "code_contains", "value": "groupby"},
                    {"type": "code_contains", "value": "plt.bar"},
                    {"type": "runs_without_error"}
                ],
                "solution": 'import pandas as pd\nimport matplotlib.pyplot as plt\ndata = {\n    "name":["Alice","Bob","Carol","Dave","Eve","Frank","Grace"],\n    "major":["BA","CS","BA","Econ","CS","BA","Econ"],\n    "gpa":[3.8,3.5,3.2,3.9,3.7,3.4,3.1]\n}\ndf = pd.DataFrame(data)\navg = df.groupby("major")["gpa"].mean()\nplt.bar(avg.index, avg.values, color="#3b82f6")\nplt.title("Average GPA by Major")\nplt.xlabel("Major")\nplt.ylabel("GPA")\nplt.savefig("gpa_chart.png")\nplt.show()'
            }
        },
        {
            "id": "m2-l7",
            "title": "Descriptive Statistics — Understanding Your Data",
            "order": 7,
            "duration_min": 20,
            "concept": """Before building models, you need to **understand your data**. Descriptive statistics summarize key characteristics.

**The key statistics:**
```python
import pandas as pd
import numpy as np

df["score"].mean()     # Average
df["score"].median()   # Middle value (50th percentile)
df["score"].mode()     # Most frequent value
df["score"].std()      # Standard deviation (spread)
df["score"].var()      # Variance (std²)
df["score"].describe() # All at once!
```

**Percentiles and quartiles:**
```python
df["score"].quantile(0.25)  # 25th percentile (Q1)
df["score"].quantile(0.75)  # 75th percentile (Q3)
df["score"].quantile(0.50)  # 50th percentile = median
```

**Correlation — do two variables move together?**
```python
df.corr()                          # Correlation matrix (all numeric cols)
df["study_hours"].corr(df["score"]) # Single correlation

# Interpretation:
#  1.0 = perfect positive correlation
#  0.0 = no correlation
# -1.0 = perfect negative correlation
```

**Value counts — frequency distribution:**
```python
df["grade"].value_counts()           # Count each category
df["grade"].value_counts(normalize=True)  # As percentages
```

**Understanding spread:**
- **Mean** tells you the center
- **Std** tells you how spread out the data is
- **Median** is robust to outliers (extreme values)
- Use **median** when data has outliers (like income data)""",
            "reference": {
                "key_syntax": [
                    ".mean() .median() .mode() .std()",
                    ".describe()  # full summary",
                    ".quantile(0.25)  # Q1",
                    ".corr()  # correlation matrix",
                    ".value_counts()  # frequency"
                ],
                "notes": "A correlation above 0.7 or below -0.7 is considered strong. 0.3-0.7 is moderate."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which statistic is most resistant to extreme outliers?",
                    "options": ["Mean", "Std", "Median", "Variance"],
                    "answer": 2,
                    "explanation": "The median is the middle value and isn't affected by extreme outliers. The mean gets pulled toward outliers."
                },
                {
                    "type": "true_false",
                    "question": "A correlation of -0.85 indicates a strong relationship between two variables.",
                    "answer": True,
                    "explanation": "Correlation measures strength regardless of direction. -0.85 is a strong negative correlation (as one goes up, the other goes down strongly)."
                },
                {
                    "type": "fill_blank",
                    "question": "Get the frequency count of each value in a 'grade' column",
                    "template": 'df["grade"].___( )',
                    "answer": "value_counts()",
                    "explanation": ".value_counts() counts how many times each unique value appears."
                }
            ],
            "challenge": {
                "instructions": "Analyze the dataset below: print the describe() summary, find which two columns have the strongest correlation, and print the grade distribution as percentages using value_counts(normalize=True).",
                "starter_code": "import pandas as pd\n\ndata = {\n    'study_hours': [2, 5, 3, 8, 1, 6, 4, 7, 2, 5],\n    'score': [65, 88, 72, 95, 55, 90, 78, 93, 60, 85],\n    'grade': ['C','B','C','A','F','A','C','A','D','B']\n}\ndf = pd.DataFrame(data)\n\n# Print describe() for numeric columns\n\n# Print correlation matrix\n\n# Print grade distribution as percentages\n",
                "tests": [
                    {"type": "code_contains", "value": "describe"},
                    {"type": "code_contains", "value": "corr"},
                    {"type": "code_contains", "value": "value_counts"}
                ],
                "solution": 'import pandas as pd\ndata = {\n    "study_hours":[2,5,3,8,1,6,4,7,2,5],\n    "score":[65,88,72,95,55,90,78,93,60,85],\n    "grade":["C","B","C","A","F","A","C","A","D","B"]\n}\ndf = pd.DataFrame(data)\nprint(df.describe())\nprint(df.corr())\nprint(df["grade"].value_counts(normalize=True))'
            }
        },
        {
            "id": "m2-l8",
            "title": "Module 2 Capstone — Sales Analytics Report",
            "order": 8,
            "duration_min": 35,
            "concept": """Time to build a real analytics report from scratch. This capstone combines everything from Module 2.

**The workflow of a data analytics project:**
1. **Load** the data
2. **Inspect** (shape, dtypes, missing values)
3. **Clean** (handle NaN, fix types, remove duplicates)
4. **Explore** (descriptive stats, value counts)
5. **Analyze** (filter, group, aggregate)
6. **Visualize** (charts that tell the story)
7. **Report** (summarize findings)

**Example — Sales Analytics:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load
df = pd.read_csv("sales.csv")

# 2. Inspect
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())

# 3. Clean
df = df.dropna()
df["revenue"] = df["units"] * df["price"]

# 4. Analyze
print("\\nTop regions by revenue:")
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False))

print("\\nBest selling product:")
print(df.groupby("product")["units"].sum().idxmax())

# 5. Visualize
region_rev = df.groupby("region")["revenue"].sum()
plt.bar(region_rev.index, region_rev.values)
plt.title("Revenue by Region")
plt.savefig("report.png")
plt.show()
```

**idxmax() and idxmin()** — return the index (label) of the maximum or minimum value. Very useful for finding "top performers".""",
            "reference": {
                "key_syntax": [
                    ".idxmax()  # label of max value",
                    ".idxmin()  # label of min value",
                    "Full analytics pipeline: load → inspect → clean → analyze → visualize"
                ],
                "notes": "Real analytics projects follow this workflow. You'll use it constantly in your program."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does .idxmax() return?",
                    "options": [
                        "The maximum value",
                        "The index label of the maximum value",
                        "The maximum index number",
                        "A sorted list"
                    ],
                    "answer": 1,
                    "explanation": "idxmax() returns the label (index) of the row/column with the maximum value — useful for 'which product had the most sales?'"
                },
                {
                    "type": "true_false",
                    "question": "In a typical analytics workflow, cleaning comes before analysis.",
                    "answer": True,
                    "explanation": "Always clean your data first. Dirty data produces wrong analysis — 'garbage in, garbage out.'"
                }
            ],
            "challenge": {
                "instructions": "Complete the sales analytics report: create a DataFrame with products, regions, units, and prices. Calculate revenue. Find the top region by revenue, the best-selling product by units, and create a bar chart of revenue by region. Print a 3-line summary of your findings.",
                "starter_code": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndata = {\n    'product': ['Laptop','Phone','Tablet','Laptop','Phone','Tablet','Laptop'],\n    'region':  ['North','North','South','South','East','East','North'],\n    'units':   [50, 120, 80, 35, 90, 45, 30],\n    'price':   [999, 699, 499, 999, 699, 499, 999]\n}\ndf = pd.DataFrame(data)\n\n# 1. Add revenue column\n\n# 2. Top region by total revenue\n\n# 3. Best-selling product by total units\n\n# 4. Bar chart of revenue by region\n\n# 5. Print 3-line summary\n",
                "tests": [
                    {"type": "code_contains", "value": "groupby"},
                    {"type": "code_contains", "value": "plt.bar"},
                    {"type": "code_contains", "value": "idxmax"}
                ],
                "solution": 'import pandas as pd\nimport matplotlib.pyplot as plt\ndata = {\n    "product":["Laptop","Phone","Tablet","Laptop","Phone","Tablet","Laptop"],\n    "region":["North","North","South","South","East","East","North"],\n    "units":[50,120,80,35,90,45,30],\n    "price":[999,699,499,999,699,499,999]\n}\ndf = pd.DataFrame(data)\ndf["revenue"] = df["units"] * df["price"]\ntop_region = df.groupby("region")["revenue"].sum().idxmax()\nbest_product = df.groupby("product")["units"].sum().idxmax()\nreg_rev = df.groupby("region")["revenue"].sum()\nplt.bar(reg_rev.index, reg_rev.values, color="#3b82f6")\nplt.title("Revenue by Region")\nplt.savefig("report.png")\nplt.show()\nprint(f"Top region: {top_region}")\nprint(f"Best product by units: {best_product}")\nprint(f"Total revenue: ${df[\'revenue\'].sum():,.0f}")'
            }
        },
        {
            "id": "m2-l9",
            "title": "Pandas Series — 1D Data Analysis",
            "order": 9,
            "duration_min": 20,
            "real_world_context": "As a business analyst, you'll often work with a single column of data — Series is the building block of every DataFrame.",
            "concept": """A **Series** is a one-dimensional labeled array — essentially a single column of data with an index. Every column you pull out of a DataFrame is a Series.

Understanding Series deeply makes you a faster, more precise analyst. You'll use them for quick calculations, comparisons, and as building blocks for more complex operations.

```python
import pandas as pd

# Creating a Series directly
revenue = pd.Series([4200, 3800, 5100, 4700, 3200],
                    index=["Jan", "Feb", "Mar", "Apr", "May"],
                    name="Monthly Revenue")
print(revenue)
# Jan    4200
# Feb    3800
# Mar    5100
# Apr    4700
# May    3200
# Name: Monthly Revenue, dtype: int64

# Key attributes
print(revenue.values)   # array([4200, 3800, 5100, 4700, 3200])
print(revenue.index)    # Index(['Jan', 'Feb', 'Mar', 'Apr', 'May'])
print(revenue.name)     # Monthly Revenue
print(revenue.dtype)    # int64
```

**Series vs DataFrame:** A DataFrame is just multiple Series sharing the same index. When you do `df["revenue"]` you get a Series back.

```python
# Pulling a Series from a DataFrame
df = pd.DataFrame({"product": ["A","B","C"], "revenue": [1000, 2000, 1500]})
rev_series = df["revenue"]
print(type(rev_series))  # <class 'pandas.core.series.Series'>

# Operations on a Series — all vectorized
print(revenue.sum())      # 21000
print(revenue.mean())     # 4200.0
print(revenue.max())      # 5100
print(revenue.idxmax())   # Mar  (which month had max revenue)
```

**Indexing a Series:**
```python
# By label
print(revenue["Mar"])     # 5100
print(revenue[["Jan","Mar"]])  # multiple labels

# By position
print(revenue.iloc[0])    # 4200 (first item)
print(revenue.iloc[-1])   # 3200 (last item)

# Boolean filtering
high_months = revenue[revenue > 4000]
print(high_months)
# Jan    4200
# Mar    5100
# Apr    4700
```

**When to use Series vs DataFrame:** Use a Series when you're working with a single variable (one column). Use a DataFrame when you need multiple columns and the relationships between them.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd

# A sales rep's quarterly commissions
commissions = pd.Series(
    [3200, 4100, 2800, 5300],
    index=["Q1", "Q2", "Q3", "Q4"],
    name="Commission"
)

# Total and average
print("Total:", commissions.sum())       # Total: 15400
print("Average:", commissions.mean())    # Average: 3850.0

# Best quarter
print("Best quarter:", commissions.idxmax())  # Best quarter: Q4

# Quarters above average
above_avg = commissions[commissions > commissions.mean()]
print("Above-average quarters:")
print(above_avg)
# Q2    4100
# Q4    5300

# Apply a bonus: 10% increase in Q4
commissions["Q4"] = commissions["Q4"] * 1.10
print("Q4 with bonus:", commissions["Q4"])  # 5830.0""",
                "explanation": "We create a Series with named index labels (Q1-Q4) so we can access data by quarter name rather than number. idxmax() returns the label of the highest value — much more useful than just the number. Boolean filtering on a Series works exactly like filtering a DataFrame column."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "pd.Series([...], index=[...], name='...')",
                    "s.values  /  s.index  /  s.name",
                    "s['label']  /  s.iloc[0]",
                    "s[s > value]  # boolean filter",
                    "s.idxmax()  /  s.idxmin()"
                ],
                "notes": "A DataFrame column accessed with df['col'] is always a Series. Operations on a Series are vectorized — no loops needed."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does s.idxmax() return for a Series?",
                    "options": [
                        "A) The maximum numeric value",
                        "B) The index label of the maximum value",
                        "C) The position (integer) of the maximum value",
                        "D) A sorted Series"
                    ],
                    "answer": 1,
                    "explanation": "idxmax() returns the index label (e.g., 'Mar' or 'Q4') of the maximum value, not the value itself. Use .max() to get the actual maximum value."
                },
                {
                    "type": "true_false",
                    "question": "Every column in a DataFrame is technically a Series.",
                    "answer": True,
                    "explanation": "A DataFrame is a collection of Series objects that share the same index. When you do df['column'], you get a Series back."
                },
                {
                    "type": "fill_blank",
                    "question": "Create a Series named 'sales' from a list [100, 200, 300]",
                    "template": "s = pd.Series([100, 200, 300], ___='sales')",
                    "answer": "name",
                    "explanation": "The 'name' parameter assigns a label to the Series, which becomes the column name if you add it to a DataFrame."
                }
            ],
            "challenge": {
                "instructions": "You have monthly website traffic data for a startup. Create a Series with the 12 months as the index and traffic numbers as values. Then: (1) print the month with the highest traffic using idxmax(), (2) print all months where traffic exceeded 10000, (3) calculate the percentage growth from January to December.",
                "starter_code": "import pandas as pd\n\nmonths = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\ntraffic = [5200, 6100, 7400, 8200, 9100, 11000, 12500, 13200, 11800, 10500, 9800, 14000]\n\n# Create the Series\n\n# Print the peak month\n\n# Print months with traffic > 10000\n\n# Print % growth Jan to Dec\n",
                "tests": [
                    {"type": "output_contains", "value": "Dec"},
                    {"type": "code_contains", "value": "idxmax"}
                ],
                "solution": "import pandas as pd\nmonths = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\ntraffic = [5200,6100,7400,8200,9100,11000,12500,13200,11800,10500,9800,14000]\ns = pd.Series(traffic, index=months, name='Traffic')\nprint('Peak month:', s.idxmax())\nprint('Months above 10000:')\nprint(s[s > 10000])\ngrowth = (s['Dec'] - s['Jan']) / s['Jan'] * 100\nprint(f'Growth Jan to Dec: {growth:.1f}%')"
            },
            "challenge_variations": [
                "Variation 1: Use daily sales data for one week and find the day with lowest sales using idxmin().",
                "Variation 2: Create a Series of employee salaries and find everyone earning above the median.",
                "Variation 3: Track NPS scores by product and compute month-over-month change.",
                "Variation 4: Create a Series of store locations and their ratings, filter to only 4-star and above.",
                "Variation 5: Build a Series of ad spend by channel, calculate each channel's share of total spend.",
                "Variation 6: Store quarterly profit margins and find the worst-performing quarter.",
                "Variation 7: Create a Series of customer counts by city, sort descending and show top 5.",
                "Variation 8: Use a boolean mask to flag months where revenue was below the company target of 8000.",
                "Variation 9: Multiply a Series of unit prices by 1.08 to apply a sales tax to all prices at once.",
                "Variation 10: Create two Series (revenue and cost) and subtract them to produce a profit Series."
            ]
        },
        {
            "id": "m2-l10",
            "title": "Index Operations — Controlling Your Data's Address",
            "order": 10,
            "duration_min": 20,
            "real_world_context": "The index is the row address system of a DataFrame. Mastering it lets you look up, align, and merge data precisely — critical when combining datasets in business analytics.",
            "concept": """The **index** in a DataFrame is like a row's address. By default it's 0, 1, 2... but you can make it anything meaningful — a date, a product ID, a customer name.

Understanding the index is crucial because `.loc` and `.iloc` behave differently, and merges/joins depend on the index aligning correctly.

```python
import pandas as pd

df = pd.DataFrame({
    "product": ["Laptop", "Phone", "Tablet", "Watch"],
    "revenue": [45000, 32000, 18000, 9500],
    "units":   [45, 92, 60, 38]
})

# Default integer index
print(df.index)  # RangeIndex(start=0, stop=4, step=1)
```

**Setting a meaningful index:**
```python
df = df.set_index("product")
print(df)
#          revenue  units
# product
# Laptop     45000     45
# Phone      32000     92
# Tablet     18000     60
# Watch       9500     38

# Now look up by name
print(df.loc["Laptop"])
# revenue    45000
# units         45
```

**Resetting the index (turning it back into a column):**
```python
df_reset = df.reset_index()
# product is now a regular column again
```

**.loc vs .iloc — the most important distinction in pandas:**
```python
# .loc  = label-based (use the actual name/value)
df.loc["Phone"]            # row where index == "Phone"
df.loc["Phone", "revenue"] # specific cell

# .iloc = position-based (use the integer position 0, 1, 2...)
df.iloc[0]         # first row (regardless of index label)
df.iloc[0, 1]      # first row, second column
df.iloc[1:3]       # rows at positions 1 and 2

# Slicing with .loc is INCLUSIVE on both ends
# Slicing with .iloc is EXCLUSIVE on the end (like Python lists)
```

**Multi-level index (MultiIndex):**
```python
sales = pd.DataFrame({
    "region": ["North","North","South","South"],
    "product": ["Laptop","Phone","Laptop","Phone"],
    "revenue": [12000, 8000, 9000, 11000]
})
sales = sales.set_index(["region", "product"])
print(sales.loc["North"])           # All North rows
print(sales.loc[("North","Laptop")]) # Specific cell
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd

# Customer purchase data
df = pd.DataFrame({
    "customer_id": ["C001","C002","C003","C004","C005"],
    "name":        ["Alice","Bob","Carol","Dave","Eve"],
    "spend":       [1200, 450, 3200, 890, 2100],
    "tier":        ["Gold","Bronze","Platinum","Silver","Gold"]
})

# Set customer_id as the index for fast lookups
df = df.set_index("customer_id")

# Look up a specific customer by ID
print(df.loc["C003"])
# name      Carol
# spend      3200
# tier   Platinum

# Look up just their spend
print(df.loc["C003", "spend"])  # 3200

# Get first two customers by position
print(df.iloc[:2])

# Reset index to get customer_id back as a column
df_flat = df.reset_index()
print(df_flat.columns.tolist())
# ['customer_id', 'name', 'spend', 'tier']""",
                "explanation": "Setting customer_id as the index makes lookups by ID instant and readable. .loc['C003'] uses the actual ID label, while .iloc[:2] uses position 0 and 1 regardless of what the index is. reset_index() reverses the operation — useful before saving to CSV."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "df.set_index('col')",
                    "df.reset_index()",
                    "df.loc['label'] / df.loc['label','col']",
                    "df.iloc[0] / df.iloc[0:3]",
                    "df.set_index(['col1','col2'])  # MultiIndex"
                ],
                "notes": ".loc is label-based and inclusive at both ends when slicing. .iloc is position-based and exclusive at the end. Never confuse them — it causes silent off-by-one errors."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What is the key difference between .loc and .iloc?",
                    "options": [
                        "A) .loc is faster than .iloc",
                        "B) .loc uses label-based indexing; .iloc uses integer position",
                        "C) .loc only works on rows; .iloc only works on columns",
                        "D) They are identical"
                    ],
                    "answer": 1,
                    "explanation": ".loc selects by the actual index label (e.g., 'Laptop', 'C003'). .iloc selects by integer position (0, 1, 2...). When the index is integers, they look similar but behave differently with slices."
                },
                {
                    "type": "true_false",
                    "question": "df.reset_index() turns the current index back into a regular column.",
                    "answer": True,
                    "explanation": "reset_index() moves the index back to a regular column and replaces it with the default 0, 1, 2... integer index. Useful before saving or merging DataFrames."
                },
                {
                    "type": "fill_blank",
                    "question": "Set the 'order_id' column as the DataFrame index",
                    "template": "df = df.___(\"order_id\")",
                    "answer": "set_index",
                    "explanation": "set_index('col') promotes a column to be the row index, enabling fast label-based lookups with .loc."
                }
            ],
            "challenge": {
                "instructions": "You have a store inventory DataFrame. Set 'sku' as the index. Use .loc to look up the price of 'SKU-103'. Use .iloc to get the last two rows. Then create a MultiIndex by setting both 'category' and 'sku' as the index and look up all items in the 'Electronics' category.",
                "starter_code": "import pandas as pd\n\ndata = {\n    'sku':      ['SKU-101','SKU-102','SKU-103','SKU-104','SKU-105'],\n    'category': ['Electronics','Clothing','Electronics','Clothing','Electronics'],\n    'item':     ['Laptop','Jacket','Headphones','Jeans','Charger'],\n    'price':    [999, 89, 149, 59, 29],\n    'stock':    [15, 40, 28, 55, 100]\n}\ndf = pd.DataFrame(data)\n\n# Set 'sku' as index\n\n# Look up price of SKU-103 using .loc\n\n# Get last 2 rows using .iloc\n\n# Create MultiIndex on ['category','sku'] and look up 'Electronics'\n",
                "tests": [
                    {"type": "code_contains", "value": "set_index"},
                    {"type": "code_contains", "value": ".loc"},
                    {"type": "code_contains", "value": ".iloc"}
                ],
                "solution": "import pandas as pd\ndata = {\n    'sku':['SKU-101','SKU-102','SKU-103','SKU-104','SKU-105'],\n    'category':['Electronics','Clothing','Electronics','Clothing','Electronics'],\n    'item':['Laptop','Jacket','Headphones','Jeans','Charger'],\n    'price':[999,89,149,59,29],\n    'stock':[15,40,28,55,100]\n}\ndf = pd.DataFrame(data)\ndf = df.set_index('sku')\nprint('SKU-103 price:', df.loc['SKU-103','price'])\nprint('Last 2 rows:')\nprint(df.iloc[-2:])\ndf2 = df.reset_index().set_index(['category','sku'])\nprint('Electronics:')\nprint(df2.loc['Electronics'])"
            },
            "challenge_variations": [
                "Variation 1: Set 'employee_id' as the index and look up salary using .loc for a specific ID.",
                "Variation 2: Use .iloc to select every other row from a DataFrame using step slicing (::2).",
                "Variation 3: Create a MultiIndex on region and month, then look up all data for one region.",
                "Variation 4: Use .loc with a slice to select all rows between two product names alphabetically.",
                "Variation 5: Reset the index after a groupby to get a clean DataFrame for export.",
                "Variation 6: Set a date column as the index, then use .loc to filter a date range.",
                "Variation 7: Use .iloc to get the middle row of a DataFrame regardless of its length.",
                "Variation 8: Compare .loc and .iloc on the same DataFrame to demonstrate the difference.",
                "Variation 9: Build a lookup table with product_id as index for O(1) price lookups.",
                "Variation 10: Create a 3-level MultiIndex (year, region, product) and query a specific combination."
            ]
        },
        {
            "id": "m2-l11",
            "title": "Merging DataFrames — Combining Tables",
            "order": 11,
            "duration_min": 25,
            "real_world_context": "Business data is almost never in one table. Orders live in one sheet, customers in another, products in a third. Merging lets you combine them into a single analysis-ready dataset.",
            "concept": """**pd.merge()** combines two DataFrames based on a shared column — exactly like SQL JOIN or Excel VLOOKUP, but faster and more powerful.

```python
import pandas as pd

# Two tables: orders and customers
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer_id": [101, 102, 101, 103],
    "amount": [250, 180, 320, 90]
})

customers = pd.DataFrame({
    "customer_id": [101, 102, 104],
    "name": ["Alice", "Bob", "Carol"],
    "city": ["NYC", "LA", "Chicago"]
})
```

**Inner join — only matching rows (default):**
```python
result = pd.merge(orders, customers, on="customer_id", how="inner")
print(result)
#    order_id  customer_id  amount   name city
# 0         1          101     250  Alice  NYC
# 1         3          101     320  Alice  NYC
# 2         2          102     180    Bob   LA
# Note: order 4 (customer 103) is dropped — no match in customers
```

**Left join — keep ALL rows from the left table:**
```python
result = pd.merge(orders, customers, on="customer_id", how="left")
# All 4 orders appear; customer 103 gets NaN for name/city
```

**Right join — keep ALL rows from the right table:**
```python
result = pd.merge(orders, customers, on="customer_id", how="right")
# All 3 customers appear; customer 104 gets NaN for order data
```

**When column names differ between tables:**
```python
pd.merge(orders, customers,
         left_on="cust_id",   # column name in left table
         right_on="customer_id")  # column name in right table
```

**pd.concat() — stacking DataFrames vertically:**
```python
# Combine two months of sales data
jan = pd.DataFrame({"product": ["A","B"], "sales": [100, 200]})
feb = pd.DataFrame({"product": ["A","B"], "sales": [120, 210]})

combined = pd.concat([jan, feb], ignore_index=True)
print(combined)
#   product  sales
# 0       A    100
# 1       B    200
# 2       A    120
# 3       B    210
```

**When to use each:**
- `pd.merge()` — when tables share a key column (like a join)
- `pd.concat()` — when stacking rows of the same structure (appending data)""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd

# Products table
products = pd.DataFrame({
    "product_id": ["P01","P02","P03"],
    "product_name": ["Laptop","Mouse","Keyboard"],
    "cost": [800, 15, 45]
})

# Sales transactions table
sales = pd.DataFrame({
    "sale_id": [1, 2, 3, 4, 5],
    "product_id": ["P01","P02","P01","P03","P02"],
    "qty": [2, 5, 1, 3, 8],
    "price": [999, 25, 999, 79, 25]
})

# Join sales with product details
merged = pd.merge(sales, products, on="product_id", how="left")

# Calculate profit per sale
merged["revenue"] = merged["qty"] * merged["price"]
merged["profit"]  = merged["qty"] * (merged["price"] - merged["cost"])

print(merged[["product_name","qty","revenue","profit"]])
#   product_name  qty  revenue  profit
# 0       Laptop    2     1998     398
# 1        Mouse    5      125      50
# 2       Laptop    1      999     199
# 3     Keyboard    3      237     102
# 4        Mouse    8      200      80

print("Total profit:", merged["profit"].sum())  # 829""",
                "explanation": "We use a left join so all sales records are preserved. The merge matches on 'product_id'. After merging we can compute profit per sale because we now have both the sale price and the cost in the same row — something impossible without joining the tables."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "pd.merge(df1, df2, on='key', how='inner')",
                    "how='left' / 'right' / 'inner' / 'outer'",
                    "left_on='col1', right_on='col2'  # different column names",
                    "pd.concat([df1, df2], ignore_index=True)",
                    "pd.concat([df1, df2], axis=1)  # side by side"
                ],
                "notes": "Inner join (default) drops unmatched rows. Left join keeps all left rows — use this when the left table is your 'main' data and you're enriching it with extra info."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "You have an orders table and a customers table. You want ALL orders even if the customer info is missing. Which join do you use?",
                    "options": [
                        "A) inner join",
                        "B) right join",
                        "C) left join",
                        "D) outer join"
                    ],
                    "answer": 2,
                    "explanation": "A left join keeps every row from the left (orders) table, filling customer columns with NaN where there's no match. Use it when your primary table is on the left."
                },
                {
                    "type": "true_false",
                    "question": "pd.concat([df1, df2]) stacks the DataFrames side by side (adds columns).",
                    "answer": False,
                    "explanation": "By default pd.concat() stacks rows vertically (adds more rows). Use axis=1 to stack horizontally (add columns side by side)."
                },
                {
                    "type": "fill_blank",
                    "question": "Merge two DataFrames where left has column 'cust_id' and right has 'customer_id'",
                    "template": "pd.merge(left, right, left_on='cust_id', ___='customer_id', how='inner')",
                    "answer": "right_on",
                    "explanation": "When the key columns have different names, use left_on and right_on instead of on=."
                }
            ],
            "challenge": {
                "instructions": "You have three tables: employees, departments, and salaries. Merge them all together using the appropriate keys. Then group by department name and find average salary per department. Print results sorted highest to lowest.",
                "starter_code": "import pandas as pd\n\nemployees = pd.DataFrame({\n    'emp_id': [1,2,3,4,5],\n    'name': ['Alice','Bob','Carol','Dave','Eve'],\n    'dept_id': [10,20,10,30,20]\n})\ndepartments = pd.DataFrame({\n    'dept_id': [10,20,30],\n    'dept_name': ['Engineering','Marketing','Finance']\n})\nsalaries = pd.DataFrame({\n    'emp_id': [1,2,3,4,5],\n    'salary': [95000, 72000, 88000, 105000, 68000]\n})\n\n# Merge employees with departments\n\n# Merge result with salaries\n\n# Average salary by department name, sorted descending\n",
                "tests": [
                    {"type": "code_contains", "value": "pd.merge"},
                    {"type": "code_contains", "value": "groupby"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nemployees = pd.DataFrame({'emp_id':[1,2,3,4,5],'name':['Alice','Bob','Carol','Dave','Eve'],'dept_id':[10,20,10,30,20]})\ndepartments = pd.DataFrame({'dept_id':[10,20,30],'dept_name':['Engineering','Marketing','Finance']})\nsalaries = pd.DataFrame({'emp_id':[1,2,3,4,5],'salary':[95000,72000,88000,105000,68000]})\ndf = pd.merge(employees, departments, on='dept_id', how='left')\ndf = pd.merge(df, salaries, on='emp_id', how='left')\nresult = df.groupby('dept_name')['salary'].mean().sort_values(ascending=False)\nprint(result)"
            },
            "challenge_variations": [
                "Variation 1: Merge an orders table with a products table to compute total order value per order.",
                "Variation 2: Use an outer join to find customers who have never placed an order.",
                "Variation 3: Concatenate 12 monthly sales files into one annual DataFrame.",
                "Variation 4: Merge a student table with a grades table, then find students missing grades.",
                "Variation 5: Join a transactions table with a fraud_flags table to label suspicious transactions.",
                "Variation 6: Use left_on and right_on to merge when the key column has different names.",
                "Variation 7: Stack two years of survey data vertically and add a 'year' column before concatenating.",
                "Variation 8: Merge on multiple columns simultaneously using on=['year','region'].",
                "Variation 9: After merging, check for NaN rows to identify unmatched records.",
                "Variation 10: Merge a product catalog with inventory data and flag out-of-stock items."
            ]
        },
        {
            "id": "m2-l12",
            "title": "Pivot Tables — Summarizing Data Like Excel",
            "order": 12,
            "duration_min": 20,
            "real_world_context": "Pivot tables are one of the most-used tools in business analytics. Excel users do this constantly — Python's version is faster, scriptable, and handles millions of rows.",
            "concept": """A **pivot table** reshapes data from long format (many rows) into a summarized wide format — grouping and aggregating in two dimensions simultaneously.

```python
import pandas as pd

sales = pd.DataFrame({
    "region":  ["North","North","South","South","East","East"],
    "product": ["Laptop","Phone","Laptop","Phone","Laptop","Phone"],
    "quarter": ["Q1","Q2","Q1","Q2","Q1","Q2"],
    "revenue": [45000, 32000, 38000, 29000, 41000, 27000]
})

# Basic pivot table: revenue by region (rows) and product (columns)
pivot = pd.pivot_table(
    sales,
    values="revenue",
    index="region",
    columns="product",
    aggfunc="sum"
)
print(pivot)
# product   Laptop   Phone
# region
# East       41000   27000
# North      45000   32000
# South      38000   29000
```

**aggfunc options:**
```python
aggfunc="sum"    # total
aggfunc="mean"   # average
aggfunc="count"  # how many records
aggfunc="max"    # maximum value
```

**Adding row/column totals with margins:**
```python
pivot = pd.pivot_table(
    sales, values="revenue", index="region",
    columns="product", aggfunc="sum",
    margins=True, margins_name="Total"
)
# Adds a 'Total' row and column automatically
```

**pd.crosstab() — counting occurrences:**
```python
# How many sales transactions per region per product?
ct = pd.crosstab(sales["region"], sales["product"])
print(ct)
# product  Laptop  Phone
# region
# East          1      1
# North         1      1
# South         1      1
```

**Key difference:** `pivot_table` aggregates numeric values (sum, mean). `crosstab` counts occurrences (frequencies).""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd

# Customer purchase log
data = {
    "customer": ["Alice","Bob","Alice","Carol","Bob","Carol","Alice"],
    "category": ["Electronics","Clothing","Clothing","Electronics","Electronics","Clothing","Electronics"],
    "amount":   [1200, 85, 150, 980, 320, 120, 750]
}
df = pd.DataFrame(data)

# Pivot: total spend per customer (rows) by category (columns)
pivot = pd.pivot_table(
    df, values="amount", index="customer",
    columns="category", aggfunc="sum", fill_value=0,
    margins=True, margins_name="Total"
)
print(pivot)
# category  Clothing  Electronics  Total
# customer
# Alice          150         1950   2100
# Bob             85          320    405
# Carol          120          980   1100
# Total          355         3250   3605

# Who spent the most overall?
print("Top customer:", pivot["Total"].drop("Total").idxmax())
# Top customer: Alice""",
                "explanation": "pivot_table's fill_value=0 replaces NaN with 0 where a customer had no purchases in that category. margins=True adds the totals row/column automatically. We drop the 'Total' row before calling idxmax() so we only compare real customers."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "pd.pivot_table(df, values='col', index='row_col', columns='col_col', aggfunc='sum')",
                    "fill_value=0  # replace NaN",
                    "margins=True  # add totals",
                    "pd.crosstab(df['col1'], df['col2'])  # count frequencies"
                ],
                "notes": "Use pivot_table for numeric aggregation (sum, mean, count). Use crosstab when you simply want to count how many times combinations appear."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does margins=True add to a pivot table?",
                    "options": [
                        "A) A chart of the data",
                        "B) Row and column totals",
                        "C) Percentage columns",
                        "D) A second aggregation function"
                    ],
                    "answer": 1,
                    "explanation": "margins=True appends a 'All' row at the bottom and 'All' column on the right (or whatever name you set with margins_name=) showing the grand totals."
                },
                {
                    "type": "true_false",
                    "question": "pd.crosstab() is typically used to count the frequency of combinations between two categorical columns.",
                    "answer": True,
                    "explanation": "crosstab counts how many times each combination of two categorical variables appears. It's great for contingency tables and frequency analysis."
                },
                {
                    "type": "fill_blank",
                    "question": "In pivot_table, use ___ to replace missing combinations with 0 instead of NaN",
                    "template": "pd.pivot_table(df, values='sales', index='region', columns='product', aggfunc='sum', ___=0)",
                    "answer": "fill_value",
                    "explanation": "fill_value=0 replaces NaN (no data for that combination) with 0, making the table cleaner and arithmetic possible."
                }
            ],
            "challenge": {
                "instructions": "Using the retail transactions below, create a pivot table showing total revenue by store (rows) and product category (columns). Add margins for totals. Then use crosstab to count the number of transactions per store per category. Print both tables.",
                "starter_code": "import pandas as pd\n\ndata = {\n    'store':    ['A','A','B','B','A','C','C','B','A','C'],\n    'category': ['Electronics','Clothing','Electronics','Food','Food','Clothing','Electronics','Clothing','Electronics','Food'],\n    'revenue':  [500,120,430,85,60,95,380,110,610,75]\n}\ndf = pd.DataFrame(data)\n\n# Pivot table: revenue by store and category with totals\n\n# Crosstab: transaction count by store and category\n",
                "tests": [
                    {"type": "code_contains", "value": "pivot_table"},
                    {"type": "code_contains", "value": "crosstab"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\ndata = {'store':['A','A','B','B','A','C','C','B','A','C'],'category':['Electronics','Clothing','Electronics','Food','Food','Clothing','Electronics','Clothing','Electronics','Food'],'revenue':[500,120,430,85,60,95,380,110,610,75]}\ndf = pd.DataFrame(data)\npivot = pd.pivot_table(df, values='revenue', index='store', columns='category', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')\nprint('Revenue Pivot:')\nprint(pivot)\nct = pd.crosstab(df['store'], df['category'])\nprint('Transaction Count:')\nprint(ct)"
            },
            "challenge_variations": [
                "Variation 1: Build a pivot table of average order value by sales rep (rows) and month (columns).",
                "Variation 2: Use aggfunc='count' to see how many transactions each region had per product.",
                "Variation 3: Use crosstab with normalize=True to get row percentages instead of raw counts.",
                "Variation 4: Create a pivot table with two aggfuncs (sum and mean) simultaneously.",
                "Variation 5: Pivot survey data to see average satisfaction score by department and question.",
                "Variation 6: Use a pivot table to compare Q1 vs Q2 performance by region.",
                "Variation 7: Build a pivot table then plot it as a heatmap using seaborn.",
                "Variation 8: Pivot employee headcount by department and job level.",
                "Variation 9: Use pivot_table with observed=True on categorical columns to avoid empty categories.",
                "Variation 10: Build a pivot table then export it to Excel with formatting using openpyxl."
            ]
        },
        {
            "id": "m2-l13",
            "title": "Time Series Data — Working with Dates",
            "order": 13,
            "duration_min": 25,
            "real_world_context": "Almost every business metric is time-stamped — sales by day, website visits per hour, stock prices. Time series analysis is a core skill for any analyst.",
            "concept": """**Time series data** has a datetime index. Pandas has powerful built-in tools to work with dates, resample data to different frequencies, and compute rolling averages.

**Converting strings to dates:**
```python
import pandas as pd

df = pd.DataFrame({
    "date":    ["2024-01-15", "2024-02-03", "2024-03-22"],
    "revenue": [12000, 15000, 11000]
})

df["date"] = pd.to_datetime(df["date"])
print(df["date"].dtype)  # datetime64[ns]
```

**DatetimeIndex — making dates the index:**
```python
df = df.set_index("date")
print(df.index)
# DatetimeIndex(['2024-01-15', '2024-02-03', '2024-03-22'], dtype='datetime64[ns]')

# Filter by date range
df["2024-02":"2024-03"]        # Feb through Mar
df.loc["2024-01-15"]           # specific date
```

**Extracting date parts:**
```python
df["year"]    = df.index.year
df["month"]   = df.index.month
df["weekday"] = df.index.day_name()  # 'Monday', 'Tuesday'...
```

**Resampling — aggregating to a different frequency:**
```python
# Generate daily data
dates = pd.date_range("2024-01-01", periods=90, freq="D")
daily = pd.DataFrame({"sales": range(90)}, index=dates)

# Resample to monthly totals
monthly = daily["sales"].resample("ME").sum()
print(monthly)
# 2024-01-31    465
# 2024-02-29    1334
# 2024-03-31    2325

# Weekly average
weekly = daily["sales"].resample("W").mean()
```

**Rolling average — smooth out noise:**
```python
# 7-day rolling average (smooth the data)
daily["rolling_7"] = daily["sales"].rolling(window=7).mean()

# Compare raw vs smoothed
print(daily.tail(10))
```

**Why rolling averages matter in business:** Raw daily sales data is noisy. A 7-day or 30-day rolling average smooths out weekday effects and reveals the true trend.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import matplotlib.pyplot as plt

# Monthly e-commerce revenue
data = {
    "date":    pd.date_range("2023-01-01", periods=12, freq="MS"),
    "revenue": [42000, 38000, 45000, 51000, 48000, 55000,
                62000, 58000, 53000, 67000, 72000, 89000]
}
df = pd.DataFrame(data).set_index("date")

# Month-over-month growth
df["mom_growth"] = df["revenue"].pct_change() * 100

# 3-month rolling average
df["rolling_3m"] = df["revenue"].rolling(window=3).mean()

# Best and worst months
print("Best month:", df["revenue"].idxmax().strftime("%B %Y"))
print("Worst month:", df["revenue"].idxmin().strftime("%B %Y"))

# Which quarter had most revenue
df["quarter"] = df.index.quarter
quarterly = df.groupby("quarter")["revenue"].sum()
print("Revenue by quarter:")
print(quarterly)

plt.plot(df.index, df["revenue"], label="Monthly", alpha=0.5)
plt.plot(df.index, df["rolling_3m"], label="3-month avg", linewidth=2)
plt.title("E-commerce Revenue 2023")
plt.legend()
plt.show()""",
                "explanation": "pct_change() computes the percentage change from the previous row — perfect for month-over-month growth. strftime('%B %Y') formats a datetime as 'January 2023'. rolling(3).mean() computes a moving average over the last 3 months, showing the trend rather than the noise."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "pd.to_datetime(df['col'])",
                    "df.set_index('date_col')  # DatetimeIndex",
                    "pd.date_range('2024-01-01', periods=12, freq='MS')",
                    "df.resample('ME').sum()  # monthly totals",
                    "df['col'].rolling(window=7).mean()"
                ],
                "notes": "Common resample frequencies: 'D'=daily, 'W'=weekly, 'ME'=month end, 'MS'=month start, 'QE'=quarter end, 'YE'=year end."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does df['sales'].rolling(window=7).mean() compute?",
                    "options": [
                        "A) The total sales over 7 days",
                        "B) A 7-day moving average at each point",
                        "C) Sales every 7th day",
                        "D) The mean of the last 7 rows only"
                    ],
                    "answer": 1,
                    "explanation": "rolling(window=7).mean() computes the average of the current row and the 6 preceding rows at every point in the Series — a moving (rolling) average that smooths out short-term fluctuations."
                },
                {
                    "type": "true_false",
                    "question": "pd.to_datetime() can convert string columns like '2024-01-15' into datetime objects.",
                    "answer": True,
                    "explanation": "pd.to_datetime() parses strings in many date formats into pandas datetime64 objects, enabling date arithmetic, filtering, and resampling."
                },
                {
                    "type": "fill_blank",
                    "question": "Resample a daily DataFrame to get monthly totals",
                    "template": "monthly = df['revenue'].resample('___').sum()",
                    "answer": "ME",
                    "explanation": "'ME' stands for Month End — the last day of each month. Use 'MS' for Month Start. After resampling, sum() aggregates all values within each period."
                }
            ],
            "challenge": {
                "instructions": "You have 365 days of daily store sales. Set the date column as the index. Compute: (1) monthly total sales using resample, (2) a 30-day rolling average, (3) which month had the highest total sales, (4) the day of the week with the highest average sales.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndates = pd.date_range('2024-01-01', periods=365, freq='D')\n# Weekends sell more — simulate that pattern\nsales = np.random.randint(500, 2000, 365)\ndf = pd.DataFrame({'date': dates, 'sales': sales})\n\n# Set date as index\n\n# Monthly totals\n\n# 30-day rolling average\n\n# Month with highest sales\n\n# Average sales by day of week\n",
                "tests": [
                    {"type": "code_contains", "value": "resample"},
                    {"type": "code_contains", "value": "rolling"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\ndates = pd.date_range('2024-01-01', periods=365, freq='D')\nsales = np.random.randint(500, 2000, 365)\ndf = pd.DataFrame({'date': dates, 'sales': sales})\ndf = df.set_index('date')\nmonthly = df['sales'].resample('ME').sum()\nprint('Monthly totals:')\nprint(monthly)\ndf['rolling_30'] = df['sales'].rolling(30).mean()\nprint('Best month:', monthly.idxmax().strftime('%B %Y'))\ndf['weekday'] = df.index.day_name()\nprint('Avg by weekday:')\nprint(df.groupby('weekday')['sales'].mean().sort_values(ascending=False))"
            },
            "challenge_variations": [
                "Variation 1: Find weeks where a stock price was above its 50-day moving average.",
                "Variation 2: Resample hourly web traffic to daily totals and plot a line chart.",
                "Variation 3: Compute year-over-year growth for monthly revenue data.",
                "Variation 4: Use pct_change() to find which month had the biggest sales jump.",
                "Variation 5: Filter a DatetimeIndex to only show Q4 data (October-December).",
                "Variation 6: Compare rolling 7-day vs 30-day averages on the same chart.",
                "Variation 7: Calculate cumulative revenue over the year using .cumsum().",
                "Variation 8: Find the longest consecutive streak of days with positive sales growth.",
                "Variation 9: Use resample to compute the maximum daily sale in each week.",
                "Variation 10: Create a heatmap showing average sales by month and day-of-week."
            ]
        },
        {
            "id": "m2-l14",
            "title": "Advanced Visualization — Professional Charts",
            "order": 14,
            "duration_min": 25,
            "real_world_context": "In a business analytics program you will present charts to professors, classmates, and eventually executives. Professional, polished visuals communicate your findings and signal your competence.",
            "concept": """Beyond basic charts, professional analysts use multi-panel layouts, heatmaps, and consistent styling to make their visualizations presentation-ready.

**Subplots — multiple charts in one figure:**
```python
import matplotlib.pyplot as plt
import pandas as pd

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Chart 1: bar chart on left
axes[0].bar(["Q1","Q2","Q3","Q4"], [42, 55, 61, 78])
axes[0].set_title("Quarterly Revenue")
axes[0].set_ylabel("Revenue ($000)")

# Chart 2: line chart on right
axes[1].plot(range(12), range(12), marker="o")
axes[1].set_title("Monthly Trend")

plt.tight_layout()   # prevent overlapping
plt.savefig("dashboard.png", dpi=150)
plt.show()
```

**Figure size — making charts presentation-ready:**
```python
# Widescreen for presentations
plt.figure(figsize=(16, 6))

# Square for reports
plt.figure(figsize=(8, 8))
```

**Heatmaps with seaborn:**
```python
import seaborn as sns

# Correlation heatmap — classic analytics visualization
corr = df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr,
            annot=True,      # show numbers in cells
            fmt=".2f",       # 2 decimal places
            cmap="coolwarm", # blue=negative, red=positive
            vmin=-1, vmax=1) # fix the color scale
plt.title("Correlation Matrix")
plt.show()
```

**Scatter matrix — relationships between all variables at once:**
```python
from pandas.plotting import scatter_matrix

scatter_matrix(df[["revenue","units","price","cost"]],
               figsize=(10, 10), alpha=0.5, diagonal="hist")
plt.suptitle("Pairwise Relationships")
plt.show()
```

**Styling charts for presentations:**
```python
# Use a clean style
plt.style.use("seaborn-v0_8-whitegrid")

# Custom colors
colors = ["#3b82f6","#10b981","#f59e0b","#ef4444"]

# Annotate bars with values
bars = plt.bar(categories, values, color=colors)
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.5,
             f"${val:,}", ha="center", fontsize=10, fontweight="bold")
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Regional sales by quarter
data = {
    "quarter": ["Q1","Q2","Q3","Q4"],
    "North":   [42000, 48000, 45000, 61000],
    "South":   [35000, 39000, 52000, 49000],
    "East":    [28000, 33000, 38000, 44000]
}
df = pd.DataFrame(data).set_index("quarter")

# 1. Multi-panel: bar chart + heatmap
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Grouped bar chart
df.plot(kind="bar", ax=ax1, color=["#3b82f6","#10b981","#f59e0b"])
ax1.set_title("Revenue by Quarter and Region", fontsize=14, fontweight="bold")
ax1.set_ylabel("Revenue ($)")
ax1.tick_params(axis="x", rotation=0)
ax1.legend(title="Region")

# Panel 2: Heatmap
sns.heatmap(df.T, annot=True, fmt=",", cmap="Blues", ax=ax2)
ax2.set_title("Revenue Heatmap", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig("regional_report.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved!")""",
                "explanation": "plt.subplots(1, 2) creates a 1-row, 2-column grid of axes. We pass each axis object to the chart functions using ax=. df.plot(kind='bar', ax=ax1) uses pandas' built-in plotting. The heatmap uses df.T (transpose) so regions are on the y-axis. tight_layout() prevents labels from overlapping, and bbox_inches='tight' ensures nothing is cut off when saving."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "fig, axes = plt.subplots(rows, cols, figsize=(w, h))",
                    "axes[0].bar() / axes[1].plot()",
                    "plt.tight_layout()",
                    "sns.heatmap(df.corr(), annot=True, cmap='coolwarm')",
                    "plt.savefig('file.png', dpi=150, bbox_inches='tight')"
                ],
                "notes": "Always use tight_layout() before savefig() to prevent labels being clipped. Use dpi=150 for crisp images in presentations."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does plt.tight_layout() do?",
                    "options": [
                        "A) Resizes the figure window",
                        "B) Adjusts spacing to prevent overlapping labels",
                        "C) Makes all axes the same size",
                        "D) Removes the chart title"
                    ],
                    "answer": 1,
                    "explanation": "tight_layout() automatically adjusts subplot spacing so titles, labels, and tick marks don't overlap each other — critical when making multi-panel figures."
                },
                {
                    "type": "true_false",
                    "question": "figsize=(12, 5) sets the figure width to 12 inches and height to 5 inches.",
                    "answer": True,
                    "explanation": "figsize takes a (width, height) tuple in inches. Use wider figures (e.g., 16x5) for time series and taller figures for vertical bar charts."
                },
                {
                    "type": "fill_blank",
                    "question": "Create a 2x2 grid of subplots with figure size 10x8",
                    "template": "fig, axes = plt.___(2, 2, figsize=(10, 8))",
                    "answer": "subplots",
                    "explanation": "plt.subplots(nrows, ncols) creates a grid of axes. With 2x2 you get a 2D array: axes[0][0], axes[0][1], axes[1][0], axes[1][1]."
                }
            ],
            "challenge": {
                "instructions": "Create a 3-panel figure (1 row, 3 columns). Panel 1: bar chart of sales by region. Panel 2: line chart of monthly trend. Panel 3: seaborn heatmap of a correlation matrix. Add a title to each panel, set figsize to (15, 5), call tight_layout(), and save as 'analytics_dashboard.png'.",
                "starter_code": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport numpy as np\n\n# Sales by region\nregions = ['North','South','East','West']\nsales = [45000, 38000, 52000, 29000]\n\n# Monthly trend\nmonths = range(1, 13)\ntrend = [30000 + i*2000 + np.random.randint(-1000,1000) for i in months]\n\n# Correlation data\nnp.random.seed(0)\ndf_corr = pd.DataFrame(np.random.randn(50, 4), columns=['Revenue','Cost','Units','Price'])\n\n# Create 1x3 subplot grid\n\n# Panel 1: bar chart (regions vs sales)\n\n# Panel 2: line chart (months vs trend)\n\n# Panel 3: correlation heatmap\n\n# tight_layout and save\n",
                "tests": [
                    {"type": "code_contains", "value": "subplots"},
                    {"type": "code_contains", "value": "tight_layout"},
                    {"type": "code_contains", "value": "heatmap"}
                ],
                "solution": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport numpy as np\nregions=['North','South','East','West']\nsales=[45000,38000,52000,29000]\nmonths=range(1,13)\nnp.random.seed(1)\ntrend=[30000+i*2000+np.random.randint(-1000,1000) for i in months]\ndf_corr=pd.DataFrame(np.random.randn(50,4),columns=['Revenue','Cost','Units','Price'])\nfig,axes=plt.subplots(1,3,figsize=(15,5))\naxes[0].bar(regions,sales,color='#3b82f6')\naxes[0].set_title('Sales by Region')\naxes[1].plot(list(months),trend,marker='o',color='#10b981')\naxes[1].set_title('Monthly Trend')\nsns.heatmap(df_corr.corr(),annot=True,fmt='.2f',cmap='coolwarm',ax=axes[2])\naxes[2].set_title('Correlation Matrix')\nplt.tight_layout()\nplt.savefig('analytics_dashboard.png',dpi=150)\nplt.show()"
            },
            "challenge_variations": [
                "Variation 1: Build a 2x2 dashboard with bar, line, scatter, and pie charts for a quarterly report.",
                "Variation 2: Add data labels (annotations) above each bar in a bar chart showing exact values.",
                "Variation 3: Create a seaborn pairplot for a 4-variable DataFrame colored by category.",
                "Variation 4: Style a chart using plt.style.use('ggplot') and compare to the default style.",
                "Variation 5: Create a stacked bar chart showing revenue contribution by product per region.",
                "Variation 6: Build a heatmap of pivot table results (monthly revenue by region).",
                "Variation 7: Add horizontal reference lines (plt.axhline) to a line chart showing the target.",
                "Variation 8: Use a secondary y-axis to overlay revenue and units sold on the same chart.",
                "Variation 9: Create a scatter plot with point size proportional to revenue (bubble chart).",
                "Variation 10: Generate a figure with 12 small subplots — one for each month's data distribution."
            ]
        },
        {
            "id": "m2-l15",
            "title": "Statistical Distributions — Understanding Data Shape",
            "order": 15,
            "duration_min": 20,
            "real_world_context": "Before running any statistical test or building any model, you need to understand the shape of your data. This affects which analysis methods are valid and what your results actually mean.",
            "concept": """The **distribution** of a variable describes how its values spread out. The shape matters enormously — it tells you what's normal, what's extreme, and which statistical methods are appropriate.

**Normal distribution — the bell curve:**
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# Simulate employee salaries (roughly normal)
np.random.seed(42)
salaries = np.random.normal(loc=75000, scale=12000, size=500)
# loc = mean, scale = standard deviation

plt.figure(figsize=(10, 4))
plt.hist(salaries, bins=30, edgecolor="white", color="#3b82f6", alpha=0.8)
plt.axvline(salaries.mean(), color="red", linestyle="--", label="Mean")
plt.title("Salary Distribution")
plt.legend()
plt.show()
```

**Skewness — is the tail on the left or right?**
```python
s = pd.Series(salaries)
print(f"Skewness: {s.skew():.3f}")
# Near 0 = symmetric (normal)
# Positive = right-skewed (long tail on right, e.g. income)
# Negative = left-skewed (long tail on left)
```

**Kurtosis — are there heavy tails (extreme values)?**
```python
print(f"Kurtosis: {s.kurtosis():.3f}")
# Near 0 = normal tails
# High positive = more extreme outliers than normal (heavy tails)
# Negative = fewer extremes (thin tails)
```

**Visualizing distributions:**
```python
import seaborn as sns

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Histogram
axes[0].hist(salaries, bins=30, color="#3b82f6")
axes[0].set_title("Histogram")

# Box plot — shows median, IQR, and outliers
axes[1].boxplot(salaries)
axes[1].set_title("Box Plot")

# KDE (smooth curve estimate of distribution)
sns.kdeplot(salaries, ax=axes[2], fill=True)
axes[2].set_title("KDE Plot")

plt.tight_layout()
plt.show()
```

**Why shape matters for analysis:**
- Many statistical tests assume normality
- Skewed data: use median, not mean, for "typical" value
- Income, sales volumes, and website traffic are almost always right-skewed
- Use log transformation to make skewed data more normal before modeling""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(7)

# Simulate two types of business data
# Customer spend: right-skewed (most customers spend little, a few spend a lot)
customer_spend = np.random.exponential(scale=150, size=400)

# Employee productivity scores: roughly normal
productivity = np.random.normal(loc=72, scale=10, size=400)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Histograms
axes[0,0].hist(customer_spend, bins=30, color="#f59e0b")
axes[0,0].set_title(f"Customer Spend  (skew={pd.Series(customer_spend).skew():.2f})")

axes[0,1].hist(productivity, bins=20, color="#3b82f6")
axes[0,1].set_title(f"Productivity  (skew={pd.Series(productivity).skew():.2f})")

# Box plots
axes[1,0].boxplot(customer_spend)
axes[1,0].set_title("Spend Boxplot")

axes[1,1].boxplot(productivity)
axes[1,1].set_title("Productivity Boxplot")

plt.tight_layout()
plt.show()

# Compare mean vs median for skewed data
print(f"Spend — mean: ${customer_spend.mean():.0f}, median: ${np.median(customer_spend):.0f}")
print(f"The mean is much higher due to big spenders — use median for 'typical' customer")""",
                "explanation": "The exponential distribution mimics real customer spend data — right-skewed because a small number of customers spend far more than average. The positive skew value (well above 0) confirms this. Notice how the mean is much higher than the median — a few big spenders pull the mean up. For reporting 'typical' customer spend, the median is more honest."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "s.skew()  # positive=right-skewed, negative=left-skewed",
                    "s.kurtosis()  # >0 means heavier tails",
                    "np.random.normal(loc=mean, scale=std, size=n)",
                    "plt.hist(data, bins=30)",
                    "sns.kdeplot(data, fill=True)"
                ],
                "notes": "Skewness near 0 and kurtosis near 0 suggest a normal distribution. Income, prices, and web traffic are typically right-skewed — always check before choosing mean vs median."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A distribution has skewness of 2.3. What does this mean?",
                    "options": [
                        "A) The data is symmetric",
                        "B) The data has a long tail on the right side",
                        "C) The data has a long tail on the left side",
                        "D) The data has no outliers"
                    ],
                    "answer": 1,
                    "explanation": "Positive skewness means the right tail is longer — most values are low but a few very high values pull the mean up. Income distribution is a classic example."
                },
                {
                    "type": "true_false",
                    "question": "For right-skewed data (like income), the median is a better measure of 'typical' than the mean.",
                    "answer": True,
                    "explanation": "The mean is pulled toward the long tail by extreme values. The median (middle value) is unaffected by a few very large numbers, making it a better representation of the typical value."
                },
                {
                    "type": "fill_blank",
                    "question": "Calculate the skewness of a pandas Series s",
                    "template": "skew_val = s.___( )",
                    "answer": "skew()",
                    "explanation": ".skew() returns a float: positive means right-skewed, negative means left-skewed, near 0 means roughly symmetric."
                }
            ],
            "challenge": {
                "instructions": "Generate three datasets: (1) normal distribution (mean=50, std=10, n=500), (2) right-skewed exponential (scale=20, n=500), (3) uniform distribution (low=0, high=100, n=500). For each: print mean, median, and skewness. Then create a 1x3 histogram plot showing all three distributions side by side.",
                "starter_code": "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\nnp.random.seed(99)\n\n# Generate datasets\nnormal_data = np.random.normal(50, 10, 500)\nskewed_data = np.random.exponential(20, 500)\nuniform_data = np.random.uniform(0, 100, 500)\n\n# Print stats for each\nfor name, data in [('Normal', normal_data), ('Skewed', skewed_data), ('Uniform', uniform_data)]:\n    s = pd.Series(data)\n    # Print mean, median, skewness\n    pass\n\n# Create 1x3 histogram subplot\n",
                "tests": [
                    {"type": "code_contains", "value": "skew"},
                    {"type": "code_contains", "value": "subplots"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nnp.random.seed(99)\nnormal_data=np.random.normal(50,10,500)\nskewed_data=np.random.exponential(20,500)\nuniform_data=np.random.uniform(0,100,500)\nfor name,data in[('Normal',normal_data),('Skewed',skewed_data),('Uniform',uniform_data)]:\n    s=pd.Series(data)\n    print(f'{name}: mean={s.mean():.1f}, median={s.median():.1f}, skew={s.skew():.2f}')\nfig,axes=plt.subplots(1,3,figsize=(15,4))\nfor ax,data,title in zip(axes,[normal_data,skewed_data,uniform_data],['Normal','Skewed','Uniform']):\n    ax.hist(data,bins=30,color='#3b82f6',edgecolor='white')\n    ax.set_title(title)\nplt.tight_layout()\nplt.show()"
            },
            "challenge_variations": [
                "Variation 1: Plot a histogram of product prices from a retail dataset and describe the distribution.",
                "Variation 2: Compare salary distributions across two departments using overlapping KDE plots.",
                "Variation 3: Apply a log transformation to right-skewed revenue data and compare before/after skewness.",
                "Variation 4: Use a Q-Q plot (scipy.stats.probplot) to test if data is normally distributed.",
                "Variation 5: Create a box plot comparing distributions of sales across 4 regions.",
                "Variation 6: Simulate a bimodal distribution (mix of two normal curves) and explain what it means.",
                "Variation 7: Compute skewness and kurtosis for all numeric columns in a DataFrame at once.",
                "Variation 8: Overlay a theoretical normal curve on top of a histogram using scipy.stats.norm.",
                "Variation 9: Plot customer ages from a retail database and identify the primary demographic.",
                "Variation 10: Compare distributions of delivery times before and after a logistics improvement."
            ]
        },
        {
            "id": "m2-l16",
            "title": "Hypothesis Testing Basics — Is This Difference Real?",
            "order": 16,
            "duration_min": 25,
            "real_world_context": "Your manager says the new checkout page increased conversions. Your A/B test shows a small difference. Is it real, or just random noise? Hypothesis testing gives you a rigorous answer — and it's a core skill in every analytics role.",
            "concept": """**Hypothesis testing** is a statistical method to decide if an observed difference is real or could have happened by chance.

**The framework:**
1. **Null hypothesis (H0):** There is NO real difference (any difference is due to random chance)
2. **Alternative hypothesis (H1):** There IS a real difference
3. **p-value:** The probability of seeing this result if H0 were true
4. **Decision rule:** If p-value < 0.05, reject H0 (the result is statistically significant)

```python
from scipy import stats
import numpy as np

# A/B test: did a new email subject line increase open rates?
# Group A (old): open rates for 30 days
# Group B (new): open rates for 30 days
np.random.seed(42)
group_a = np.random.normal(22, 4, 30)  # ~22% open rate
group_b = np.random.normal(25, 4, 30)  # ~25% open rate

t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value:     {p_value:.4f}")

if p_value < 0.05:
    print("Result: SIGNIFICANT — the new subject line really works")
else:
    print("Result: NOT significant — the difference could be random")
```

**Understanding the p-value intuitively:**
- p = 0.001 means there's a 0.1% chance this result is just random luck — very confident it's real
- p = 0.45 means there's a 45% chance this result is just random luck — not convincing at all
- **0.05 is the standard threshold** (5% false positive rate)

**Practical business application:**
```python
# Did marketing campaign increase average order value?
before_campaign = [85, 92, 78, 88, 95, 71, 83, 90, 76, 88]
after_campaign  = [94, 103, 88, 97, 108, 85, 91, 99, 87, 101]

t_stat, p_value = stats.ttest_ind(before_campaign, after_campaign)
print(f"Before average: ${np.mean(before_campaign):.2f}")
print(f"After average:  ${np.mean(after_campaign):.2f}")
print(f"p-value: {p_value:.4f}")
print(f"Significant: {p_value < 0.05}")
```

**Important caveat:** Statistical significance ≠ business significance. A difference can be statistically significant but too small to matter practically. Always report both the p-value and the actual effect size (difference in means).""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

np.random.seed(10)

# Scenario: Does a 10% discount coupon increase purchase rate?
# We tracked 50 customers each: one group got coupon, one didn't
# Metric: total spend during the 30-day period

no_coupon = np.random.normal(loc=120, scale=25, size=50)
with_coupon = np.random.normal(loc=138, scale=28, size=50)

# Run the t-test
t_stat, p_value = stats.ttest_ind(no_coupon, with_coupon)

print("=== Coupon A/B Test Results ===")
print(f"No coupon  — mean spend: ${no_coupon.mean():.2f}")
print(f"With coupon — mean spend: ${with_coupon.mean():.2f}")
print(f"Difference: ${with_coupon.mean() - no_coupon.mean():.2f}")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print()
if p_value < 0.05:
    print("CONCLUSION: The coupon significantly increases spend (p < 0.05).")
    print(f"Recommend rolling out to all customers.")
else:
    print("CONCLUSION: No significant difference detected (p >= 0.05).")
    print("Need more data or a larger promotion.")

# Visualize
plt.figure(figsize=(8, 4))
plt.hist(no_coupon, alpha=0.6, label="No Coupon", bins=15)
plt.hist(with_coupon, alpha=0.6, label="With Coupon", bins=15)
plt.axvline(no_coupon.mean(), color="blue", linestyle="--")
plt.axvline(with_coupon.mean(), color="orange", linestyle="--")
plt.legend()
plt.title(f"Spend Distribution (p={p_value:.4f})")
plt.show()""",
                "explanation": "ttest_ind compares two independent groups. We print the actual means alongside the p-value — because reporting 'p=0.03' without saying 'the average spend increased by $18' is incomplete. The visualization shows the overlap between groups; heavy overlap with a low p-value means the effect is real but subtle."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "from scipy import stats",
                    "t_stat, p_value = stats.ttest_ind(group_a, group_b)",
                    "p_value < 0.05  # standard significance threshold",
                    "H0: no difference  |  H1: there is a difference"
                ],
                "notes": "ttest_ind is for two independent groups. For before/after measurements on the SAME subjects, use stats.ttest_rel (paired t-test). Always report effect size (actual difference), not just p-value."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A p-value of 0.03 means:",
                    "options": [
                        "A) There is a 3% chance the groups are different",
                        "B) The result is 97% accurate",
                        "C) There is a 3% chance of seeing this result if there were truly no difference",
                        "D) The null hypothesis is true"
                    ],
                    "answer": 2,
                    "explanation": "The p-value is the probability of observing your result (or more extreme) assuming H0 (no difference) is true. p=0.03 means there's only a 3% chance the result is random — so we reject H0."
                },
                {
                    "type": "true_false",
                    "question": "A result can be statistically significant (p < 0.05) but still not be practically meaningful for a business decision.",
                    "answer": True,
                    "explanation": "With large enough sample sizes, even tiny, irrelevant differences become 'statistically significant'. Always check the actual effect size — a $0.05 average increase might be statistically significant but not worth acting on."
                },
                {
                    "type": "fill_blank",
                    "question": "Import the stats module from scipy",
                    "template": "from scipy ___ stats",
                    "answer": "import",
                    "explanation": "'from scipy import stats' gives you access to stats.ttest_ind(), stats.norm, stats.pearsonr(), and hundreds of other statistical functions."
                }
            ],
            "challenge": {
                "instructions": "A retail chain tested a new store layout in 10 stores while 10 stores kept the old layout. Run a t-test to determine if the new layout significantly increased average daily sales. Print the means for both groups, the p-value, and a clear business recommendation.",
                "starter_code": "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(5)\n\n# Average daily sales over 30 days\nold_layout = np.random.normal(loc=3200, scale=400, size=10)\nnew_layout = np.random.normal(loc=3600, scale=420, size=10)\n\n# Run t-test\n\n# Print results\n\n# Print business recommendation based on p-value\n",
                "tests": [
                    {"type": "code_contains", "value": "ttest_ind"},
                    {"type": "code_contains", "value": "p_value"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import numpy as np\nfrom scipy import stats\nnp.random.seed(5)\nold_layout=np.random.normal(loc=3200,scale=400,size=10)\nnew_layout=np.random.normal(loc=3600,scale=420,size=10)\nt_stat,p_value=stats.ttest_ind(old_layout,new_layout)\nprint(f'Old layout avg: ${old_layout.mean():.0f}/day')\nprint(f'New layout avg: ${new_layout.mean():.0f}/day')\nprint(f'p-value: {p_value:.4f}')\nif p_value<0.05:\n    print('RECOMMENDATION: New layout significantly increases sales. Roll out chain-wide.')\nelse:\n    print('RECOMMENDATION: Difference not statistically significant. Collect more data.')"
            },
            "challenge_variations": [
                "Variation 1: A/B test two different pricing strategies on customer conversion rates.",
                "Variation 2: Test whether male and female employees have significantly different promotion rates.",
                "Variation 3: Compare customer satisfaction scores before and after a service improvement (paired t-test).",
                "Variation 4: Determine if Q4 sales are significantly higher than Q3 across 20 store locations.",
                "Variation 5: Test if a new onboarding flow reduces time-to-first-purchase significantly.",
                "Variation 6: Run a hypothesis test on delivery times: same-day vs standard shipping satisfaction.",
                "Variation 7: Test if premium members spend significantly more than free tier members.",
                "Variation 8: Compare website session durations for mobile vs desktop users.",
                "Variation 9: Determine if a training program significantly improved employee performance scores.",
                "Variation 10: Test whether click-through rates differ significantly between two ad creatives."
            ]
        },
        {
            "id": "m2-l17",
            "title": "Correlation Deep Dive — Finding Relationships",
            "order": 17,
            "duration_min": 20,
            "real_world_context": "One of the most common questions in business analytics is 'what factors drive our sales?' Correlation analysis is the first step to answering that — but you must understand its limits.",
            "concept": """**Correlation** measures the strength and direction of the linear relationship between two variables. It ranges from -1.0 to +1.0.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sales data with multiple potential drivers
df = pd.DataFrame({
    "ad_spend":     [1000, 2500, 1800, 3200, 900, 2100, 2800, 1500],
    "store_size":   [500,  1200, 800,  1500, 400, 1000, 1300, 700],
    "staff_hours":  [40,   80,   60,   90,   35,  70,   85,   55],
    "revenue":      [8000, 18000, 13000, 22000, 7000, 15000, 20000, 11000]
})

# Full correlation matrix
print(df.corr())

# Single correlation
r = df["ad_spend"].corr(df["revenue"])
print(f"ad_spend ↔ revenue: {r:.3f}")
# 0.999 = nearly perfect positive correlation
```

**Pearson vs Spearman:**
```python
from scipy import stats

# Pearson: measures LINEAR relationship (assumes normal distribution)
r_p, p_p = stats.pearsonr(df["ad_spend"], df["revenue"])
print(f"Pearson r={r_p:.3f}, p={p_p:.4f}")

# Spearman: measures RANK-ORDER relationship (works for non-linear, skewed data)
r_s, p_s = stats.spearmanr(df["ad_spend"], df["revenue"])
print(f"Spearman r={r_s:.3f}, p={p_s:.4f}")
```

**Use Spearman** when your data is skewed, has outliers, or the relationship might be non-linear (common in business data).

**Correlation matrix heatmap:**
```python
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(),
            annot=True, fmt=".2f",
            cmap="coolwarm",
            vmin=-1, vmax=1,
            square=True)
plt.title("Correlation Matrix — What Drives Revenue?")
plt.show()
```

**Spurious correlations:**
Ice cream sales and drowning deaths are correlated (both rise in summer) — but ice cream doesn't cause drowning. The hidden driver is **summer heat**.

**Correlation ≠ Causation. Always ask:** Is there a third variable (confounder) that explains both?""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
n = 50

# Create a realistic marketing dataset
ad_spend = np.random.uniform(500, 5000, n)
# Revenue is roughly ad_spend * 5 + noise
revenue = ad_spend * 5.2 + np.random.normal(0, 1500, n)
# Temperature: unrelated (but common confounder in retail)
temperature = np.random.uniform(60, 95, n)
# Staff count: slightly related to revenue
staff = np.round(revenue / 4000 + np.random.normal(0, 1, n)).clip(3, 12)

df = pd.DataFrame({
    "ad_spend": ad_spend,
    "revenue": revenue,
    "temperature": temperature,
    "staff": staff
})

# Full correlation matrix
corr_matrix = df.corr()
print("Correlation with Revenue:")
print(corr_matrix["revenue"].sort_values(ascending=False))

# Scatter plot: ad_spend vs revenue
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.scatter(df["ad_spend"], df["revenue"], alpha=0.6, color="#3b82f6")
r, p = stats.pearsonr(df["ad_spend"], df["revenue"])
plt.title(f"Ad Spend vs Revenue (r={r:.2f}, p={p:.3f})")
plt.xlabel("Ad Spend ($)")
plt.ylabel("Revenue ($)")

plt.subplot(1, 2, 2)
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()""",
                "explanation": "We print correlations with revenue sorted so the strongest drivers are obvious. Ad spend has a strong positive correlation (~0.95), staff has a moderate correlation, and temperature is near zero (unrelated — as expected). The scatter plot lets you visually confirm the linear relationship before trusting the correlation coefficient."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "df.corr()  # full correlation matrix",
                    "df['a'].corr(df['b'])  # single pair",
                    "stats.pearsonr(x, y)  # returns (r, p-value)",
                    "stats.spearmanr(x, y)  # rank-order correlation",
                    "sns.heatmap(df.corr(), annot=True, cmap='coolwarm')"
                ],
                "notes": "Pearson assumes linearity and normality. Spearman is more robust for skewed or non-linear data. A p-value alongside r tells you if the correlation is statistically significant."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Pearson correlation of -0.82 between 'price' and 'units_sold' means:",
                    "options": [
                        "A) Higher price causes lower sales",
                        "B) Price and sales are unrelated",
                        "C) As price increases, units sold tend to decrease (strong negative relationship)",
                        "D) Sales cause prices to fall"
                    ],
                    "answer": 2,
                    "explanation": "-0.82 is a strong negative correlation: as price goes up, units sold tend to go down. But correlation doesn't prove causation — always interpret with domain knowledge."
                },
                {
                    "type": "true_false",
                    "question": "A high correlation between two variables proves that one causes the other.",
                    "answer": False,
                    "explanation": "Correlation ≠ causation. Both variables might be driven by a third (confounding) variable. For example, shoe size and reading ability correlate strongly in children — but only because both are driven by age."
                },
                {
                    "type": "fill_blank",
                    "question": "Calculate Pearson correlation and p-value between arrays x and y using scipy",
                    "template": "r, p = stats.___(x, y)",
                    "answer": "pearsonr",
                    "explanation": "stats.pearsonr(x, y) returns a tuple (correlation_coefficient, p_value). The p-value tells you whether the correlation is statistically significant."
                }
            ],
            "challenge": {
                "instructions": "Using the customer data below, compute the full correlation matrix and visualize it as a heatmap. Then identify: (1) which variable has the strongest positive correlation with 'revenue', (2) which variable has the strongest negative correlation with 'revenue', (3) print a business insight summary.",
                "starter_code": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom scipy import stats\n\nnp.random.seed(0)\nn = 100\ndf = pd.DataFrame({\n    'ad_spend':    np.random.uniform(1000, 10000, n),\n    'price':       np.random.uniform(20, 200, n),\n    'store_age':   np.random.randint(1, 20, n),\n    'staff_count': np.random.randint(5, 30, n),\n    'revenue':     None  # will compute below\n})\n# Revenue driven by ad_spend and staff, hurt by high price\ndf['revenue'] = (df['ad_spend'] * 3.5 + df['staff_count'] * 500\n                 - df['price'] * 50 + np.random.normal(0, 2000, n))\n\n# Compute and print correlation matrix\n\n# Heatmap\n\n# Identify strongest positive and negative correlation with revenue\n",
                "tests": [
                    {"type": "code_contains", "value": ".corr()"},
                    {"type": "code_contains", "value": "heatmap"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nnp.random.seed(0)\nn=100\ndf=pd.DataFrame({'ad_spend':np.random.uniform(1000,10000,n),'price':np.random.uniform(20,200,n),'store_age':np.random.randint(1,20,n),'staff_count':np.random.randint(5,30,n),'revenue':None})\ndf['revenue']=df['ad_spend']*3.5+df['staff_count']*500-df['price']*50+np.random.normal(0,2000,n)\ncorr=df.corr()\nprint(corr)\nplt.figure(figsize=(8,6))\nsns.heatmap(corr,annot=True,fmt='.2f',cmap='coolwarm',vmin=-1,vmax=1)\nplt.title('Correlation Matrix')\nplt.show()\nrev_corr=corr['revenue'].drop('revenue').sort_values()\nprint('Strongest negative correlation with revenue:',rev_corr.index[0])\nprint('Strongest positive correlation with revenue:',rev_corr.index[-1])"
            },
            "challenge_variations": [
                "Variation 1: Compute correlations between all marketing channels and conversion rate.",
                "Variation 2: Use Spearman correlation on skewed sales data and compare to Pearson results.",
                "Variation 3: Identify and explain a spurious correlation in a given business dataset.",
                "Variation 4: Build a correlation heatmap for a customer satisfaction survey dataset.",
                "Variation 5: Find which product features most strongly correlate with customer rating.",
                "Variation 6: Compute rolling 30-day correlations between two time series variables.",
                "Variation 7: Filter the correlation matrix to show only pairs with |r| > 0.7.",
                "Variation 8: Test whether a correlation is statistically significant using scipy.stats.pearsonr.",
                "Variation 9: Compare correlation matrices for two different market segments.",
                "Variation 10: Create a scatter matrix for 5 business variables and annotate with correlation values."
            ]
        },
        {
            "id": "m2-l18",
            "title": "Outlier Detection — Finding the Weird Data",
            "order": 18,
            "duration_min": 20,
            "real_world_context": "A single data entry error — a salary of $9,000,000 instead of $90,000 — can completely distort your analysis. Detecting and handling outliers is essential before reporting any results.",
            "concept": """**Outliers** are data points that fall far from the rest of the data. They can be data entry errors, fraud signals, or genuinely unusual events — you need to investigate before deciding what to do.

**Method 1: IQR (Interquartile Range) — the standard approach:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "salary": [55000, 62000, 58000, 71000, 65000,
               69000, 980000, 57000, 63000, 60000]  # 980000 is the outlier
})

Q1 = df["salary"].quantile(0.25)
Q3 = df["salary"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["salary"] < lower_bound) | (df["salary"] > upper_bound)]
print(f"Outliers found: {len(outliers)}")
print(outliers)
# Flags the 980000 entry

# Clean data (remove outliers)
df_clean = df[(df["salary"] >= lower_bound) & (df["salary"] <= upper_bound)]
```

**Method 2: Z-score — how many standard deviations from the mean?**
```python
from scipy import stats

z_scores = stats.zscore(df["salary"])
df["z_score"] = z_scores

# Flag anything beyond 3 standard deviations
outliers_z = df[abs(df["z_score"]) > 3]
print(outliers_z)
```

**Visualizing outliers with a box plot:**
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.boxplot(df["salary"])
plt.title("Box Plot — Before Cleaning")

plt.subplot(1, 2, 2)
plt.boxplot(df_clean["salary"])
plt.title("Box Plot — After Removing Outliers")
plt.show()
```

**When to REMOVE vs KEEP outliers:**
- **Remove:** If it's clearly a data entry error (salary of $9,000,000)
- **Keep:** If the outlier represents a real, important event (a viral sale day)
- **Investigate:** Contact data owner before deleting — outliers are often the most interesting data points

**Business rule of thumb:** Never remove outliers automatically. Document your decision and its rationale.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(3)

# Transaction amounts — mostly normal, a few fraud suspects
transactions = pd.Series(
    list(np.random.normal(150, 30, 95)) + [2400, 1850, 3200]  # 3 outliers
)

# IQR method
Q1, Q3 = transactions.quantile(0.25), transactions.quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

outlier_mask = (transactions < lower) | (transactions > upper)
print(f"Total transactions: {len(transactions)}")
print(f"Flagged as outliers: {outlier_mask.sum()}")
print("Outlier values:")
print(transactions[outlier_mask].values)

# Z-score method
z = stats.zscore(transactions)
z_outliers = abs(z) > 3
print(f"Z-score flags: {z_outliers.sum()}")

# Compare stats with/without outliers
print(f"Mean with outliers:    ${transactions.mean():.0f}")
print(f"Mean without outliers: ${transactions[~outlier_mask].mean():.0f}")
print(f"Impact of outliers on mean: ${transactions.mean() - transactions[~outlier_mask].mean():.0f}")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].boxplot(transactions)
axes[0].set_title("All Transactions (with outliers)")
axes[1].boxplot(transactions[~outlier_mask])
axes[1].set_title("After Flagging Outliers")
plt.tight_layout()
plt.show()""",
                "explanation": "The 3 artificially inserted high values (2400, 1850, 3200) are caught by both methods. We use ~outlier_mask (the tilde means NOT) to get clean data. Notice the mean drops significantly when outliers are removed — demonstrating exactly why you must check for them before reporting averages."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "Q1, Q3 = df['col'].quantile(0.25), df['col'].quantile(0.75)",
                    "IQR = Q3 - Q1",
                    "lower = Q1 - 1.5*IQR  /  upper = Q3 + 1.5*IQR",
                    "from scipy import stats; z = stats.zscore(data)",
                    "outliers = df[abs(z) > 3]"
                ],
                "notes": "IQR method is more robust for skewed data. Z-score assumes normality. Use |z| > 3 as the threshold (covers 99.7% of normal data). Always visualize with boxplot before and after."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "In the IQR method, the upper bound for outliers is:",
                    "options": [
                        "A) Q3 + IQR",
                        "B) Q3 + 1.5 * IQR",
                        "C) mean + 2 * std",
                        "D) Q3 + 3 * IQR"
                    ],
                    "answer": 1,
                    "explanation": "The standard IQR method uses Q3 + 1.5 * IQR as the upper fence and Q1 - 1.5 * IQR as the lower fence. Values outside these bounds are flagged as outliers. Using 3.0 * IQR catches only extreme outliers."
                },
                {
                    "type": "true_false",
                    "question": "Outliers should always be removed from a dataset before analysis.",
                    "answer": False,
                    "explanation": "Outliers should be investigated, not automatically removed. They might represent real important events (fraud, a record sales day) or data entry errors. Document your decision either way."
                },
                {
                    "type": "fill_blank",
                    "question": "Use the z-score method to find outliers beyond 3 standard deviations",
                    "template": "from scipy import stats\nz = stats.zscore(data)\noutliers = data[___(z) > 3]",
                    "answer": "abs",
                    "explanation": "abs() takes the absolute value so we catch outliers in both directions (too high AND too low). |z| > 3 means more than 3 standard deviations from the mean."
                }
            ],
            "challenge": {
                "instructions": "You have employee expense reports. Some are obviously fraudulent (unusually high). Use the IQR method to flag outliers. Print the number of flagged records, their values, and compare the mean expense with and without outliers. Then create a boxplot showing the distribution.",
                "starter_code": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nnp.random.seed(77)\n# Normal expenses + a few outliers\nexpenses = pd.Series(\n    list(np.random.normal(250, 60, 47)) + [1800, 2200, 950]\n)\n\n# IQR method: compute Q1, Q3, IQR\n\n# Define lower and upper bounds\n\n# Flag outliers\n\n# Print count and values of outliers\n\n# Compare mean with vs without outliers\n\n# Boxplot\n",
                "tests": [
                    {"type": "code_contains", "value": "quantile"},
                    {"type": "code_contains", "value": "IQR"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nnp.random.seed(77)\nexpenses=pd.Series(list(np.random.normal(250,60,47))+[1800,2200,950])\nQ1=expenses.quantile(0.25)\nQ3=expenses.quantile(0.75)\nIQR=Q3-Q1\nlower=Q1-1.5*IQR\nupper=Q3+1.5*IQR\noutlier_mask=(expenses<lower)|(expenses>upper)\nprint(f'Flagged: {outlier_mask.sum()}')\nprint('Outlier values:',expenses[outlier_mask].values)\nprint(f'Mean with outliers: ${expenses.mean():.0f}')\nprint(f'Mean without: ${expenses[~outlier_mask].mean():.0f}')\nplt.boxplot(expenses)\nplt.title('Expense Distribution')\nplt.show()"
            },
            "challenge_variations": [
                "Variation 1: Detect outliers in delivery times and investigate if they cluster on specific days.",
                "Variation 2: Flag outlier transactions in credit card data as potential fraud signals.",
                "Variation 3: Apply both IQR and z-score methods and compare which catches more outliers.",
                "Variation 4: Detect outliers in product ratings — are any suspiciously perfect or all-1-star?",
                "Variation 5: Use a boxplot grouped by region to compare outlier patterns across locations.",
                "Variation 6: Apply winsorization: cap outliers at the 1st and 99th percentile instead of removing.",
                "Variation 7: Detect outliers in a time series and annotate them on a line chart.",
                "Variation 8: Find rows that are outliers in MULTIPLE columns simultaneously.",
                "Variation 9: Compute the percentage of revenue attributable to outlier transactions.",
                "Variation 10: Build a function detect_outliers(series, method='iqr') that works for any column."
            ]
        },
        {
            "id": "m2-l19",
            "title": "Feature Engineering — Creating Better Columns",
            "order": 19,
            "duration_min": 25,
            "real_world_context": "Raw data almost never has the exact columns you need. Feature engineering — creating new, more informative columns from existing ones — is what separates mediocre analysts from great ones. It directly improves any model you build downstream.",
            "concept": """**Feature engineering** is the art of creating new variables from raw data. It helps your analysis capture patterns that weren't visible before.

**Binning — converting continuous numbers into categories:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "customer_id": range(8),
    "age": [22, 35, 48, 61, 19, 42, 55, 29],
    "spend": [120, 850, 1200, 680, 95, 1100, 920, 430]
})

# Bin ages into categories
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 25, 40, 55, 100],
    labels=["18-25", "26-40", "41-55", "55+"]
)
print(df[["age", "age_group"]])
# age  age_group
# 22   18-25
# 35   26-40
# 48   41-55
# 61   55+
```

**Encoding categories — converting text to numbers:**
```python
df["region"] = ["North","South","North","East","South","East","North","South"]

# One-hot encoding: each category becomes a 0/1 column
encoded = pd.get_dummies(df["region"], prefix="region")
print(encoded)
# region_East  region_North  region_South
#           0             1             0
#           0             0             1
# ...

df = pd.concat([df, encoded], axis=1)
```

**Creating ratio features:**
```python
# Revenue per employee — a more meaningful metric than raw revenue
df["revenue_per_staff"] = df["revenue"] / df["staff_count"]

# Conversion rate from raw funnel data
df["conversion_rate"] = df["purchases"] / df["visits"]

# Month-over-month growth
df["mom_growth"] = df["revenue"].pct_change()
```

**Log transformation — taming skewed data:**
```python
# If revenue is heavily right-skewed
df["log_revenue"] = np.log1p(df["revenue"])
# log1p = log(x+1) — safe even when x=0

# Compare distributions
print(f"Original skewness: {df['revenue'].skew():.2f}")
print(f"Log skewness:      {df['log_revenue'].skew():.2f}")
```

**Why feature engineering matters:** Machine learning models and statistical tests work better when features are in meaningful, comparable ranges. Binning, encoding, and log transforms are the most common techniques you'll use in every analytics project.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import numpy as np

# E-commerce order data
df = pd.DataFrame({
    "order_id":   range(1, 9),
    "customer":   ["Alice","Bob","Alice","Carol","Bob","Carol","Dave","Alice"],
    "category":   ["Electronics","Clothing","Electronics","Food","Clothing","Food","Electronics","Food"],
    "revenue":    [1200, 85, 950, 42, 120, 38, 1800, 15],
    "items":      [2, 3, 1, 5, 4, 2, 3, 1],
    "days_since_last": [5, 45, 12, 3, 60, 8, 120, 2]
})

# 1. Revenue per item (efficiency metric)
df["revenue_per_item"] = df["revenue"] / df["items"]

# 2. Customer recency bins
df["recency_tier"] = pd.cut(
    df["days_since_last"],
    bins=[0, 7, 30, 90, 999],
    labels=["Active", "Recent", "Lapsing", "Churned"]
)

# 3. Log-transform skewed revenue
df["log_revenue"] = np.log1p(df["revenue"])

# 4. One-hot encode category
dummies = pd.get_dummies(df["category"], prefix="cat")
df = pd.concat([df, dummies], axis=1)

print(df[["customer","revenue","revenue_per_item","recency_tier","log_revenue"]].to_string())
print(f"\nRevenue skewness before log: {df['revenue'].skew():.2f}")
print(f"Revenue skewness after log:  {df['log_revenue'].skew():.2f}")""",
                "explanation": "revenue_per_item normalizes orders so a $1200 order with 2 items ($600/item) is comparable to a $950 order with 1 item ($950/item). pd.cut() with labels converts raw numbers into meaningful business tiers. log1p() (log of x+1) handles zeros safely. pd.concat with axis=1 appends the dummy columns side-by-side rather than stacking rows."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "pd.cut(df['col'], bins=[...], labels=[...])",
                    "pd.get_dummies(df['col'], prefix='prefix')",
                    "pd.concat([df, dummies], axis=1)",
                    "np.log1p(df['col'])  # log transform (safe for 0s)",
                    "df['col'].pct_change()  # % change"
                ],
                "notes": "pd.get_dummies creates a column for each unique value — be careful with high-cardinality columns (many unique values). For k categories, consider using k-1 dummies to avoid multicollinearity."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does pd.get_dummies(df['color']) do if 'color' has values ['Red','Blue','Green']?",
                    "options": [
                        "A) Converts text to numbers 1, 2, 3",
                        "B) Creates three new 0/1 columns: color_Red, color_Blue, color_Green",
                        "C) Groups rows by color",
                        "D) Removes the color column"
                    ],
                    "answer": 1,
                    "explanation": "get_dummies creates a binary (0 or 1) column for each unique value. A row with color='Red' gets color_Red=1, color_Blue=0, color_Green=0. This is called one-hot encoding."
                },
                {
                    "type": "true_false",
                    "question": "np.log1p(x) is equivalent to np.log(x+1) and is safe when x contains zeros.",
                    "answer": True,
                    "explanation": "log(0) is undefined (-infinity). log1p adds 1 before taking the log, so log1p(0) = log(1) = 0. This makes it safe for count data and revenue figures that might be 0."
                },
                {
                    "type": "fill_blank",
                    "question": "Bin a 'score' column into 'Low'/'Medium'/'High' using pd.cut",
                    "template": "df['tier'] = pd.___(df['score'], bins=[0,40,70,100], labels=['Low','Medium','High'])",
                    "answer": "cut",
                    "explanation": "pd.cut divides continuous values into discrete bins defined by the breakpoints in 'bins'. The labels list must have one fewer element than the number of breakpoints."
                }
            ],
            "challenge": {
                "instructions": "You have a customer database. Engineer 4 new features: (1) 'clv_tier' — bin 'lifetime_value' into Bronze/Silver/Gold/Platinum, (2) 'spend_per_visit' — revenue divided by visits, (3) 'log_lifetime_value' — log transform of lifetime_value, (4) one-hot encode the 'channel' column. Print the final DataFrame with all new features.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'customer_id': range(1, 9),\n    'lifetime_value': [250, 4200, 980, 12000, 380, 750, 8500, 120],\n    'visits':         [5, 40, 12, 95, 8, 15, 70, 3],\n    'revenue':        [180, 3100, 720, 9800, 290, 580, 6400, 85],\n    'channel':        ['Web','App','Web','App','Store','Store','App','Web']\n})\n\n# 1. CLV tier\n\n# 2. Spend per visit\n\n# 3. Log lifetime value\n\n# 4. One-hot encode channel\n\nprint(df.head())\n",
                "tests": [
                    {"type": "code_contains", "value": "pd.cut"},
                    {"type": "code_contains", "value": "get_dummies"},
                    {"type": "code_contains", "value": "log1p"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\ndf=pd.DataFrame({'customer_id':range(1,9),'lifetime_value':[250,4200,980,12000,380,750,8500,120],'visits':[5,40,12,95,8,15,70,3],'revenue':[180,3100,720,9800,290,580,6400,85],'channel':['Web','App','Web','App','Store','Store','App','Web']})\ndf['clv_tier']=pd.cut(df['lifetime_value'],bins=[0,500,2000,7000,50000],labels=['Bronze','Silver','Gold','Platinum'])\ndf['spend_per_visit']=df['revenue']/df['visits']\ndf['log_lifetime_value']=np.log1p(df['lifetime_value'])\ndummies=pd.get_dummies(df['channel'],prefix='ch')\ndf=pd.concat([df,dummies],axis=1)\nprint(df)"
            },
            "challenge_variations": [
                "Variation 1: Create an 'is_weekend' binary feature from a date column.",
                "Variation 2: Bin customer ages into generational segments (Boomer, GenX, Millennial, GenZ).",
                "Variation 3: Encode product categories and build a correlation heatmap of the result.",
                "Variation 4: Create a 'days_to_close' feature from start and end date columns.",
                "Variation 5: Build a 'value_score' composite feature combining revenue and recency.",
                "Variation 6: Apply log transform to all right-skewed columns in a DataFrame automatically.",
                "Variation 7: Create interaction features (e.g., price * quantity) from existing columns.",
                "Variation 8: Use pd.qcut instead of pd.cut for equal-frequency bins.",
                "Variation 9: One-hot encode and then train a simple linear regression on the result.",
                "Variation 10: Build a pipeline that applies binning, encoding, and log transform to any dataset."
            ]
        },
        {
            "id": "m2-l20",
            "title": "Data Normalization — Putting Data on the Same Scale",
            "order": 20,
            "duration_min": 20,
            "real_world_context": "If you compare 'age' (range 18-80) with 'salary' (range 30000-200000) in a model, salary will dominate simply because its numbers are bigger — not because it's more important. Normalization fixes this.",
            "concept": """**Normalization** (also called scaling or standardization) transforms features so they're on comparable scales. It's required before clustering, PCA, and most machine learning models.

**Min-Max Scaling — compress to [0, 1] range:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "age":    [25, 45, 32, 51, 28],
    "salary": [42000, 95000, 61000, 110000, 48000],
    "score":  [72, 88, 65, 91, 78]
})

# Manual min-max scaling
def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

df["age_scaled"]    = min_max_scale(df["age"])
df["salary_scaled"] = min_max_scale(df["salary"])
print(df[["age","age_scaled","salary","salary_scaled"]])
# age  age_scaled  salary  salary_scaled
#  25       0.000   42000          0.000
#  45       0.769   95000          0.779
```

**Z-score Standardization — mean=0, std=1:**
```python
def z_score(series):
    return (series - series.mean()) / series.std()

df["age_z"] = z_score(df["age"])
# Values typically range from about -3 to +3
# 0 = exactly average, +1 = one std above average
```

**Using scikit-learn (the production way):**
```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Min-Max Scaler
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(
    scaler.fit_transform(df[["age","salary","score"]]),
    columns=["age","salary","score"]
)

# Standard Scaler (z-score)
scaler_z = StandardScaler()
df_standardized = pd.DataFrame(
    scaler_z.fit_transform(df[["age","salary","score"]]),
    columns=["age","salary","score"]
)
```

**When to use each:**
- **Min-Max:** When you need values between 0 and 1 (neural networks, image data). Sensitive to outliers.
- **Z-score:** When your data is roughly normal and you want mean-centered data. More robust to outliers.
- **Neither:** Tree-based models (decision trees, random forests) don't need scaling.

**Rule:** Always fit the scaler on training data only, then transform test data using the same scaler — otherwise you're leaking information from the test set.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Store performance metrics (very different scales)
stores = pd.DataFrame({
    "store":         ["A","B","C","D","E"],
    "sq_footage":    [1200, 4500, 800, 3200, 2100],  # hundreds to thousands
    "daily_traffic": [85, 320, 60, 240, 155],         # tens to hundreds
    "avg_ticket":    [45, 92, 38, 78, 61],             # tens to hundreds
    "monthly_rev":   [115000, 890000, 68000, 720000, 285000]  # hundreds of thousands
})

# Columns to scale
cols = ["sq_footage","daily_traffic","avg_ticket","monthly_rev"]

# Min-Max scaling (manual)
scaled = stores.copy()
for col in cols:
    scaled[col] = (stores[col] - stores[col].min()) / (stores[col].max() - stores[col].min())

print("After Min-Max Scaling (all values 0-1):")
print(scaled[cols].round(3))

# Visualize: before vs after scaling
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Before: wide range makes comparison impossible
axes[0].bar(stores["store"], stores["monthly_rev"], color="#3b82f6")
axes[0].set_title("Monthly Revenue (raw) — hard to compare with other metrics")
axes[0].set_ylabel("$")

# After: everything on 0-1 scale
scaled.set_index("store")[cols].plot(kind="bar", ax=axes[1])
axes[1].set_title("All Metrics Scaled (0-1) — now comparable")
axes[1].set_ylim(0, 1.2)

plt.tight_layout()
plt.show()""",
                "explanation": "Before scaling, monthly_rev (in hundreds of thousands) completely dominates any comparison or model. After min-max scaling, all four metrics are on the same 0-1 scale. Store B performs consistently high across metrics; Store C is consistently low. This cross-metric comparison is impossible without normalization."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "(x - x.min()) / (x.max() - x.min())  # min-max manual",
                    "(x - x.mean()) / x.std()  # z-score manual",
                    "from sklearn.preprocessing import MinMaxScaler, StandardScaler",
                    "scaler.fit_transform(df[cols])"
                ],
                "notes": "Min-Max is sensitive to outliers (one extreme value compresses all others). Z-score is more robust. Tree-based models (Random Forest, XGBoost) don't require scaling — but k-means clustering and linear models do."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "After Z-score standardization, what are the mean and standard deviation of a feature?",
                    "options": [
                        "A) Mean=0.5, Std=0.25",
                        "B) Mean=1, Std=0",
                        "C) Mean=0, Std=1",
                        "D) Mean=100, Std=10"
                    ],
                    "answer": 2,
                    "explanation": "Z-score standardization transforms data so mean=0 and std=1. A value of +2 means '2 standard deviations above average'. A value of 0 means exactly average."
                },
                {
                    "type": "true_false",
                    "question": "Min-Max scaling is robust to outliers because it uses the mean and standard deviation.",
                    "answer": False,
                    "explanation": "Min-Max uses min and max values — a single extreme outlier will compress all other values into a tiny range. Z-score (which uses mean/std) is slightly more robust, but both are affected by outliers."
                },
                {
                    "type": "fill_blank",
                    "question": "Apply Z-score standardization manually to a Series s",
                    "template": "s_scaled = (s - s.___()) / s.std()",
                    "answer": "mean",
                    "explanation": "Z-score formula: (value - mean) / std. This centers the data at 0 (by subtracting the mean) and scales it to unit variance (by dividing by std)."
                }
            ],
            "challenge": {
                "instructions": "You have a DataFrame of job applicant scores across 4 tests that have very different scales. Apply both Min-Max and Z-score normalization manually. Then print which applicant has the highest average Z-score (overall best performer across all tests). Visualize the original vs scaled distributions.",
                "starter_code": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\napplicants = pd.DataFrame({\n    'name':        ['Ana','Ben','Cara','Dan','Eli'],\n    'coding_test': [72, 88, 65, 91, 78],       # 0-100\n    'verbal':      [145, 132, 158, 128, 141],   # 100-200\n    'case_study':  [4.2, 3.8, 4.6, 3.5, 4.1],  # 1-5\n    'experience':  [3, 8, 1, 12, 5]            # years\n})\n\ncols = ['coding_test','verbal','case_study','experience']\n\n# Min-Max scale each column\n\n# Z-score scale each column\n\n# Find applicant with highest average Z-score\n\n# Visualize original vs min-max scaled\n",
                "tests": [
                    {"type": "code_contains", "value": "mean()"},
                    {"type": "code_contains", "value": "std()"},
                    {"type": "runs_without_error"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\napp=pd.DataFrame({'name':['Ana','Ben','Cara','Dan','Eli'],'coding_test':[72,88,65,91,78],'verbal':[145,132,158,128,141],'case_study':[4.2,3.8,4.6,3.5,4.1],'experience':[3,8,1,12,5]})\ncols=['coding_test','verbal','case_study','experience']\nfor col in cols:\n    app[col+'_mm']=(app[col]-app[col].min())/(app[col].max()-app[col].min())\n    app[col+'_z']=(app[col]-app[col].mean())/app[col].std()\nz_cols=[c+'_z' for c in cols]\napp['avg_z']=app[z_cols].mean(axis=1)\nprint('Best overall applicant:',app.loc[app['avg_z'].idxmax(),'name'])\nprint(app[['name','avg_z']].sort_values('avg_z',ascending=False))"
            },
            "challenge_variations": [
                "Variation 1: Normalize customer RFM (Recency, Frequency, Monetary) scores for segmentation.",
                "Variation 2: Use sklearn's StandardScaler and verify it produces the same results as manual z-score.",
                "Variation 3: Scale features for a k-means clustering task on customer purchase data.",
                "Variation 4: Compare a regression model's coefficients before and after standardizing features.",
                "Variation 5: Show how a single outlier distorts Min-Max scaling using a contrived example.",
                "Variation 6: Apply RobustScaler from sklearn (uses median/IQR) for data with outliers.",
                "Variation 7: Normalize a time series to compare multiple KPIs on the same chart.",
                "Variation 8: Scale only numeric columns in a mixed DataFrame, leaving text columns unchanged.",
                "Variation 9: Reverse a min-max transformation using the inverse_transform method.",
                "Variation 10: Build a reusable normalize_df() function that scales all numeric columns."
            ]
        },
        {
            "id": "m2-l21",
            "title": "Working with Real Datasets — From Messy to Insight",
            "order": 21,
            "duration_min": 25,
            "real_world_context": "Every analytics job starts with an unfamiliar dataset and the question 'figure out what's going on.' This lesson teaches the systematic first-look workflow that professional analysts use every time they open a new file.",
            "concept": """When you encounter an unfamiliar dataset, follow this systematic exploration workflow before doing any analysis.

**Step 1 — Get the big picture:**
```python
import pandas as pd

df = pd.read_csv("mystery_data.csv")

print(f"Shape: {df.shape}")          # (rows, columns)
print(f"Columns: {df.columns.tolist()}")
print(df.dtypes)
print(df.head(3))
```

**Step 2 — Check data quality:**
```python
# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print(pd.DataFrame({"count": missing, "pct": missing_pct}).sort_values("pct", ascending=False))

# Duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")

# Unique values per column
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")
```

**Step 3 — Understand distributions:**
```python
# Numeric columns
print(df.describe())

# Categorical columns
for col in df.select_dtypes(include="object").columns:
    print(f"\\n{col}:")
    print(df[col].value_counts().head(5))
```

**Step 4 — Look for obvious problems:**
```python
# Impossible values
print(df[df["age"] < 0])          # Negative ages
print(df[df["price"] == 0])       # Zero prices (intentional?)
print(df[df["quantity"] > 1000])  # Suspiciously large quantities

# Date range check
df["date"] = pd.to_datetime(df["date"])
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
```

**Step 5 — First hypothesis:**
```python
# Once clean, answer: what's the most interesting pattern?
# Typical first questions:
# - Who are the top customers by revenue?
# - Which time period had the most activity?
# - Are there any categories dramatically outperforming others?

top_customers = df.groupby("customer")["revenue"].sum().sort_values(ascending=False).head(5)
print("Top 5 customers:")
print(top_customers)
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd
import numpy as np
import io

# Simulate a messy dataset (as if loaded from CSV)
raw_csv = \"\"\"order_id,customer,product,category,quantity,unit_price,date,region
1001,Alice,Laptop,Electronics,2,999.99,2024-01-15,North
1002,Bob,Shirt,Clothing,,29.99,2024-01-16,South
1003,Alice,Laptop,Electronics,2,999.99,2024-01-15,North
1004,Carol,Phone,Electronics,1,699.0,bad_date,East
1005,Dave,Jeans,Clothing,3,59.99,2024-02-01,
1006,Eve,Charger,Electronics,-1,24.99,2024-02-03,North
1007,Frank,Tablet,Electronics,1,449.0,2024-02-10,West
\"\"\"

df = pd.read_csv(io.StringIO(raw_csv))

print("=== STEP 1: Big Picture ===")
print(f"Shape: {df.shape}")
print(df.dtypes)

print("\\n=== STEP 2: Data Quality ===")
print("Missing values:")
print(df.isnull().sum())
print(f"Duplicates: {df.duplicated().sum()}")

print("\\n=== STEP 3: Problems Found ===")
print("Negative quantities (data error):")
print(df[df["quantity"] < 0])

# Fix issues
df_clean = df.copy()
df_clean = df_clean.drop_duplicates()
df_clean["quantity"] = df_clean["quantity"].fillna(1)
df_clean["region"] = df_clean["region"].fillna("Unknown")
df_clean = df_clean[df_clean["quantity"] > 0]  # remove negative
df_clean["date"] = pd.to_datetime(df_clean["date"], errors="coerce")

print("\\n=== STEP 4: First Insight ===")
df_clean["revenue"] = df_clean["quantity"] * df_clean["unit_price"]
print("Revenue by category:")
print(df_clean.groupby("category")["revenue"].sum().sort_values(ascending=False))""",
                "explanation": "errors='coerce' in pd.to_datetime converts unparseable dates to NaT (Not a Time) rather than crashing. We document every cleaning decision: filling NaN quantity with 1 (reasonable assumption for an order), removing negative quantities (clearly an error), deduplicating the Alice order. Each cleaning step should be defensible."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "df.isnull().sum() / df.duplicated().sum()",
                    "df.select_dtypes(include='object')  # text columns only",
                    "df['col'].nunique()  # count unique values",
                    "pd.to_datetime(df['col'], errors='coerce')",
                    "df.describe()  # full numeric summary"
                ],
                "notes": "The first-look workflow: shape → dtypes → missing values → duplicates → distributions → impossible values → first insight. Never skip to analysis before completing all quality checks."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does df.select_dtypes(include='object') return?",
                    "options": [
                        "A) All numeric columns",
                        "B) Only the index column",
                        "C) All text/string columns",
                        "D) Columns with missing values"
                    ],
                    "answer": 2,
                    "explanation": "In pandas, string columns have dtype 'object'. select_dtypes(include='object') returns a DataFrame with only the text columns — useful for applying string cleaning operations."
                },
                {
                    "type": "true_false",
                    "question": "pd.to_datetime(col, errors='coerce') will raise an error if a date string cannot be parsed.",
                    "answer": False,
                    "explanation": "errors='coerce' silently converts unparseable values to NaT (Not a Time) instead of raising an error. This is the safest option when loading real-world messy date data."
                },
                {
                    "type": "fill_blank",
                    "question": "Count the number of unique values in a 'product' column",
                    "template": "n_unique = df['product'].___( )",
                    "answer": "nunique()",
                    "explanation": ".nunique() (n unique) returns the count of distinct values, excluding NaN. It's faster than len(df['product'].unique())."
                }
            ],
            "challenge": {
                "instructions": "You receive a raw sales CSV (created in the starter code). Apply the full 5-step first-look workflow: (1) print shape and dtypes, (2) check missing values and duplicates, (3) identify impossible values (negative revenue or zero quantity), (4) clean the data, (5) print top 3 products by total revenue as your first insight.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\n# Simulate loading a messy CSV\nnp.random.seed(42)\nn = 50\ndata = {\n    'product':  np.random.choice(['Laptop','Phone','Tablet','Watch','Charger'], n),\n    'region':   np.random.choice(['North','South','East','West', None], n),\n    'quantity': np.random.choice([1,2,3,-1,0, None], n),\n    'unit_price': np.random.choice([999,699,499,299,29, 0], n)\n}\ndf = pd.DataFrame(data)\n# Add some duplicates\ndf = pd.concat([df, df.iloc[:5]], ignore_index=True)\n\n# STEP 1: Big picture\n\n# STEP 2: Data quality\n\n# STEP 3: Find impossible values\n\n# STEP 4: Clean\n\n# STEP 5: First insight — top 3 products by revenue\n",
                "tests": [
                    {"type": "code_contains", "value": "isnull"},
                    {"type": "code_contains", "value": "drop_duplicates"},
                    {"type": "code_contains", "value": "groupby"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\nn=50\ndata={'product':np.random.choice(['Laptop','Phone','Tablet','Watch','Charger'],n),'region':np.random.choice(['North','South','East','West',None],n),'quantity':np.random.choice([1,2,3,-1,0,None],n),'unit_price':np.random.choice([999,699,499,299,29,0],n)}\ndf=pd.DataFrame(data)\ndf=pd.concat([df,df.iloc[:5]],ignore_index=True)\nprint('Shape:',df.shape)\nprint(df.dtypes)\nprint('\\nMissing:')\nprint(df.isnull().sum())\nprint('Duplicates:',df.duplicated().sum())\nprint('\\nProblems:')\nprint(df[(df['quantity']<=0)|(df['unit_price']==0)])\ndf=df.drop_duplicates()\ndf=df.dropna(subset=['quantity','unit_price'])\ndf=df[(df['quantity']>0)&(df['unit_price']>0)]\ndf['region']=df['region'].fillna('Unknown')\ndf['revenue']=df['quantity']*df['unit_price']\nprint('\\nTop 3 products:')\nprint(df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(3))"
            },
            "challenge_variations": [
                "Variation 1: Load and explore the classic Titanic dataset, following all 5 steps.",
                "Variation 2: Explore a customer churn dataset: identify which features have the most missing data.",
                "Variation 3: Find and document all data quality issues in a given HR dataset.",
                "Variation 4: Write a reusable data_quality_report(df) function that prints all quality checks.",
                "Variation 5: Profile a dataset and automatically flag columns that are >20% missing.",
                "Variation 6: Detect mixed data types in a single column (e.g., column with both numbers and strings).",
                "Variation 7: Apply the 5-step workflow to a retail inventory dataset with 10+ columns.",
                "Variation 8: Identify which customer IDs appear in one table but not another.",
                "Variation 9: Explore a time series dataset: check for date gaps and missing periods.",
                "Variation 10: Build an automated EDA (exploratory data analysis) report using pandas-profiling style logic."
            ]
        },
        {
            "id": "m2-l22",
            "title": "Excel Integration — Reading and Writing Excel",
            "order": 22,
            "duration_min": 20,
            "real_world_context": "In the real business world, Excel is everywhere. Every client, manager, and stakeholder expects reports in Excel format. Knowing how to read from and write to Excel files in Python is a practical necessity.",
            "concept": """Pandas reads and writes Excel files directly. This bridges the gap between Python analytics and the Excel-based business world.

**Reading Excel files:**
```python
import pandas as pd

# Read a single sheet
df = pd.read_excel("sales_report.xlsx")

# Read a specific sheet by name
df = pd.read_excel("sales_report.xlsx", sheet_name="Q4_Data")

# Read a specific sheet by index (0=first, 1=second...)
df = pd.read_excel("sales_report.xlsx", sheet_name=0)

# Read all sheets at once — returns a dict
all_sheets = pd.read_excel("sales_report.xlsx", sheet_name=None)
for sheet_name, df_sheet in all_sheets.items():
    print(f"{sheet_name}: {df_sheet.shape}")
```

**Useful read_excel options:**
```python
pd.read_excel("data.xlsx",
    header=1,               # Row 1 is the header (not row 0)
    skiprows=3,             # Skip first 3 rows
    usecols="A:D",          # Only columns A through D
    nrows=100               # Only first 100 rows
)
```

**Writing to Excel:**
```python
# Simple write — one sheet
df.to_excel("output.xlsx", index=False)

# Write multiple sheets using ExcelWriter
with pd.ExcelWriter("analytics_report.xlsx", engine="openpyxl") as writer:
    df_summary.to_excel(writer, sheet_name="Summary", index=False)
    df_detail.to_excel(writer, sheet_name="Detail", index=False)
    df_chart_data.to_excel(writer, sheet_name="Chart_Data", index=False)
```

**Required libraries:**
```python
# Install if needed:
# pip install openpyxl  (for .xlsx files)
# pip install xlrd      (for older .xls files)

# Check what's available
import openpyxl
```

**Common patterns:**
```python
# Read monthly Excel files and combine
import glob

all_files = glob.glob("data/monthly_*.xlsx")
dfs = [pd.read_excel(f) for f in all_files]
combined = pd.concat(dfs, ignore_index=True)
combined.to_excel("combined_annual.xlsx", index=False)
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import pandas as pd

# --- CREATING EXCEL REPORT FROM ANALYSIS ---

# Simulate analysis results
summary_data = {
    "Region":    ["North","South","East","West"],
    "Total_Revenue": [245000, 198000, 312000, 167000],
    "Avg_Order": [485, 421, 610, 398],
    "Num_Orders": [505, 470, 511, 420]
}
df_summary = pd.DataFrame(summary_data)

detail_data = {
    "Product":  ["Laptop","Phone","Tablet","Watch","Laptop","Phone"],
    "Region":   ["North","North","South","East","East","West"],
    "Revenue":  [45000, 32000, 18000, 9500, 51000, 28000],
    "Units":    [45, 92, 60, 38, 51, 80]
}
df_detail = pd.DataFrame(detail_data)

# Write to Excel with multiple sheets
output_path = "analytics_report.xlsx"
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df_summary.to_excel(writer, sheet_name="Executive Summary", index=False)
    df_detail.to_excel(writer, sheet_name="Product Detail", index=False)

print(f"Report written to {output_path}")

# --- READING BACK AND VERIFYING ---
verify = pd.read_excel(output_path, sheet_name="Executive Summary")
print("\\nSummary sheet loaded back:")
print(verify)
print(f"\\nTop region by revenue: {verify.loc[verify['Total_Revenue'].idxmax(), 'Region']}")""",
                "explanation": "ExcelWriter is used as a context manager (with block) so the file is properly saved and closed when the block exits. We pass engine='openpyxl' explicitly — this is the modern engine for .xlsx files. Each call to .to_excel() inside the block writes to a different sheet. Reading back the file with a specific sheet_name confirms the write succeeded."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "pd.read_excel('file.xlsx', sheet_name='Sheet1')",
                    "pd.read_excel('file.xlsx', sheet_name=None)  # all sheets as dict",
                    "df.to_excel('file.xlsx', index=False)",
                    "pd.ExcelWriter('file.xlsx', engine='openpyxl') as writer",
                    "df.to_excel(writer, sheet_name='Name', index=False)"
                ],
                "notes": "Always use engine='openpyxl' for modern .xlsx files. Use index=False unless you specifically want row numbers in the Excel file. The 'with' block ensures the file is written and closed properly."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "How do you read ALL sheets from an Excel file into a dictionary of DataFrames?",
                    "options": [
                        "A) pd.read_excel('file.xlsx', sheet_name='all')",
                        "B) pd.read_excel('file.xlsx', sheet_name=None)",
                        "C) pd.read_all_excel('file.xlsx')",
                        "D) pd.read_excel('file.xlsx', all_sheets=True)"
                    ],
                    "answer": 1,
                    "explanation": "sheet_name=None tells pandas to read every sheet and return a dict where keys are sheet names and values are DataFrames."
                },
                {
                    "type": "true_false",
                    "question": "pd.ExcelWriter should be used as a context manager (with block) when writing multiple sheets.",
                    "answer": True,
                    "explanation": "Using 'with pd.ExcelWriter(...) as writer:' ensures the file is properly finalized and closed after all sheets are written. Without it you must manually call writer.save() (deprecated) or writer.close()."
                },
                {
                    "type": "fill_blank",
                    "question": "Write a DataFrame to a sheet named 'Sales' inside an ExcelWriter context",
                    "template": "df.to_excel(writer, ___='Sales', index=False)",
                    "answer": "sheet_name",
                    "explanation": "sheet_name parameter specifies which sheet in the Excel workbook this DataFrame will be written to. Without it, pandas uses 'Sheet1'."
                }
            ],
            "challenge": {
                "instructions": "Create a 3-sheet Excel analytics report: (1) 'Summary' sheet with regional totals, (2) 'Monthly' sheet with monthly breakdown, (3) 'Top Products' sheet with top 5 products by revenue. Save as 'business_report.xlsx', then read back the Summary sheet and print it to verify.",
                "starter_code": "import pandas as pd\n\n# Regional summary\ndf_summary = pd.DataFrame({\n    'Region': ['North','South','East','West'],\n    'Revenue': [245000,198000,312000,167000],\n    'Units': [490,420,560,380]\n})\n\n# Monthly data\ndf_monthly = pd.DataFrame({\n    'Month': ['Jan','Feb','Mar','Apr','May','Jun'],\n    'Revenue': [82000,75000,93000,88000,101000,96000]\n})\n\n# Products\ndf_products = pd.DataFrame({\n    'Product': ['Laptop','Phone','Tablet','Watch','Charger','Headphones'],\n    'Revenue': [185000,142000,98000,54000,32000,28000]\n})\n\n# Write to Excel with 3 sheets\n\n# Read back the Summary sheet and print it\n",
                "tests": [
                    {"type": "code_contains", "value": "ExcelWriter"},
                    {"type": "code_contains", "value": "to_excel"},
                    {"type": "code_contains", "value": "read_excel"}
                ],
                "solution": "import pandas as pd\ndf_summary=pd.DataFrame({'Region':['North','South','East','West'],'Revenue':[245000,198000,312000,167000],'Units':[490,420,560,380]})\ndf_monthly=pd.DataFrame({'Month':['Jan','Feb','Mar','Apr','May','Jun'],'Revenue':[82000,75000,93000,88000,101000,96000]})\ndf_products=pd.DataFrame({'Product':['Laptop','Phone','Tablet','Watch','Charger','Headphones'],'Revenue':[185000,142000,98000,54000,32000,28000]})\ndf_top5=df_products.sort_values('Revenue',ascending=False).head(5)\nwith pd.ExcelWriter('business_report.xlsx',engine='openpyxl') as writer:\n    df_summary.to_excel(writer,sheet_name='Summary',index=False)\n    df_monthly.to_excel(writer,sheet_name='Monthly',index=False)\n    df_top5.to_excel(writer,sheet_name='Top Products',index=False)\nverify=pd.read_excel('business_report.xlsx',sheet_name='Summary')\nprint(verify)"
            },
            "challenge_variations": [
                "Variation 1: Read an Excel file with multiple header rows (skiprows) and clean the column names.",
                "Variation 2: Read only specific columns from a large Excel file using usecols='A:F'.",
                "Variation 3: Combine 4 monthly Excel reports into one annual DataFrame using glob and concat.",
                "Variation 4: Write a pivot table result to Excel with frozen header row using openpyxl.",
                "Variation 5: Read all sheets from an Excel workbook and print the shape of each.",
                "Variation 6: Write the same analysis to both CSV and Excel formats for different stakeholders.",
                "Variation 7: Read an Excel file where dates are stored as strings and convert them properly.",
                "Variation 8: Add column width formatting to an Excel output using openpyxl's column_dimensions.",
                "Variation 9: Read an Excel template, fill in calculated values, and save as a new file.",
                "Variation 10: Automate a weekly Excel report that pulls from a CSV and outputs a formatted Excel file."
            ]
        },
        {
            "id": "m2-l23",
            "title": "Exploratory Data Analysis (EDA)",
            "order": 23,
            "duration_min": 25,
            "concept": """**Exploratory Data Analysis (EDA)** is the process of *getting to know your data* before modeling or reporting. It uncovers shape, outliers, distributions, and relationships.

**EDA workflow:**
1. **Understand the schema** — how many rows, columns, data types?
2. **Check missing data** — where are the gaps?
3. **Describe distributions** — central tendency, spread, skew
4. **Find correlations** — which features move together?
5. **Spot outliers** — values that seem impossible or anomalous

```python
import pandas as pd
import numpy as np

df = pd.read_csv('sales.csv')

# 1. Shape and types
print(df.shape)          # (1200, 8)
print(df.dtypes)         # column types
print(df.head())

# 2. Missing values
print(df.isnull().sum())             # count per column
print(df.isnull().mean() * 100)      # % missing

# 3. Distributions
print(df.describe())                 # count, mean, std, min, 25%, 50%, 75%, max
print(df['revenue'].skew())          # positive = right-skewed
print(df['revenue'].kurtosis())      # >3 = heavy tails

# 4. Correlations
print(df.corr(numeric_only=True))    # pairwise correlation matrix

# 5. Outliers (IQR method)
Q1 = df['revenue'].quantile(0.25)
Q3 = df['revenue'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['revenue'] < Q1 - 1.5*IQR) | (df['revenue'] > Q3 + 1.5*IQR)]
print(f"{len(outliers)} outlier rows")
```

**Key principle:** EDA is about *asking questions*, not answering them. Every plot and summary should raise the next question.

**Business tip:** In BA&AI roles, you'll spend ~60% of project time in EDA. Thorough exploration prevents costly mistakes downstream.""",
            "worked_example": """**Scenario:** You just received a customer dataset for a subscription SaaS product. Let's do a proper EDA.

```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('customers.csv')
print("Shape:", df.shape)
# Shape: (5000, 10)

# Column overview
print(df.dtypes)
# customer_id       int64
# signup_date       object   ← string, needs parsing
# plan              object
# monthly_spend    float64
# sessions_month    int64
# churn             int64    ← 0 or 1
# country           object
# age               float64  ← has NaN (not int!)
# support_tickets   int64
# referral          object

# Fix date type
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Missing values
print(df.isnull().mean() * 100)
# age        8.4%  ← 8.4% missing
# country    1.2%

# Distribution of target variable
print(df['churn'].value_counts(normalize=True))
# 0    0.82  (82% retained)
# 1    0.18  (18% churned)  ← class imbalance!

# Numeric summary
print(df[['monthly_spend','sessions_month','age','support_tickets']].describe())

# Who churns more — by plan?
print(df.groupby('plan')['churn'].mean())
# basic       0.31
# standard    0.15
# premium     0.07   ← premium customers churn least

# Correlation with churn
print(df.corr(numeric_only=True)['churn'].sort_values())
# monthly_spend     -0.32  (higher spend = less churn)
# sessions_month    -0.28  (more engaged = less churn)
# support_tickets    0.41  (more tickets = more churn!)
```

**Findings summary:**
- 18% churn rate — worth investigating
- Support tickets are the strongest churn predictor
- Premium plan customers are 4× more loyal than basic
- 8% of ages are missing — need to decide: impute or drop?

This EDA would take 15 minutes in practice and saves weeks of wasted modeling effort.""",
            "difficulty_tiers": {
                "beginner": "Run df.describe() and df.isnull().sum() on any CSV file. Print the 5 columns most correlated with a target variable.",
                "intermediate": "Write a reusable eda_report(df, target) function that prints shape, missing %, distribution of target, and top 5 correlations.",
                "advanced": "Build a full EDA pipeline that auto-detects categorical vs. numeric columns, generates frequency tables for categoricals, and flags columns with >20% missing."
            },
            "quiz": [
                {
                    "type": "multiple_choice",
                    "question": "df.describe() shows 'count: 950' for a column in a 1000-row DataFrame. What does this mean?",
                    "options": [
                        "A) The column has 950 unique values",
                        "B) 50 values are missing (NaN) in that column",
                        "C) The column contains 950 zeros",
                        "D) The DataFrame has 950 actual rows"
                    ],
                    "answer": 1,
                    "explanation": "describe() only counts non-null values. If count is 950 and the DataFrame has 1000 rows, then 50 rows have NaN in that column."
                },
                {
                    "type": "multiple_choice",
                    "question": "Which method identifies outliers using the interquartile range (IQR) approach?",
                    "options": [
                        "A) Values beyond mean ± 2 standard deviations",
                        "B) Values below Q1 - 1.5×IQR or above Q3 + 1.5×IQR",
                        "C) Values in the top or bottom 5% of the distribution",
                        "D) Values that differ from the median by more than 10%"
                    ],
                    "answer": 1,
                    "explanation": "The IQR method flags points more than 1.5 × IQR below Q1 or above Q3 as outliers. This is Tukey's fence and is the default for box plots."
                },
                {
                    "type": "true_false",
                    "question": "A correlation of 0.95 between two features always means one causes the other.",
                    "answer": False,
                    "explanation": "Correlation measures linear association, not causation. Two variables can be highly correlated due to a third confounding variable or pure coincidence (spurious correlation)."
                }
            ],
            "challenge": {
                "instructions": "Given the employee dataset below, perform a complete EDA: (1) print shape and dtypes, (2) find columns with missing values and their %, (3) print summary stats for numeric columns, (4) find which department has the highest average salary, (5) find the top 3 features most correlated with 'left_company'.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\n# Create sample employee data\nnp.random.seed(42)\nn = 500\ndf = pd.DataFrame({\n    'age': np.random.normal(38, 8, n),\n    'department': np.random.choice(['Sales','Engineering','HR','Finance','Marketing'], n),\n    'salary': np.random.normal(75000, 20000, n),\n    'tenure_years': np.random.exponential(4, n),\n    'satisfaction': np.random.uniform(1, 5, n),\n    'projects': np.random.randint(1, 10, n),\n    'left_company': np.random.choice([0, 1], n, p=[0.78, 0.22])\n})\n# Add some missing values\ndf.loc[np.random.choice(n, 40, replace=False), 'satisfaction'] = np.nan\ndf.loc[np.random.choice(n, 15, replace=False), 'age'] = np.nan\n\n# 1. Print shape and dtypes\n\n# 2. Missing values %\n\n# 3. Summary stats for numeric columns\n\n# 4. Avg salary by department\n\n# 5. Top 3 correlations with left_company\n",
                "tests": [
                    {"type": "code_contains", "value": "isnull"},
                    {"type": "code_contains", "value": "describe"},
                    {"type": "code_contains", "value": "corr"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\nn=500\ndf=pd.DataFrame({'age':np.random.normal(38,8,n),'department':np.random.choice(['Sales','Engineering','HR','Finance','Marketing'],n),'salary':np.random.normal(75000,20000,n),'tenure_years':np.random.exponential(4,n),'satisfaction':np.random.uniform(1,5,n),'projects':np.random.randint(1,10,n),'left_company':np.random.choice([0,1],n,p=[0.78,0.22])})\ndf.loc[np.random.choice(n,40,replace=False),'satisfaction']=np.nan\ndf.loc[np.random.choice(n,15,replace=False),'age']=np.nan\nprint(df.shape)\nprint(df.dtypes)\nprint(df.isnull().mean()*100)\nprint(df.describe())\nprint(df.groupby('department')['salary'].mean().sort_values(ascending=False))\nprint(df.corr(numeric_only=True)['left_company'].abs().sort_values(ascending=False).head(4))"
            },
            "challenge_variations": [
                "Variation 1: Write an eda_report(df) function that automatically prints all EDA outputs in a structured way.",
                "Variation 2: Compare the distributions of a numeric column between churned and retained customers.",
                "Variation 3: Find all pairs of columns with correlation > 0.8 (potential multicollinearity).",
                "Variation 4: Count and visualize (text bar chart) the value counts for every categorical column.",
                "Variation 5: Identify rows that are outliers in multiple columns simultaneously.",
                "Variation 6: Compute the % of rows that have at least one missing value anywhere.",
                "Variation 7: Find columns where the median and mean differ by more than 20% (sign of skew).",
                "Variation 8: Group by a categorical column and compute describe() for each group.",
                "Variation 9: Build an 'EDA scorecard' dict: {'rows', 'cols', 'missing_pct', 'numeric_cols', 'categorical_cols', 'duplicate_rows'}.",
                "Variation 10: Detect constant or near-constant columns (variance < 0.01) that provide no predictive value."
            ]
        },
        {
            "id": "m2-l24",
            "title": "Data Visualization — Telling Stories with Charts",
            "order": 24,
            "duration_min": 25,
            "concept": """**Data visualization** is how analysts communicate findings. The right chart makes a pattern instantly obvious; the wrong chart hides it.

**Core chart types and when to use them:**

| Chart | Use case | Library |
|-------|----------|---------|
| Line | Trends over time | matplotlib / seaborn |
| Bar | Compare categories | matplotlib / seaborn |
| Histogram | Distribution of one variable | matplotlib / seaborn |
| Scatter | Relationship between two numerics | matplotlib / seaborn |
| Box plot | Distribution + outliers by group | seaborn |
| Heatmap | Correlation matrix, confusion matrix | seaborn |
| Pie | Part-of-whole (use sparingly!) | matplotlib |

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('sales.csv')

# --- Line chart: revenue trend ---
monthly = df.groupby('month')['revenue'].sum()
plt.figure(figsize=(10, 4))
plt.plot(monthly.index, monthly.values, marker='o', color='steelblue')
plt.title('Monthly Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('revenue_trend.png')
plt.show()

# --- Bar chart: revenue by region ---
region_rev = df.groupby('region')['revenue'].sum().sort_values()
region_rev.plot(kind='barh', figsize=(8, 4), color='teal')
plt.title('Revenue by Region')
plt.tight_layout()
plt.show()

# --- Seaborn histogram + kde ---
sns.histplot(df['revenue'], bins=30, kde=True, color='steelblue')
plt.title('Revenue Distribution')
plt.show()

# --- Scatter: spend vs. sessions ---
sns.scatterplot(data=df, x='monthly_spend', y='sessions', hue='plan', alpha=0.6)
plt.title('Spend vs. Sessions by Plan')
plt.show()

# --- Correlation heatmap ---
corr = df.select_dtypes('number').corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()
```

**Design principles:**
- **One chart = one insight.** Don't cram everything in.
- **Label everything.** Axes, title, units.
- **Color purposefully.** Use diverging colors for correlation, sequential for quantities.
- **Save to file** with `plt.savefig('chart.png', dpi=150)` for reports.""",
            "worked_example": """**Scenario:** You need to build a one-page visual summary of a retail dataset for a stakeholder meeting.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.random.seed(42)
n = 600
df = pd.DataFrame({
    'month': pd.date_range('2024-01', periods=n//50, freq='ME').repeat(50)[:n],
    'region': np.random.choice(['North','South','East','West'], n),
    'category': np.random.choice(['Electronics','Clothing','Food','Home'], n),
    'revenue': np.random.exponential(500, n) + 100,
    'units': np.random.randint(1, 50, n),
    'discount': np.random.uniform(0, 0.4, n)
})

# Build a 2×2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Retail Analytics Dashboard — Q1 2024', fontsize=16, fontweight='bold')

# Panel 1: Monthly revenue trend
monthly = df.groupby('month')['revenue'].sum()
axes[0, 0].plot(monthly.index, monthly.values, marker='o', color='steelblue', linewidth=2)
axes[0, 0].set_title('Monthly Revenue')
axes[0, 0].set_ylabel('Revenue ($)')
axes[0, 0].tick_params(axis='x', rotation=45)

# Panel 2: Revenue by region (horizontal bar)
region_rev = df.groupby('region')['revenue'].sum().sort_values()
axes[0, 1].barh(region_rev.index, region_rev.values, color='teal')
axes[0, 1].set_title('Revenue by Region')
axes[0, 1].set_xlabel('Total Revenue ($)')

# Panel 3: Revenue distribution by category (box plot)
sns.boxplot(data=df, x='category', y='revenue', ax=axes[1, 0], palette='Set2')
axes[1, 0].set_title('Revenue Distribution by Category')
axes[1, 0].set_ylabel('Revenue ($)')

# Panel 4: Discount vs Revenue scatter
axes[1, 1].scatter(df['discount'], df['revenue'], alpha=0.3, color='coral', s=20)
# Add trend line
z = np.polyfit(df['discount'], df['revenue'], 1)
p = np.poly1d(z)
x_line = np.linspace(0, 0.4, 100)
axes[1, 1].plot(x_line, p(x_line), 'r--', linewidth=2, label='Trend')
axes[1, 1].set_title('Discount vs Revenue')
axes[1, 1].set_xlabel('Discount Rate')
axes[1, 1].set_ylabel('Revenue ($)')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('retail_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("Dashboard saved!")
```

This creates a professional 4-panel dashboard that can go directly into a PowerPoint or report.""",
            "difficulty_tiers": {
                "beginner": "Create a line chart of any time-series data and a bar chart comparing at least 3 categories. Add titles and axis labels to both.",
                "intermediate": "Build a 2×2 subplot dashboard using real CSV data. Include one chart from each category: trend, comparison, distribution, relationship.",
                "advanced": "Create an annotated visualization that highlights the single most important insight (e.g., annotate the peak revenue month with an arrow and text)."
            },
            "quiz": [
                {
                    "type": "multiple_choice",
                    "question": "You want to show how revenue is distributed across 1000 transactions. Which chart is most appropriate?",
                    "options": [
                        "A) Line chart",
                        "B) Pie chart",
                        "C) Histogram",
                        "D) Scatter plot"
                    ],
                    "answer": 2,
                    "explanation": "Histograms show the distribution (shape, spread, skew) of a single numeric variable. A pie chart would have 1000 slices which is unreadable. A scatter needs two variables."
                },
                {
                    "type": "multiple_choice",
                    "question": "Which seaborn function is best for visualizing a correlation matrix?",
                    "options": [
                        "A) sns.barplot()",
                        "B) sns.heatmap()",
                        "C) sns.lineplot()",
                        "D) sns.violinplot()"
                    ],
                    "answer": 1,
                    "explanation": "sns.heatmap() color-codes a 2D matrix — perfect for correlation matrices. Each cell shows the correlation value, and color indicates direction and strength."
                },
                {
                    "type": "fill_blank",
                    "question": "Save a matplotlib figure as a high-resolution PNG (150 DPI)",
                    "template": "plt.savefig('chart.png', ___=150)",
                    "answer": "dpi",
                    "explanation": "dpi (dots per inch) controls resolution. 150 dpi is good for reports; 300 dpi for print. Default is 100."
                }
            ],
            "challenge": {
                "instructions": "Build a 3-panel visualization report for the employee dataset: (1) histogram of salaries with a vertical line at the mean, (2) bar chart of average salary by department, (3) scatter plot of tenure vs satisfaction colored by whether the employee left. Save to 'employee_report.png'.",
                "starter_code": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nn = 500\ndf = pd.DataFrame({\n    'department': np.random.choice(['Sales','Engineering','HR','Finance','Marketing'], n),\n    'salary': np.random.normal(75000, 20000, n),\n    'tenure_years': np.random.exponential(4, n),\n    'satisfaction': np.random.uniform(1, 5, n),\n    'left_company': np.random.choice([0, 1], n, p=[0.78, 0.22])\n})\n\n# Create 3-panel figure\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\nfig.suptitle('Employee Analytics Report')\n\n# Panel 1: Salary histogram with mean line\n\n# Panel 2: Avg salary by department (bar)\n\n# Panel 3: Tenure vs satisfaction, colored by left_company\n\nplt.tight_layout()\nplt.savefig('employee_report.png', dpi=150)\nplt.show()\n",
                "tests": [
                    {"type": "code_contains", "value": "savefig"},
                    {"type": "code_contains", "value": "subplots"},
                    {"type": "code_contains", "value": "axes"}
                ],
                "solution": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nn=500\ndf=pd.DataFrame({'department':np.random.choice(['Sales','Engineering','HR','Finance','Marketing'],n),'salary':np.random.normal(75000,20000,n),'tenure_years':np.random.exponential(4,n),'satisfaction':np.random.uniform(1,5,n),'left_company':np.random.choice([0,1],n,p=[0.78,0.22])})\nfig,axes=plt.subplots(1,3,figsize=(15,5))\nfig.suptitle('Employee Analytics Report')\naxes[0].hist(df['salary'],bins=30,color='steelblue',edgecolor='white')\naxes[0].axvline(df['salary'].mean(),color='red',linestyle='--',label=f'Mean: ${df[\"salary\"].mean():,.0f}')\naxes[0].set_title('Salary Distribution')\naxes[0].legend()\navg_sal=df.groupby('department')['salary'].mean().sort_values()\naxes[1].barh(avg_sal.index,avg_sal.values,color='teal')\naxes[1].set_title('Avg Salary by Department')\ncolors=df['left_company'].map({0:'steelblue',1:'red'})\naxes[2].scatter(df['tenure_years'],df['satisfaction'],c=colors,alpha=0.4,s=20)\naxes[2].set_title('Tenure vs Satisfaction')\naxes[2].set_xlabel('Tenure (years)')\naxes[2].set_ylabel('Satisfaction')\nplt.tight_layout()\nplt.savefig('employee_report.png',dpi=150)\nplt.show()"
            },
            "challenge_variations": [
                "Variation 1: Add data labels on top of each bar in a bar chart showing exact values.",
                "Variation 2: Create a side-by-side bar chart comparing two groups (e.g., churned vs retained) across categories.",
                "Variation 3: Build a time-series area chart showing cumulative revenue month over month.",
                "Variation 4: Create a violin plot showing salary distribution by department.",
                "Variation 5: Add a second y-axis to show both revenue and number of transactions on one chart.",
                "Variation 6: Use seaborn's pairplot() on a DataFrame with 4 numeric columns to see all pairwise relationships.",
                "Variation 7: Create a stacked bar chart showing revenue by category and region.",
                "Variation 8: Annotate the highest and lowest points on a line chart with text labels.",
                "Variation 9: Create a ranked horizontal bar chart with colors based on value (green=high, red=low).",
                "Variation 10: Build a 4-chart performance dashboard and export it as a PDF page using matplotlib's PdfPages."
            ]
        },
        {
            "id": "m2-l25",
            "title": "Building a Complete Data Analytics Pipeline",
            "order": 25,
            "duration_min": 30,
            "concept": """A **data analytics pipeline** is a repeatable, end-to-end workflow that takes raw data and produces insights or outputs automatically. Building pipelines (instead of one-off scripts) is the mark of a professional analyst.

**Pipeline stages:**
1. **Ingest** — load data from files, databases, or APIs
2. **Validate** — check schemas, types, missing values
3. **Clean** — fix/impute/drop problems
4. **Transform** — engineer new features, aggregate, reshape
5. **Analyze** — compute metrics, run statistical tests
6. **Output** — save results, generate reports, export to Excel

```python
import pandas as pd
import numpy as np
from pathlib import Path

def load_data(filepath: str) -> pd.DataFrame:
    '''Ingest: load CSV with basic schema validation.'''
    df = pd.read_csv(filepath, parse_dates=['date'])
    required = {'date', 'customer_id', 'revenue', 'product'}
    missing_cols = required - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    print(f"Loaded {len(df):,} rows from {filepath}")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    '''Clean: remove duplicates, fix types, handle nulls.'''
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=['customer_id', 'revenue'])  # must-have columns
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['revenue'] = df['revenue'].clip(lower=0)         # no negative revenue
    df['product'] = df['product'].str.strip().str.title()
    print(f"Cleaned: {before} → {len(df)} rows ({before - len(df)} removed)")
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    '''Transform: add computed columns and aggregations.'''
    df['month'] = df['date'].dt.to_period('M')
    df['revenue_bucket'] = pd.cut(
        df['revenue'],
        bins=[0, 100, 500, 2000, np.inf],
        labels=['small', 'medium', 'large', 'enterprise']
    )
    return df

def analyze(df: pd.DataFrame) -> dict:
    '''Analyze: compute KPIs.'''
    return {
        'total_revenue': df['revenue'].sum(),
        'avg_order_value': df['revenue'].mean(),
        'unique_customers': df['customer_id'].nunique(),
        'top_product': df.groupby('product')['revenue'].sum().idxmax(),
        'monthly_revenue': df.groupby('month')['revenue'].sum().to_dict()
    }

def save_outputs(df: pd.DataFrame, metrics: dict, output_dir: str = 'output'):
    '''Output: save cleaned data + metrics report.'''
    Path(output_dir).mkdir(exist_ok=True)
    df.to_csv(f'{output_dir}/clean_data.csv', index=False)
    pd.Series(metrics).to_json(f'{output_dir}/metrics.json')
    print(f"Outputs saved to {output_dir}/")

# --- Run the pipeline ---
def run_pipeline(filepath: str):
    df = load_data(filepath)
    df = clean_data(df)
    df = transform_data(df)
    metrics = analyze(df)
    save_outputs(df, metrics)
    print("\\nKey Metrics:")
    for k, v in metrics.items():
        if k != 'monthly_revenue':
            print(f"  {k}: {v}")
    return metrics
```

**Why functions?** Each stage can be tested, reused, and replaced independently. If the data source changes, you only update `load_data()`.

**Why this matters for your career:** In MS BA&AI roles, you'll own pipelines — not just one-off analyses. Reproducibility and automation are what separate junior analysts from senior ones.""",
            "worked_example": """**Scenario:** Build a monthly churn analysis pipeline that can be re-run each month on new data.

```python
import pandas as pd
import numpy as np
from pathlib import Path

def generate_sample_data(n=1000):
    '''Simulate a month of customer activity data.'''
    np.random.seed(42)
    return pd.DataFrame({
        'customer_id': range(1, n+1),
        'plan': np.random.choice(['basic','standard','premium'], n, p=[0.5, 0.35, 0.15]),
        'sessions': np.random.poisson(12, n),
        'support_tickets': np.random.poisson(0.8, n),
        'monthly_spend': np.random.normal(75, 30, n).clip(9, 500),
        'tenure_months': np.random.randint(1, 48, n),
        'churned': np.random.choice([0, 1], n, p=[0.82, 0.18])
    })

def compute_churn_metrics(df):
    '''Core analysis: churn rates by segment.'''
    overall = df['churned'].mean()
    by_plan = df.groupby('plan')['churned'].agg(['mean', 'count'])
    by_plan.columns = ['churn_rate', 'customers']
    by_plan['churn_rate'] = by_plan['churn_rate'].round(3)

    # Tenure buckets
    df['tenure_bucket'] = pd.cut(
        df['tenure_months'],
        bins=[0, 3, 12, 24, np.inf],
        labels=['new','growing','established','loyal']
    )
    by_tenure = df.groupby('tenure_bucket', observed=True)['churned'].mean().round(3)

    return {
        'overall_churn_rate': round(overall, 3),
        'by_plan': by_plan,
        'by_tenure': by_tenure,
        'total_customers': len(df),
        'churned_count': df['churned'].sum()
    }

def save_report(metrics, output_dir='churn_report'):
    Path(output_dir).mkdir(exist_ok=True)
    # Save plan breakdown
    metrics['by_plan'].to_csv(f'{output_dir}/churn_by_plan.csv')
    # Save summary
    with open(f'{output_dir}/summary.txt', 'w') as f:
        f.write(f"CHURN ANALYSIS REPORT\\n")
        f.write(f"{'='*40}\\n")
        f.write(f"Total customers: {metrics['total_customers']:,}\\n")
        f.write(f"Churned: {metrics['churned_count']:,}\\n")
        f.write(f"Overall churn rate: {metrics['overall_churn_rate']:.1%}\\n\\n")
        f.write("Churn by plan:\\n")
        f.write(metrics['by_plan'].to_string())
        f.write("\\n\\nChurn by tenure:\\n")
        f.write(metrics['by_tenure'].to_string())
    print(f"Report saved to {output_dir}/")

# Run it
df = generate_sample_data()
metrics = compute_churn_metrics(df)
save_report(metrics)

print(f"Overall churn: {metrics['overall_churn_rate']:.1%}")
print("\\nBy plan:")
print(metrics['by_plan'])
print("\\nBy tenure:")
print(metrics['by_tenure'])
```

Next month: swap `generate_sample_data()` for `pd.read_csv('march_customers.csv')` and the rest runs unchanged.""",
            "difficulty_tiers": {
                "beginner": "Write a 3-function pipeline (load, clean, summarize) for any CSV file. Each function takes a DataFrame and returns one.",
                "intermediate": "Add data validation to your pipeline that raises a ValueError if required columns are missing or if >30% of key columns are null.",
                "advanced": "Add logging (Python's `logging` module) to each pipeline stage so you can see execution progress, row counts, and timings in a log file."
            },
            "quiz": [
                {
                    "type": "multiple_choice",
                    "question": "Why should each pipeline stage (load, clean, transform) be a separate function?",
                    "options": [
                        "A) Python requires it for all data pipelines",
                        "B) Each stage can be independently tested, replaced, and reused",
                        "C) Functions are faster than inline code",
                        "D) It reduces memory usage"
                    ],
                    "answer": 1,
                    "explanation": "Modularity means each stage can be unit-tested, swapped out without affecting others, and reused in different pipelines. This is the core software engineering principle of separation of concerns."
                },
                {
                    "type": "true_false",
                    "question": "A well-designed analytics pipeline should produce identical outputs given identical inputs (reproducibility).",
                    "answer": True,
                    "explanation": "Reproducibility is a core requirement for business analytics. Stakeholders need to trust that running the pipeline again won't change the numbers. This is achieved by fixing random seeds, versioning data, and avoiding side effects."
                },
                {
                    "type": "multiple_choice",
                    "question": "What does pd.cut() do?",
                    "options": [
                        "A) Removes rows where a column exceeds a threshold",
                        "B) Slices a DataFrame by row index",
                        "C) Bins a continuous variable into labeled categories",
                        "D) Splits a DataFrame into train and test sets"
                    ],
                    "answer": 2,
                    "explanation": "pd.cut() converts a continuous numeric column into categorical buckets defined by bin edges. For example, revenue into ['small', 'medium', 'large', 'enterprise'] based on dollar thresholds."
                }
            ],
            "challenge": {
                "instructions": "Build a complete sales analytics pipeline with 4 functions: (1) load_and_validate(df) — check required columns exist and return cleaned df, (2) add_features(df) — add 'quarter' column from date and 'high_value' bool column for orders > $1000, (3) compute_kpis(df) — return dict with total_revenue, avg_order, q1/q2/q3/q4 revenue, high_value_pct, (4) run_pipeline(df) — call all 3 in order and print the KPIs.",
                "starter_code": "import pandas as pd\nimport numpy as np\n\n# Sample data\nnp.random.seed(42)\nn = 800\ndf = pd.DataFrame({\n    'order_id': range(1, n+1),\n    'date': pd.date_range('2024-01-01', periods=n, freq='12H'),\n    'customer_id': np.random.randint(1, 200, n),\n    'product': np.random.choice(['Widget','Gadget','Doohickey','Thingamajig'], n),\n    'revenue': np.random.exponential(400, n) + 50,\n    'region': np.random.choice(['North','South','East','West'], n)\n})\n\ndef load_and_validate(df):\n    required = {'date', 'customer_id', 'revenue', 'product'}\n    # Check required columns\n    # Return clean df\n    pass\n\ndef add_features(df):\n    # Add 'quarter' from date\n    # Add 'high_value' bool for revenue > 1000\n    pass\n\ndef compute_kpis(df):\n    # Return dict with total_revenue, avg_order, q1..q4 revenue, high_value_pct\n    pass\n\ndef run_pipeline(df):\n    # Call all 3 functions\n    # Print each KPI\n    pass\n\nrun_pipeline(df)\n",
                "tests": [
                    {"type": "code_contains", "value": "def load_and_validate"},
                    {"type": "code_contains", "value": "def compute_kpis"},
                    {"type": "code_contains", "value": "run_pipeline"}
                ],
                "solution": "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\nn=800\ndf=pd.DataFrame({'order_id':range(1,n+1),'date':pd.date_range('2024-01-01',periods=n,freq='12H'),'customer_id':np.random.randint(1,200,n),'product':np.random.choice(['Widget','Gadget','Doohickey','Thingamajig'],n),'revenue':np.random.exponential(400,n)+50,'region':np.random.choice(['North','South','East','West'],n)})\ndef load_and_validate(df):\n    required={'date','customer_id','revenue','product'}\n    missing=required-set(df.columns)\n    if missing: raise ValueError(f'Missing: {missing}')\n    df=df.dropna(subset=list(required))\n    df['revenue']=pd.to_numeric(df['revenue'],errors='coerce').clip(0)\n    df['date']=pd.to_datetime(df['date'])\n    return df\ndef add_features(df):\n    df=df.copy()\n    df['quarter']=df['date'].dt.quarter\n    df['high_value']=df['revenue']>1000\n    return df\ndef compute_kpis(df):\n    return {'total_revenue':df['revenue'].sum(),'avg_order':df['revenue'].mean(),'q1':df[df['quarter']==1]['revenue'].sum(),'q2':df[df['quarter']==2]['revenue'].sum(),'q3':df[df['quarter']==3]['revenue'].sum(),'q4':df[df['quarter']==4]['revenue'].sum(),'high_value_pct':df['high_value'].mean()}\ndef run_pipeline(df):\n    df=load_and_validate(df)\n    df=add_features(df)\n    kpis=compute_kpis(df)\n    for k,v in kpis.items(): print(f'{k}: {v:,.2f}' if isinstance(v,float) else f'{k}: {v:,}')\nrun_pipeline(df)"
            },
            "challenge_variations": [
                "Variation 1: Add a timing decorator to each pipeline function that prints how long it took to execute.",
                "Variation 2: Add a validate_output(df) step that checks the cleaned data has no nulls in critical columns.",
                "Variation 3: Make the pipeline accept either a filepath or a DataFrame as input (check with isinstance).",
                "Variation 4: Add error handling so the pipeline logs errors but continues processing remaining rows.",
                "Variation 5: Write unit tests for each pipeline function using assert statements.",
                "Variation 6: Extend the pipeline to save both a CSV and a JSON metrics file.",
                "Variation 7: Add a 'dry run' mode that validates and reports issues without modifying data.",
                "Variation 8: Build a pipeline that processes multiple CSVs from a folder and concatenates results.",
                "Variation 9: Add a caching step that skips cleaning if a cleaned version already exists.",
                "Variation 10: Create a pipeline config dict that controls behavior (e.g., {'drop_duplicates': True, 'revenue_clip_max': 10000}) without changing function code."
            ]
        },
        {
            "id": "m2-capstone",
            "title": "Module 2 Capstone — Customer Analytics Platform",
            "order": 26,
            "duration_min": 60,
            "concept": """**Module 2 Capstone:** You'll build a complete customer analytics platform that integrates everything from this module — NumPy, Pandas, EDA, visualization, and pipeline thinking.

**What you're building:** A reusable analytics system for a subscription SaaS business that:
- Ingests and cleans customer data
- Computes business KPIs (churn rate, CLV, cohort retention)
- Generates a formatted Excel report with multiple sheets
- Produces a visual dashboard with 4 charts
- Outputs a plain-text summary for stakeholders

**Skills integrated:**
- NumPy array operations
- Pandas: loading, cleaning, groupby, merge, pivot, datetime
- EDA: missing data, distributions, correlations
- Visualization: matplotlib multi-panel dashboard
- Excel I/O: multi-sheet report
- Pipeline pattern: modular functions

This is the kind of project you'll build in your first 90 days at a BA&AI role.""",
            "worked_example": """```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ─── 0. DATA GENERATION (replace with real CSV in practice) ──────────────────
np.random.seed(42)
n = 2000
signup_dates = pd.date_range('2022-01', '2024-01', periods=n)
df = pd.DataFrame({
    'customer_id': range(1, n+1),
    'signup_date': signup_dates,
    'plan': np.random.choice(['basic','standard','premium'], n, p=[0.45, 0.38, 0.17]),
    'country': np.random.choice(['US','UK','CA','AU','Other'], n, p=[0.55, 0.20, 0.12, 0.08, 0.05]),
    'monthly_spend': np.where(
        np.random.choice(['basic','standard','premium'], n, p=[0.45, 0.38, 0.17]) == 'basic',
        np.random.normal(29, 5, n),
        np.where(np.random.choice(['basic','standard','premium'], n, p=[0.45, 0.38, 0.17]) == 'standard',
                 np.random.normal(79, 10, n), np.random.normal(199, 25, n))
    ).clip(9, 500),
    'sessions_month': np.random.poisson(15, n),
    'support_tickets': np.random.poisson(0.7, n),
    'churned': np.random.choice([0, 1], n, p=[0.81, 0.19]),
    'tenure_months': np.random.randint(1, 25, n)
})
# Add some messy data
df.loc[np.random.choice(n, 80, replace=False), 'monthly_spend'] = np.nan
df.loc[np.random.choice(n, 30, replace=False), 'sessions_month'] = -1  # bad data
df = pd.concat([df, df.sample(50, random_state=1)])  # add duplicates

# ─── 1. CLEAN ────────────────────────────────────────────────────────────────
def clean(df):
    before = len(df)
    df = df.drop_duplicates(subset=['customer_id'])
    df['monthly_spend'] = df['monthly_spend'].fillna(df.groupby('plan')['monthly_spend'].transform('median'))
    df['sessions_month'] = df['sessions_month'].clip(lower=0)
    print(f"Cleaned: {before} → {len(df)} rows")
    return df

# ─── 2. FEATURE ENGINEERING ──────────────────────────────────────────────────
def engineer(df):
    df = df.copy()
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['cohort'] = df['signup_date'].dt.to_period('Q')
    df['estimated_clv'] = df['monthly_spend'] * (1 / 0.19) * (1 - df['churned'])
    df['high_engagement'] = df['sessions_month'] >= 20
    return df

# ─── 3. KPIs ─────────────────────────────────────────────────────────────────
def compute_kpis(df):
    return {
        'total_customers': len(df),
        'churn_rate': df['churned'].mean(),
        'avg_monthly_spend': df['monthly_spend'].mean(),
        'total_mrr': df[df['churned'] == 0]['monthly_spend'].sum(),
        'avg_clv': df['estimated_clv'].mean(),
        'avg_sessions': df['sessions_month'].mean(),
        'high_engagement_pct': df['high_engagement'].mean(),
        'churn_by_plan': df.groupby('plan')['churned'].mean().round(3).to_dict(),
        'revenue_by_plan': df.groupby('plan')['monthly_spend'].sum().round(0).to_dict()
    }

# ─── 4. VISUALIZE ─────────────────────────────────────────────────────────────
def visualize(df, kpis, output_dir):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Customer Analytics Dashboard', fontsize=16, fontweight='bold')

    # Churn rate by plan
    plans = list(kpis['churn_by_plan'].keys())
    rates = list(kpis['churn_by_plan'].values())
    colors = ['#e74c3c' if r > 0.2 else '#2ecc71' for r in rates]
    axes[0, 0].bar(plans, rates, color=colors)
    axes[0, 0].set_title('Churn Rate by Plan')
    axes[0, 0].set_ylabel('Churn Rate')
    axes[0, 0].axhline(kpis['churn_rate'], color='gray', linestyle='--', label='Overall avg')
    axes[0, 0].legend()

    # Monthly spend distribution
    for plan in ['basic', 'standard', 'premium']:
        subset = df[df['plan'] == plan]['monthly_spend']
        axes[0, 1].hist(subset, bins=25, alpha=0.6, label=plan)
    axes[0, 1].set_title('Monthly Spend Distribution by Plan')
    axes[0, 1].set_xlabel('Monthly Spend ($)')
    axes[0, 1].legend()

    # Sessions vs Churn (box plot by plan)
    churned_labels = df['churned'].map({0: 'Retained', 1: 'Churned'})
    for i, status in enumerate(['Retained', 'Churned']):
        data = df[churned_labels == status]['sessions_month']
        axes[1, 0].boxplot(data, positions=[i], widths=0.5)
    axes[1, 0].set_xticks([0, 1])
    axes[1, 0].set_xticklabels(['Retained', 'Churned'])
    axes[1, 0].set_title('Sessions: Retained vs Churned')
    axes[1, 0].set_ylabel('Sessions / Month')

    # Revenue by plan (horizontal bar)
    rev = pd.Series(kpis['revenue_by_plan']).sort_values()
    axes[1, 1].barh(rev.index, rev.values, color='steelblue')
    axes[1, 1].set_title('Total Revenue by Plan')
    axes[1, 1].set_xlabel('Total Monthly Revenue ($)')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/dashboard.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Dashboard saved.")

# ─── 5. EXCEL REPORT ──────────────────────────────────────────────────────────
def export_excel(df, kpis, output_dir):
    kpi_df = pd.DataFrame([
        {'Metric': k, 'Value': v}
        for k, v in kpis.items()
        if not isinstance(v, dict)
    ])
    plan_df = pd.DataFrame([
        {'Plan': k, 'Churn Rate': v, 'Monthly Revenue': kpis['revenue_by_plan'].get(k, 0)}
        for k, v in kpis['churn_by_plan'].items()
    ])
    with pd.ExcelWriter(f'{output_dir}/customer_report.xlsx', engine='openpyxl') as writer:
        kpi_df.to_excel(writer, sheet_name='KPIs', index=False)
        plan_df.to_excel(writer, sheet_name='By Plan', index=False)
        df[df['churned'] == 1][['customer_id', 'plan', 'monthly_spend', 'tenure_months']].to_excel(
            writer, sheet_name='Churned Customers', index=False)
    print("Excel report saved.")

# ─── 6. RUN PIPELINE ──────────────────────────────────────────────────────────
Path('capstone_output').mkdir(exist_ok=True)
df = clean(df)
df = engineer(df)
kpis = compute_kpis(df)
visualize(df, kpis, 'capstone_output')
export_excel(df, kpis, 'capstone_output')

print(f"\\nBusiness Summary:")
print(f"  Total customers: {kpis['total_customers']:,}")
print(f"  Monthly churn: {kpis['churn_rate']:.1%}")
print(f"  Total MRR: ${kpis['total_mrr']:,.0f}")
print(f"  Avg CLV: ${kpis['avg_clv']:,.0f}")
print(f"  High engagement: {kpis['high_engagement_pct']:.1%}")
```""",
            "difficulty_tiers": {
                "beginner": "Complete the capstone by running the provided code and modifying one section (e.g., change the chart colors or add a fifth KPI to the summary).",
                "intermediate": "Extend the capstone to include a cohort retention analysis: group customers by signup quarter and compute the churn rate for each cohort.",
                "advanced": "Add a risk scoring model to the pipeline: compute a 'churn_risk_score' per customer based on tenure, sessions, support tickets, and plan type using a weighted formula. Output the top 50 highest-risk active customers."
            },
            "quiz": [
                {
                    "type": "multiple_choice",
                    "question": "In the capstone, why do we use df.groupby('plan')['monthly_spend'].transform('median') to fill missing spend values?",
                    "options": [
                        "A) transform() is required when using fillna()",
                        "B) It fills each row's NaN with the median for that row's plan group, preserving the original DataFrame index",
                        "C) It's faster than using the global median",
                        "D) transform() automatically handles all missing values"
                    ],
                    "answer": 1,
                    "explanation": "transform('median') returns a Series with the same index as the original DataFrame, so each NaN row gets the median for its specific plan group. Using .mean() on the group would return a shorter Series that can't be used with fillna() directly."
                },
                {
                    "type": "true_false",
                    "question": "Customer Lifetime Value (CLV) can be estimated as: monthly_spend × (1 / churn_rate).",
                    "answer": True,
                    "explanation": "If the monthly churn rate is 19%, the expected customer lifespan is 1/0.19 ≈ 5.3 months. Multiplying by monthly spend gives a simple CLV estimate. Real CLV models are more complex but this is a valid first approximation."
                },
                {
                    "type": "multiple_choice",
                    "question": "When exporting to Excel with pd.ExcelWriter, what does engine='openpyxl' specify?",
                    "options": [
                        "A) The version of pandas to use",
                        "B) The file format (xlsx vs xls)",
                        "C) The underlying library used to write .xlsx files",
                        "D) The sheet creation order"
                    ],
                    "answer": 2,
                    "explanation": "openpyxl is the Python library that writes .xlsx format. pandas uses it as the 'engine' under the hood. xlsxwriter is another option with more formatting capabilities but no reading support."
                }
            ],
            "challenge": {
                "instructions": "Extend the capstone with a cohort analysis: (1) create a 'signup_quarter' column, (2) for each cohort (Q1 2022, Q2 2022, etc.), compute: number of customers, churn rate, average monthly spend, (3) identify the cohort with the lowest churn rate, (4) save cohort results as a new sheet 'Cohort Analysis' in the Excel report.",
                "starter_code": "# Run the full capstone code above first, then add:\n\n# 1. Cohort analysis\ncohort_df = df.copy()\ncohort_df['signup_quarter'] = # extract quarter from signup_date\n\n# 2. Compute per-cohort metrics\ncohort_metrics = cohort_df.groupby('signup_quarter').agg(\n    customers=('customer_id', 'count'),\n    churn_rate=('churned', 'mean'),\n    avg_spend=('monthly_spend', 'mean')\n).round(3)\n\n# 3. Best cohort (lowest churn)\nbest_cohort = # find cohort with min churn_rate\nprint(f\"Best cohort: {best_cohort} ({cohort_metrics.loc[best_cohort, 'churn_rate']:.1%} churn)\")\n\n# 4. Save to Excel (add to existing report or create new file)\nwith pd.ExcelWriter('capstone_output/cohort_report.xlsx', engine='openpyxl') as writer:\n    cohort_metrics.to_excel(writer, sheet_name='Cohort Analysis')\nprint(cohort_metrics)\n",
                "tests": [
                    {"type": "code_contains", "value": "signup_quarter"},
                    {"type": "code_contains", "value": "groupby"},
                    {"type": "code_contains", "value": "churn_rate"}
                ],
                "solution": "cohort_df=df.copy()\ncohort_df['signup_quarter']=pd.to_datetime(cohort_df['signup_date']).dt.to_period('Q')\ncohort_metrics=cohort_df.groupby('signup_quarter').agg(customers=('customer_id','count'),churn_rate=('churned','mean'),avg_spend=('monthly_spend','mean')).round(3)\nbest_cohort=cohort_metrics['churn_rate'].idxmin()\nprint(f'Best cohort: {best_cohort} ({cohort_metrics.loc[best_cohort,\"churn_rate\"]:.1%} churn)')\nfrom pathlib import Path\nPath('capstone_output').mkdir(exist_ok=True)\nwith pd.ExcelWriter('capstone_output/cohort_report.xlsx',engine='openpyxl') as writer:\n    cohort_metrics.to_excel(writer,sheet_name='Cohort Analysis')\nprint(cohort_metrics)"
            },
            "challenge_variations": [
                "Variation 1: Add a month-over-month churn trend chart to the dashboard (show if churn is improving or worsening).",
                "Variation 2: Compute Net Revenue Retention (NRR) by cohort: total revenue from retained customers / original cohort revenue.",
                "Variation 3: Build a customer health score (0-100) based on sessions, spend, tenure, and support tickets.",
                "Variation 4: Add a 'top 100 customers at risk' table sorted by highest spend AND high churn probability.",
                "Variation 5: Create a heatmap of churn rate by plan × country.",
                "Variation 6: Compute the payback period: average months until a customer's revenue exceeds acquisition cost (assume $50 CAC).",
                "Variation 7: Add a product usage funnel analysis: % of customers who used the product 0, 1-5, 6-15, 15+ times.",
                "Variation 8: Build a simple RFM (Recency, Frequency, Monetary) segmentation and visualize the segments.",
                "Variation 9: Add an automated insight generator that prints 3 key findings in plain English based on the KPI values.",
                "Variation 10: Schedule the pipeline to auto-run on the first of each month using Python's schedule library."
            ]
        }
    ]
}

