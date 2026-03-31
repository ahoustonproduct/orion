MODULE_3 = {
    "id": "module3",
    "title": "Structured Data & SQL",
    "description": "Learn to speak the language of databases. SQL is the universal tool for querying, analyzing, and managing structured data — used by every data analyst on the planet.",
    "course": "MSBX 5405 · Structured Data & SQL",
    "order": 3,
    "locked": False,
    "supplementary_courses": [
        {
            "title": "Databases and SQL for Data Science with Python",
            "provider": "IBM",
            "url": "https://www.coursera.org/learn/sql-data-science",
            "duration": "~2 weeks at 10 hrs/week",
            "level": "Beginner",
            "free_audit": True,
            "description": "SQL basics, querying, filtering, sorting, aggregating, joins, subqueries, and accessing databases from Python. Covers SELECT, INSERT, UPDATE, DELETE, GROUP BY, and real-world datasets with IBM Db2.",
        },
    ],
    "concept_map": [
        {"id": "m3-l1",  "label": "What is a Database?",           "connects_to": ["m3-l2"]},
        {"id": "m3-l2",  "label": "Tables, Rows & Columns",        "connects_to": ["m3-l3"]},
        {"id": "m3-l3",  "label": "SELECT & FROM",                 "connects_to": ["m3-l4"]},
        {"id": "m3-l4",  "label": "Filtering with WHERE",          "connects_to": ["m3-l5"]},
        {"id": "m3-l5",  "label": "Sorting with ORDER BY",         "connects_to": ["m3-l6"]},
        {"id": "m3-l6",  "label": "LIMIT / TOP",                   "connects_to": ["m3-l7"]},
        {"id": "m3-l7",  "label": "Aggregation Functions",         "connects_to": ["m3-l8"]},
        {"id": "m3-l8",  "label": "GROUP BY",                      "connects_to": ["m3-l9"]},
        {"id": "m3-l9",  "label": "HAVING",                        "connects_to": ["m3-l10"]},
        {"id": "m3-l10", "label": "INNER JOIN",                    "connects_to": ["m3-l11"]},
        {"id": "m3-l11", "label": "LEFT & RIGHT JOIN",             "connects_to": ["m3-l12"]},
        {"id": "m3-l12", "label": "Multiple JOINs & Aliases",      "connects_to": ["m3-l13"]},
        {"id": "m3-l13", "label": "Subqueries",                    "connects_to": ["m3-l14"]},
        {"id": "m3-l14", "label": "Primary & Foreign Keys",        "connects_to": ["m3-l15"]},
        {"id": "m3-l15", "label": "Normalization",                 "connects_to": ["m3-l16"]},
        {"id": "m3-l16", "label": "ERDs",                          "connects_to": ["m3-l17"]},
        {"id": "m3-l17", "label": "CREATE TABLE",                  "connects_to": ["m3-l18"]},
        {"id": "m3-l18", "label": "INSERT INTO",                   "connects_to": ["m3-l19"]},
        {"id": "m3-l19", "label": "UPDATE & DELETE",               "connects_to": ["m3-l20"]},
        {"id": "m3-l20", "label": "Python + SQLite",               "connects_to": ["m3-l21"]},
        {"id": "m3-l21", "label": "Parameterized Queries",         "connects_to": ["m3-l22"]},
        {"id": "m3-l22", "label": "SQLAlchemy ORM",                "connects_to": ["m3-l23"]},
        {"id": "m3-l23", "label": "CASE, COALESCE, NULLIF",        "connects_to": ["m3-l24"]},
        {"id": "m3-l24", "label": "Views & Indexes",               "connects_to": ["m3-l25"]},
        {"id": "m3-l25", "label": "Window Functions",              "connects_to": ["m3-capstone"]},
        {"id": "m3-capstone", "label": "Capstone: Sales Database", "connects_to": []},
    ],
    "lessons": [
        # ── LESSON 1 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l1",
            "title": "What is a Database?",
            "order": 1,
            "duration_min": 15,
            "real_world_context": "Every company stores its data in databases — customer records, sales transactions, inventory. As a business analyst, SQL lets you pull exactly the data you need without waiting for an engineer.",
            "concept": """A **database** is an organized collection of data stored so it can be easily accessed, managed, and updated. Think of it as a highly disciplined filing system — but instead of paper folders, data lives in structured tables that can be searched and combined in milliseconds.

**Relational vs Flat File**

A **flat file** is a single spreadsheet: one tab, all data in one place. It works fine for a few hundred rows. But imagine a company with 500,000 customer orders — the spreadsheet bloats, data gets duplicated everywhere, and one typo in a customer's name creates inconsistencies across thousands of rows.

A **relational database** splits data into multiple related tables. Customer information lives in one table, orders in another, products in a third. They're linked by shared ID columns. This eliminates duplication and keeps data consistent.

```sql
-- A flat file might have this repeated for every order:
-- customer_name | customer_email     | product | price
-- Alice Smith   | alice@example.com  | Laptop  | 999.00
-- Alice Smith   | alice@example.com  | Mouse   |  29.00

-- A relational database instead stores:
-- customers table:  id=1, name='Alice Smith', email='alice@example.com'
-- orders table:     id=101, customer_id=1, product='Laptop', price=999.00
-- orders table:     id=102, customer_id=1, product='Mouse',  price=29.00
```

**Why databases beat spreadsheets for business**

- **Scale**: databases handle billions of rows without slowing down
- **Concurrency**: thousands of users can read/write at the same time
- **Integrity**: rules prevent bad data (e.g., no order without a valid customer)
- **SQL**: a universal query language understood by every major database system

**Common database systems you'll encounter**: SQLite (lightweight, file-based, great for learning), PostgreSQL (open-source powerhouse), MySQL (web applications), Microsoft SQL Server (enterprise), Snowflake (cloud data warehousing).

As a business analyst, you'll query these systems daily — pulling sales figures, customer segments, KPIs — all using the same core SQL you'll learn here.""",
            "worked_example": {
                "description": "Let's look at how the same business data looks as a flat file vs a relational database.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Relational approach: two separate tables
cursor.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')
cursor.execute('''
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT,
        price REAL
    )
''')

cursor.executemany('INSERT INTO customers VALUES (?,?,?)', [
    (1, 'Alice Smith',  'alice@example.com'),
    (2, 'Bob Johnson',  'bob@example.com'),
])
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', [
    (101, 1, 'Laptop', 999.00),
    (102, 1, 'Mouse',   29.00),
    (103, 2, 'Keyboard',79.00),
])

# Alice's email is stored ONCE — no duplication
cursor.execute('SELECT * FROM customers')
print('Customers:', cursor.fetchall())

cursor.execute('SELECT * FROM orders')
print('Orders:', cursor.fetchall())""",
                "explanation": "Notice that Alice's email appears only once in the customers table. Every order just references her ID (1). If she changes her email, you update one row — not thousands of order records. This is the core power of relational design."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "Relational DB = multiple linked tables",
                    "Primary key = unique row identifier",
                    "SQL = Structured Query Language",
                ],
                "notes": "SQLite is built into Python's standard library — no installation needed. Perfect for learning and small apps."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What is the main advantage of a relational database over a flat file (spreadsheet)?",
                    "options": [
                        "A. It can only store numbers, not text",
                        "B. It eliminates data duplication by splitting data into linked tables",
                        "C. It requires no programming knowledge to use",
                        "D. It stores data in XML format"
                    ],
                    "answer": 1,
                    "explanation": "Relational databases eliminate duplication by storing each piece of information once and linking tables via shared ID columns."
                },
                {
                    "type": "true_false",
                    "question": "SQLite requires a separate server installation to use with Python.",
                    "answer": False,
                    "explanation": "SQLite is built into Python's standard library. You just 'import sqlite3' — no installation needed."
                },
                {
                    "type": "fill_blank",
                    "question": "The language used to query relational databases is called ___.",
                    "template": "___ (Structured Query Language)",
                    "answer": "SQL",
                    "explanation": "SQL stands for Structured Query Language. It's the universal language for interacting with relational databases."
                }
            ],
            "challenge": {
                "instructions": "Create two tables in an in-memory SQLite database: 'products' (id, name, category, price) and 'sales' (id, product_id, quantity, sale_date). Insert 3 products and 4 sales records. Then query and print all rows from both tables. This simulates a real retail database structure.",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create the products table
cursor.execute('''
    CREATE TABLE products (
        id       INTEGER PRIMARY KEY,
        name     TEXT,
        category TEXT,
        price    REAL
    )
''')

# Create the sales table
cursor.execute('''
    CREATE TABLE sales (
        id         INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity   INTEGER,
        sale_date  TEXT
    )
''')

# Insert 3 products
# cursor.executemany(...)

# Insert 4 sales records
# cursor.executemany(...)

# Query and print both tables
""",
                "tests": [
                    {"type": "output_contains", "value": "products"},
                    {"type": "code_contains", "value": "CREATE TABLE"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)''')
cursor.execute('''CREATE TABLE sales (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, sale_date TEXT)''')

cursor.executemany('INSERT INTO products VALUES (?,?,?,?)', [
    (1, 'Laptop',   'Electronics', 999.00),
    (2, 'Mouse',    'Electronics',  29.00),
    (3, 'Notebook', 'Stationery',    4.99),
])
cursor.executemany('INSERT INTO sales VALUES (?,?,?,?)', [
    (1, 1, 2, '2024-01-15'),
    (2, 2, 5, '2024-01-15'),
    (3, 3, 10,'2024-01-16'),
    (4, 1, 1, '2024-01-17'),
])

print('products:', cursor.execute('SELECT * FROM products').fetchall())
print('sales:',    cursor.execute('SELECT * FROM sales').fetchall())
conn.close()"""
            },
            "challenge_variations": [
                "Create a 'customers' and 'appointments' table for a medical clinic, insert sample data, and print both.",
                "Build a 'employees' and 'departments' table for an HR system with 4 employees and 3 departments.",
                "Create 'books' and 'loans' tables for a library system; insert 5 books and 6 loan records.",
                "Design 'flights' and 'passengers' tables for an airline; insert 3 flights and 6 passenger bookings.",
                "Build 'restaurants' and 'reviews' tables; insert 3 restaurants and 5 reviews with star ratings.",
                "Create 'courses' and 'enrollments' tables for a university; insert 4 courses and 8 enrollments.",
                "Design 'vendors' and 'invoices' tables for accounts payable; insert 3 vendors and 6 invoices.",
                "Build 'warehouses' and 'inventory' tables; insert 2 warehouses and 10 inventory line items.",
                "Create 'projects' and 'tasks' tables for a project management app; insert 2 projects and 8 tasks.",
                "Design 'athletes' and 'results' tables for a sports league; insert 4 athletes and 8 race results."
            ]
        },

        # ── LESSON 2 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l2",
            "title": "Tables, Rows, and Columns",
            "order": 2,
            "duration_min": 15,
            "real_world_context": "Before writing a single query, you need to understand how data is physically organized. Every database you'll ever work with — from a startup's SQLite file to Snowflake's petabyte warehouse — uses this same table structure.",
            "concept": """A database **table** is like a spreadsheet tab — but with strict rules. Every table has a fixed set of **columns** (also called fields or attributes), and each **row** (also called a record or tuple) represents one entity.

```
Table: customers
┌────┬──────────────┬───────────────────┬─────────┐
│ id │ name         │ email             │ city    │
├────┼──────────────┼───────────────────┼─────────┤
│  1 │ Alice Smith  │ alice@example.com │ Denver  │  ← row 1
│  2 │ Bob Johnson  │ bob@example.com   │ Austin  │  ← row 2
│  3 │ Carol White  │ carol@example.com │ Denver  │  ← row 3
└────┴──────────────┴───────────────────┴─────────┘
         ↑ column       ↑ column           ↑ column
```

**Columns** define the *structure* — what kind of data this table holds. Each column has a **data type**: TEXT (strings), INTEGER (whole numbers), REAL (decimals), DATE, BOOLEAN, etc.

**Rows** hold the *data* — one row = one customer, one order, one product. Every row in a well-designed table represents exactly one "thing."

**Primary Key (PK)**

The `id` column above is a **primary key** — a column (or combination of columns) that uniquely identifies each row. Rules for primary keys:
- Must be unique across all rows (no two customers can share an id)
- Cannot be NULL (empty)
- Usually an auto-incrementing integer: 1, 2, 3, 4...

Think of it as a social security number for your data rows.

```sql
-- Checking a table's structure (SQLite syntax)
PRAGMA table_info(customers);
-- Returns: column names, types, whether nullable, primary key info

-- Seeing all tables in a SQLite database
SELECT name FROM sqlite_master WHERE type='table';
```

**Null values**

NULL means "unknown" or "missing" — it's not zero, not an empty string, it's the *absence* of a value. A customer with no phone number has NULL in the phone column. This matters a lot when filtering and aggregating data.""",
            "worked_example": {
                "description": "Let's inspect a real table structure and understand what each piece means.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE employees (
        id         INTEGER PRIMARY KEY,
        first_name TEXT    NOT NULL,
        last_name  TEXT    NOT NULL,
        department TEXT,
        salary     REAL,
        hire_date  TEXT
    )
''')

cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?,?)', [
    (1, 'Alice', 'Smith',   'Engineering', 95000, '2021-03-15'),
    (2, 'Bob',   'Johnson', 'Marketing',   72000, '2020-07-01'),
    (3, 'Carol', 'White',   'Engineering', 88000, '2022-01-10'),
    (4, 'Dave',  'Brown',   None,          65000, '2023-05-20'),  # NULL department
])

# Inspect the table structure
print('=== Table Structure ===')
for row in cursor.execute('PRAGMA table_info(employees)'):
    print(row)
# Output: (cid, name, type, notnull, dflt_value, pk)

print()
print('=== All Rows ===')
for row in cursor.execute('SELECT * FROM employees'):
    print(row)""",
                "explanation": "PRAGMA table_info shows column index (cid), name, type, whether NOT NULL is enforced, default value, and whether it's a primary key (1=yes). Row 4 shows None in Python — that's a NULL value in SQLite. Dave's department is unknown."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "PRAGMA table_info(tablename);  -- inspect structure",
                    "SELECT name FROM sqlite_master WHERE type='table';",
                    "PRIMARY KEY -- unique, non-null row identifier",
                    "NULL -- missing/unknown value (not zero, not empty string)"
                ],
                "notes": "In Python, SQLite NULL values come back as None. Always check for None when processing query results."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A primary key column must be:",
                    "options": [
                        "A. Always an integer",
                        "B. Unique and non-NULL for every row",
                        "C. The first column in the table",
                        "D. Less than 100 characters"
                    ],
                    "answer": 1,
                    "explanation": "A primary key must be unique (no duplicates) and NOT NULL. It can be an integer, text, or other types — it just must uniquely identify each row."
                },
                {
                    "type": "true_false",
                    "question": "NULL in SQL is the same as the number zero.",
                    "answer": False,
                    "explanation": "NULL means 'unknown' or 'missing' — it is completely different from zero or an empty string. NULL comparisons require special syntax like IS NULL, not = NULL."
                },
                {
                    "type": "fill_blank",
                    "question": "To inspect a table's column structure in SQLite, use: ___ table_info(tablename);",
                    "template": "___ table_info(employees);",
                    "answer": "PRAGMA",
                    "explanation": "PRAGMA is SQLite's way of running special administrative commands. PRAGMA table_info() returns column details for a given table."
                }
            ],
            "challenge": {
                "instructions": "Create a 'products' table with columns: id (PRIMARY KEY), name (TEXT, NOT NULL), category (TEXT), price (REAL), stock_quantity (INTEGER), and discontinued (INTEGER — stores 0 or 1). Insert 5 products including one with a NULL category. Then use PRAGMA table_info to print the structure, and SELECT * to print all rows.",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create products table with all specified columns
cursor.execute('''
    CREATE TABLE products (
        -- your columns here
    )
''')

# Insert 5 products (one with NULL category)
cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', [
    # your data here
])

# Print table structure using PRAGMA
print('=== Structure ===')
# your code here

# Print all rows
print('=== Data ===')
# your code here
""",
                "tests": [
                    {"type": "output_contains", "value": "Structure"},
                    {"type": "code_contains", "value": "PRAGMA table_info"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE products (
        id             INTEGER PRIMARY KEY,
        name           TEXT    NOT NULL,
        category       TEXT,
        price          REAL,
        stock_quantity INTEGER,
        discontinued   INTEGER
    )
''')

cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', [
    (1, 'Laptop',     'Electronics', 999.00, 50, 0),
    (2, 'Mouse',      'Electronics',  29.00, 200, 0),
    (3, 'Notebook',   'Stationery',    4.99, 500, 0),
    (4, 'Old Pager',  None,           15.00,   2, 1),
    (5, 'USB Hub',    'Electronics',  39.99, 150, 0),
])

print('=== Structure ===')
for row in cursor.execute('PRAGMA table_info(products)'):
    print(row)

print('=== Data ===')
for row in cursor.execute('SELECT * FROM products'):
    print(row)
conn.close()"""
            },
            "challenge_variations": [
                "Create an 'employees' table with 7 columns including nullable 'manager_id'; insert 5 rows and inspect with PRAGMA.",
                "Build a 'students' table with GPA (REAL), enrollment_year, and major; insert 6 students including one with NULL major.",
                "Design a 'transactions' table for a bank with account_id, amount, transaction_type, and timestamp; insert 8 rows.",
                "Create a 'vehicles' table with make, model, year, mileage, and owner_id; insert 5 vehicles with one NULL owner.",
                "Build a 'recipes' table with name, cuisine, prep_time_mins, servings; insert 4 recipes and verify structure.",
                "Design an 'events' table with title, venue, start_date, capacity, and ticket_price; insert 5 events.",
                "Create a 'movies' table with title, director, release_year, rating, box_office_millions; insert 6 movies.",
                "Build a 'sensors' table with sensor_id, location, reading_value, reading_time; insert 8 sensor readings.",
                "Design a 'job_postings' table with title, company, salary_min, salary_max, remote (0/1); insert 5 postings.",
                "Create a 'shipments' table with tracking_id, origin, destination, weight_kg, delivered (0/1); insert 6 rows."
            ]
        },

        # ── LESSON 3 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l3",
            "title": "Your First SQL Query — SELECT and FROM",
            "order": 3,
            "duration_min": 15,
            "real_world_context": "SELECT is the workhorse of SQL. 90% of what a business analyst does is reading data — pulling reports, checking numbers, answering questions. SELECT is how you do all of it.",
            "concept": """The **SELECT** statement retrieves data from a table. Every SQL query you write for data analysis starts with SELECT.

**The basic structure:**
```sql
SELECT column1, column2
FROM table_name;
```

**Select all columns with *:**
```sql
SELECT * FROM customers;
-- Returns every column for every row
-- * means "all columns" — useful for exploration, avoid in production
```

**Select specific columns:**
```sql
SELECT name, email FROM customers;
-- Returns only the name and email columns
-- More efficient — doesn't transfer data you don't need
```

**Column order matters in SELECT:**
```sql
SELECT email, name FROM customers;
-- Returns columns in the order you list them, not table order
```

**SQL syntax rules:**
- Statements end with a semicolon `;`
- SQL keywords (SELECT, FROM, WHERE) are case-insensitive but UPPERCASE by convention
- Table and column names are also case-insensitive in most databases
- Whitespace and line breaks don't matter — format for readability
- String values use single quotes: `'Alice'` not `"Alice"`

**Giving columns friendly names with AS:**
```sql
SELECT name AS customer_name, email AS contact_email
FROM customers;
-- Renames columns in the output (doesn't change the table)
```

**SELECT without a table (for quick calculations):**
```sql
SELECT 2 + 2;          -- Returns 4
SELECT 'Hello World';  -- Returns the string
SELECT date('now');    -- Returns today's date (SQLite)
```""",
            "worked_example": {
                "description": "Let's query a sales database three different ways to see how SELECT shapes the output.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT, annual_spend REAL
)''')
cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?)', [
    (1, 'Alice Smith',  'alice@co.com', 'Denver', 12500.00),
    (2, 'Bob Johnson',  'bob@co.com',   'Austin',  8750.50),
    (3, 'Carol White',  'carol@co.com', 'Denver', 21000.00),
    (4, 'Dave Brown',   'dave@co.com',  'Seattle',  3200.75),
])

# Query 1: All columns
print('=== All Columns ===')
for row in cursor.execute('SELECT * FROM customers'):
    print(row)

# Query 2: Specific columns only
print('\n=== Names and Cities Only ===')
for row in cursor.execute('SELECT name, city FROM customers'):
    print(row)

# Query 3: With column aliases
print('\n=== With Aliases ===')
for row in cursor.execute('SELECT name AS customer, annual_spend AS spend FROM customers'):
    print(row)""",
                "explanation": "Query 1 returns all 5 columns. Query 2 returns only 2 — more focused. Query 3 renames the columns in output using AS. The underlying table is never modified. Aliases only affect what you see in the result."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "SELECT * FROM table;",
                    "SELECT col1, col2 FROM table;",
                    "SELECT col AS alias FROM table;",
                    "-- This is a SQL comment",
                    "/* Multi-line comment */"
                ],
                "notes": "Use SELECT * only for exploration. In production queries, always name your columns explicitly so your query doesn't break if someone adds a column to the table."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does SELECT * FROM orders; do?",
                    "options": [
                        "A. Deletes all rows from orders",
                        "B. Creates a new table called orders",
                        "C. Returns every column and every row from the orders table",
                        "D. Returns only the first row from orders"
                    ],
                    "answer": 2,
                    "explanation": "SELECT * means 'select all columns'. FROM orders specifies the table. Together they return the complete orders table."
                },
                {
                    "type": "true_false",
                    "question": "The AS keyword permanently renames a column in the database table.",
                    "answer": False,
                    "explanation": "AS creates an alias only in the query output. The actual table column name is never changed. It's purely cosmetic for the result set."
                },
                {
                    "type": "fill_blank",
                    "question": "To select only the 'product' and 'price' columns from a 'sales' table:",
                    "template": "SELECT product, ___ FROM sales;",
                    "answer": "price",
                    "explanation": "List the column names separated by commas after SELECT. Only those columns will appear in the result."
                }
            ],
            "challenge": {
                "instructions": "You have a 'products' table with columns: id, name, category, price, stock. Write three queries: (1) select all columns, (2) select only name and price, (3) select name and price but alias them as 'product_name' and 'unit_price'. Print results of all three.",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER
)''')
cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', [
    (1, 'Laptop',   'Electronics', 999.00, 50),
    (2, 'Mouse',    'Electronics',  29.00, 200),
    (3, 'Notebook', 'Stationery',    4.99, 500),
    (4, 'USB Hub',  'Electronics',  39.99, 150),
    (5, 'Pen Pack', 'Stationery',    6.49, 800),
])

# Query 1: All columns
print('=== All Columns ===')
# your query here

# Query 2: Only name and price
print('\\n=== Name and Price ===')
# your query here

# Query 3: With aliases product_name and unit_price
print('\\n=== With Aliases ===')
# your query here
""",
                "tests": [
                    {"type": "output_contains", "value": "Laptop"},
                    {"type": "code_contains", "value": "AS"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER
)''')
cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', [
    (1, 'Laptop',   'Electronics', 999.00, 50),
    (2, 'Mouse',    'Electronics',  29.00, 200),
    (3, 'Notebook', 'Stationery',    4.99, 500),
    (4, 'USB Hub',  'Electronics',  39.99, 150),
    (5, 'Pen Pack', 'Stationery',    6.49, 800),
])

print('=== All Columns ===')
for row in cursor.execute('SELECT * FROM products'):
    print(row)

print('\\n=== Name and Price ===')
for row in cursor.execute('SELECT name, price FROM products'):
    print(row)

print('\\n=== With Aliases ===')
for row in cursor.execute('SELECT name AS product_name, price AS unit_price FROM products'):
    print(row)
conn.close()"""
            },
            "challenge_variations": [
                "Query an 'employees' table: select all, then just name+salary, then alias them as 'staff' and 'compensation'.",
                "From a 'movies' table, select all columns, then just title+year, then alias as 'film' and 'released'.",
                "Query a 'customers' table: all columns, then email+city only, then alias email as 'contact'.",
                "From an 'orders' table, select all columns then only order_date and total, aliased as 'date' and 'amount'.",
                "Query 'inventory': all columns, then item_name+quantity, then alias quantity as 'units_on_hand'.",
                "From a 'flights' table, select origin and destination aliased as 'from_city' and 'to_city'.",
                "Query 'students': all columns, then student_name+gpa, alias gpa as 'grade_point_average'.",
                "From 'sales_reps', select name+region+quota, aliasing quota as 'sales_target'.",
                "Query 'projects': all columns, then project_name+budget, alias budget as 'approved_budget'.",
                "From a 'sensors' table, select sensor_id and reading_value aliased as 'sensor' and 'measurement'."
            ]
        },

        # ── LESSON 4 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l4",
            "title": "Filtering with WHERE",
            "order": 4,
            "duration_min": 20,
            "real_world_context": "A real customer table might have millions of rows. WHERE is how you zero in on exactly what you need — find all customers in one city, orders above a certain amount, products running low on stock.",
            "concept": """The **WHERE** clause filters rows — only rows that match the condition are returned.

```sql
SELECT * FROM customers WHERE city = 'Denver';
-- Returns only Denver customers
```

**Comparison operators:**
```sql
=    equal to              WHERE price = 29.99
!=   not equal             WHERE status != 'cancelled'
<>   not equal (same)      WHERE status <> 'cancelled'
>    greater than          WHERE salary > 50000
<    less than             WHERE stock < 10
>=   greater than or equal WHERE age >= 21
<=   less than or equal    WHERE price <= 100
```

**Combining conditions with AND / OR / NOT:**
```sql
-- AND: both conditions must be true
SELECT * FROM orders WHERE amount > 500 AND status = 'shipped';

-- OR: either condition is true
SELECT * FROM customers WHERE city = 'Denver' OR city = 'Austin';

-- NOT: inverts the condition
SELECT * FROM products WHERE NOT category = 'Electronics';
```

**Filtering text — LIKE for pattern matching:**
```sql
-- % matches any number of characters
SELECT * FROM customers WHERE name LIKE 'A%';    -- starts with A
SELECT * FROM customers WHERE email LIKE '%@gmail.com';  -- gmail users
SELECT * FROM products WHERE name LIKE '%Pro%';  -- contains 'Pro'

-- _ matches exactly one character
SELECT * FROM products WHERE code LIKE 'A_1';    -- A, any char, 1
```

**IN — match any value in a list:**
```sql
SELECT * FROM customers WHERE city IN ('Denver', 'Austin', 'Seattle');
-- Much cleaner than: WHERE city='Denver' OR city='Austin' OR city='Seattle'
```

**BETWEEN — range filtering (inclusive):**
```sql
SELECT * FROM orders WHERE amount BETWEEN 100 AND 500;
SELECT * FROM employees WHERE hire_date BETWEEN '2020-01-01' AND '2022-12-31';
```

**NULL filtering — IS NULL / IS NOT NULL:**
```sql
SELECT * FROM employees WHERE manager_id IS NULL;      -- top-level managers
SELECT * FROM customers WHERE phone IS NOT NULL;       -- has a phone number
-- WARNING: WHERE phone = NULL will NOT work — always use IS NULL
```""",
            "worked_example": {
                "description": "Let's filter a sales database using multiple WHERE techniques to answer real business questions.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE orders (
    id INTEGER PRIMARY KEY, customer TEXT, product TEXT,
    amount REAL, status TEXT, region TEXT
)''')
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', [
    (1,  'Alice',  'Laptop',   999.00, 'shipped',   'West'),
    (2,  'Bob',    'Mouse',     29.00, 'pending',   'East'),
    (3,  'Carol',  'Keyboard',  79.00, 'shipped',   'West'),
    (4,  'Dave',   'Monitor',  349.00, 'cancelled', 'East'),
    (5,  'Eve',    'Laptop',   999.00, 'shipped',   'West'),
    (6,  'Frank',  'Mouse',     29.00, 'pending',   'Central'),
    (7,  'Grace',  'Monitor',  349.00, 'shipped',   'East'),
    (8,  'Henry',  'Keyboard',  79.00, 'shipped',   'Central'),
])

# High-value shipped orders
print('=== Shipped orders over $100 ===')
for row in cursor.execute(\'\'\'
    SELECT customer, product, amount
    FROM orders
    WHERE status = 'shipped' AND amount > 100
'''):
    print(row)

# West or Central region
print('\\n=== West or Central ===')
for row in cursor.execute(\'\'\'
    SELECT customer, region FROM orders
    WHERE region IN ('West', 'Central')
'''):
    print(row)

# Pattern match
print('\\n=== Products with double letters (LIKE) ===')
for row in cursor.execute(\'\'\'
    SELECT DISTINCT product FROM orders WHERE product LIKE '%o%'
'''):
    print(row)""",
                "explanation": "The first query combines AND to get only shipped orders over $100. The second uses IN as a shortcut for multiple OR conditions. The third uses LIKE with % wildcards to find products containing the letter 'o'. DISTINCT removes duplicate product names."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "WHERE col = 'value'",
                    "WHERE col > number AND col < number",
                    "WHERE col IN ('a', 'b', 'c')",
                    "WHERE col BETWEEN 10 AND 100",
                    "WHERE col LIKE 'prefix%'",
                    "WHERE col IS NULL / IS NOT NULL"
                ],
                "notes": "String comparisons in SQL use single quotes. Double quotes are for column/table names in some databases. In SQLite, LIKE is case-insensitive by default."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which WHERE clause correctly finds customers NOT from 'Denver' or 'Austin'?",
                    "options": [
                        "A. WHERE city != 'Denver' AND city != 'Austin'",
                        "B. WHERE city NOT IN ('Denver', 'Austin')",
                        "C. WHERE NOT city = 'Denver' OR 'Austin'",
                        "D. Both A and B are correct"
                    ],
                    "answer": 3,
                    "explanation": "Both A (using AND with !=) and B (using NOT IN) correctly exclude both cities. Option C has incorrect syntax — NOT doesn't apply to the second city."
                },
                {
                    "type": "true_false",
                    "question": "WHERE salary = NULL correctly finds employees with no salary on record.",
                    "answer": False,
                    "explanation": "You must use WHERE salary IS NULL. Comparing with = NULL always returns nothing because NULL is 'unknown' — you can't say unknown equals unknown."
                },
                {
                    "type": "fill_blank",
                    "question": "Find all products where the name starts with 'Pro':",
                    "template": "SELECT * FROM products WHERE name LIKE '___';",
                    "answer": "Pro%",
                    "explanation": "The % wildcard matches zero or more characters. 'Pro%' matches 'Pro', 'Product', 'Professional', etc."
                }
            ],
            "challenge": {
                "instructions": "Query a customer database to answer three business questions: (1) Find all customers in 'California' with a lifetime_value over 5000. (2) Find customers whose email ends in '@gmail.com'. (3) Find customers with NULL phone numbers (these need to be contacted to update their records).",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT, email TEXT,
    state TEXT, phone TEXT, lifetime_value REAL
)''')
cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?)', [
    (1, 'Alice Smith',  'alice@gmail.com',   'California', '555-1001', 8500.00),
    (2, 'Bob Jones',    'bob@company.com',   'Texas',      '555-1002', 3200.00),
    (3, 'Carol White',  'carol@gmail.com',   'California', None,       12000.00),
    (4, 'Dave Brown',   'dave@outlook.com',  'California', '555-1004', 4800.00),
    (5, 'Eve Davis',    'eve@gmail.com',     'Florida',    None,       6700.00),
    (6, 'Frank Lee',    'frank@company.com', 'California', '555-1006', 9100.00),
])

# Q1: California customers with lifetime_value > 5000
print('=== High-Value California Customers ===')
# your query here

# Q2: Gmail users
print('\\n=== Gmail Users ===')
# your query here

# Q3: Missing phone numbers
print('\\n=== Missing Phone Numbers ===')
# your query here
""",
                "tests": [
                    {"type": "output_contains", "value": "Alice"},
                    {"type": "code_contains", "value": "IS NULL"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT, email TEXT,
    state TEXT, phone TEXT, lifetime_value REAL
)''')
cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?)', [
    (1, 'Alice Smith',  'alice@gmail.com',   'California', '555-1001', 8500.00),
    (2, 'Bob Jones',    'bob@company.com',   'Texas',      '555-1002', 3200.00),
    (3, 'Carol White',  'carol@gmail.com',   'California', None,       12000.00),
    (4, 'Dave Brown',   'dave@outlook.com',  'California', '555-1004', 4800.00),
    (5, 'Eve Davis',    'eve@gmail.com',     'Florida',    None,       6700.00),
    (6, 'Frank Lee',    'frank@company.com', 'California', '555-1006', 9100.00),
])

print('=== High-Value California Customers ===')
for row in cursor.execute(\'\'\'
    SELECT name, lifetime_value FROM customers
    WHERE state = 'California' AND lifetime_value > 5000
'''):
    print(row)

print('\\n=== Gmail Users ===')
for row in cursor.execute(\'\'\'
    SELECT name, email FROM customers WHERE email LIKE '%@gmail.com'
'''):
    print(row)

print('\\n=== Missing Phone Numbers ===')
for row in cursor.execute(\'\'\'
    SELECT name, email FROM customers WHERE phone IS NULL
'''):
    print(row)
conn.close()"""
            },
            "challenge_variations": [
                "Filter an orders table: find all 'pending' orders placed after '2024-06-01' with amount > 200.",
                "From an employees table, find all engineers (department='Engineering') earning between 80000 and 120000.",
                "Query products: find items with less than 20 in stock that are NOT discontinued.",
                "From a students table, find all students with GPA >= 3.5 whose major LIKE '%Data%'.",
                "Filter transactions: find all debits (type='debit') over $1000 in the last quarter.",
                "Find all flights where origin IN ('JFK', 'LAX', 'ORD') and seats_available > 0.",
                "Query reviews: find all 5-star reviews (rating=5) where the comment is NOT NULL.",
                "From a projects table, find projects that are 'active' and have a budget > 50000.",
                "Filter job postings: find remote jobs (remote=1) where salary_max >= 100000.",
                "Find all shipments that are NOT delivered (delivered=0) and were shipped before today's date."
            ]
        },

        # ── LESSON 5 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l5",
            "title": "Sorting with ORDER BY",
            "order": 5,
            "duration_min": 15,
            "real_world_context": "Reports always need data in a meaningful order — top sales, most recent transactions, alphabetical customer lists. ORDER BY turns raw query results into organized, readable output.",
            "concept": """**ORDER BY** sorts the results of your query. Without it, database results come back in no guaranteed order (usually insertion order, but never rely on that).

```sql
-- Sort ascending (A→Z, lowest→highest) — ASC is the default
SELECT * FROM customers ORDER BY name;
SELECT * FROM customers ORDER BY name ASC;  -- same thing

-- Sort descending (Z→A, highest→lowest)
SELECT * FROM products ORDER BY price DESC;

-- Top-selling products first
SELECT product, total_sales FROM summary ORDER BY total_sales DESC;
```

**Sorting by multiple columns:**
```sql
-- Sort by department first, then by salary within each department
SELECT name, department, salary
FROM employees
ORDER BY department ASC, salary DESC;
-- Result: All Engineering sorted high→low salary, then Marketing high→low, etc.
```

**Sort by column position (less readable but valid):**
```sql
SELECT name, salary FROM employees ORDER BY 2 DESC;
-- ORDER BY 2 means "sort by the 2nd column in the SELECT list" (salary)
```

**NULL handling in ORDER BY:**
```sql
-- In most databases, NULLs sort LAST in ASC, FIRST in DESC
-- SQLite: NULLs are considered smaller than any value
SELECT * FROM employees ORDER BY bonus DESC;
-- Employees with NULL bonus appear at the END in DESC order
```

**Combining ORDER BY with WHERE:**
```sql
SELECT name, salary
FROM employees
WHERE department = 'Sales'
ORDER BY salary DESC;
-- Filter FIRST (WHERE), then sort the filtered results (ORDER BY)
```

The SQL execution order conceptually is: FROM → WHERE → SELECT → ORDER BY. Always apply filters before sorting.""",
            "worked_example": {
                "description": "Let's build a sales leaderboard — sorted by revenue, then alphabetically for ties.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE sales_reps (
    id INTEGER PRIMARY KEY, name TEXT, region TEXT,
    quarterly_revenue REAL, deals_closed INTEGER
)''')
cursor.executemany('INSERT INTO sales_reps VALUES (?,?,?,?,?)', [
    (1, 'Alice',  'West',    125000, 28),
    (2, 'Bob',    'East',     98000, 22),
    (3, 'Carol',  'West',    125000, 31),
    (4, 'Dave',   'Central',  67000, 15),
    (5, 'Eve',    'East',    112000, 25),
    (6, 'Frank',  'Central', 145000, 33),
])

print('=== Sales Leaderboard (Revenue DESC, Name ASC for ties) ===')
for row in cursor.execute('''
    SELECT name, region, quarterly_revenue, deals_closed
    FROM sales_reps
    ORDER BY quarterly_revenue DESC, name ASC
'''):
    print(f"  {row[0]:<8} | {row[2]:>10,.2f} | {row[3]} deals")

print('\\n=== Best Deal Closers in West Region ===')
for row in cursor.execute('''
    SELECT name, deals_closed
    FROM sales_reps
    WHERE region = 'West'
    ORDER BY deals_closed DESC
'''):
    print(f"  {row[0]}: {row[1]} deals")""",
                "explanation": "The leaderboard sorts by revenue descending first. Alice and Carol both have $125,000 — the second sort key (name ASC) breaks the tie alphabetically, putting Alice before Carol. The second query adds WHERE first, then sorts only West region reps."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "ORDER BY col ASC   -- ascending (default)",
                    "ORDER BY col DESC  -- descending",
                    "ORDER BY col1 DESC, col2 ASC  -- multi-column sort",
                    "WHERE ... ORDER BY ...  -- filter then sort"
                ],
                "notes": "ORDER BY always comes after WHERE in a query. The order of clauses matters: SELECT → FROM → WHERE → ORDER BY."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does ORDER BY price DESC, name ASC do?",
                    "options": [
                        "A. Sorts by name first, then by price",
                        "B. Sorts by price highest-to-lowest; ties broken by name A-to-Z",
                        "C. Sorts by price lowest-to-highest",
                        "D. Returns an error because you can't mix DESC and ASC"
                    ],
                    "answer": 1,
                    "explanation": "Multi-column ORDER BY sorts by the first column first. When two rows have the same price, the second column (name ASC) determines their relative order."
                },
                {
                    "type": "true_false",
                    "question": "If you don't include ORDER BY, a SQL query always returns rows in the order they were inserted.",
                    "answer": False,
                    "explanation": "Without ORDER BY, the row order is undefined — databases may return rows in any order depending on internal storage, indexes, or query optimization. Never rely on implicit ordering."
                },
                {
                    "type": "fill_blank",
                    "question": "Sort employees by salary from highest to lowest:",
                    "template": "SELECT * FROM employees ORDER BY salary ___;",
                    "answer": "DESC",
                    "explanation": "DESC (descending) sorts highest to lowest for numbers, Z to A for text. ASC (ascending) is the default."
                }
            ],
            "challenge": {
                "instructions": "You manage a product catalog. Write queries to: (1) List all products sorted by price lowest to highest. (2) List products in the 'Electronics' category sorted by stock DESC (most available first). (3) Create a 'reorder report' — products with stock under 50, sorted by stock ASC (most urgent first), then by name.",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER
)''')
cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', [
    (1,  'Laptop',       'Electronics', 999.00, 45),
    (2,  'Mouse',        'Electronics',  29.00, 200),
    (3,  'Notebook',     'Stationery',    4.99, 500),
    (4,  'USB Hub',      'Electronics',  39.99, 18),
    (5,  'Pen Pack',     'Stationery',    6.49, 800),
    (6,  'Monitor',      'Electronics', 349.00, 30),
    (7,  'Desk Lamp',    'Furniture',    49.99, 65),
    (8,  'Stapler',      'Stationery',   12.99, 12),
    (9,  'Webcam',       'Electronics',  79.99, 8),
    (10, 'Chair Mat',    'Furniture',    39.99, 55),
])

# Query 1: All products by price ASC
print('=== Price List (Low to High) ===')
# your query here

# Query 2: Electronics by stock DESC
print('\\n=== Electronics Availability ===')
# your query here

# Query 3: Reorder report (stock < 50, sort by stock ASC then name ASC)
print('\\n=== Reorder Report ===')
# your query here
""",
                "tests": [
                    {"type": "output_contains", "value": "Reorder"},
                    {"type": "code_contains", "value": "ORDER BY"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER
)''')
cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', [
    (1,  'Laptop',    'Electronics', 999.00, 45),
    (2,  'Mouse',     'Electronics',  29.00, 200),
    (3,  'Notebook',  'Stationery',    4.99, 500),
    (4,  'USB Hub',   'Electronics',  39.99, 18),
    (5,  'Pen Pack',  'Stationery',    6.49, 800),
    (6,  'Monitor',   'Electronics', 349.00, 30),
    (7,  'Desk Lamp', 'Furniture',    49.99, 65),
    (8,  'Stapler',   'Stationery',   12.99, 12),
    (9,  'Webcam',    'Electronics',  79.99, 8),
    (10, 'Chair Mat', 'Furniture',    39.99, 55),
])

print('=== Price List (Low to High) ===')
for row in cursor.execute('SELECT name, price FROM products ORDER BY price ASC'):
    print(f"  {row[0]:<15} ${row[1]:>7.2f}")

print('\\n=== Electronics Availability ===')
for row in cursor.execute(\'\'\'
    SELECT name, stock FROM products
    WHERE category = 'Electronics'
    ORDER BY stock DESC
'''):
    print(f"  {row[0]:<15} stock: {row[1]}")

print('\\n=== Reorder Report ===')
for row in cursor.execute(\'\'\'
    SELECT name, category, stock FROM products
    WHERE stock < 50
    ORDER BY stock ASC, name ASC
'''):
    print(f"  {row[0]:<15} [{row[1]}] stock: {row[2]}")
conn.close()"""
            },
            "challenge_variations": [
                "Sort a 'movies' table by release_year DESC, then title ASC to get a reverse-chronological film list.",
                "From an 'employees' table, sort by department ASC then salary DESC to see top earners per department.",
                "Create a customer loyalty report: sort by lifetime_value DESC, show only top spenders.",
                "Sort 'flights' by departure_time ASC and filter to only show flights with available_seats > 0.",
                "Order 'job_postings' by salary_max DESC to find the highest-paying jobs first.",
                "Sort 'students' by GPA DESC, then last_name ASC for an academic honor roll.",
                "From 'transactions', sort by amount DESC to find the largest transactions.",
                "Sort 'recipes' by prep_time_mins ASC to find the quickest meals.",
                "Order 'projects' by deadline ASC (most urgent first) filtering to only active projects.",
                "Sort 'sensors' by reading_value DESC and location ASC for a monitoring dashboard."
            ]
        },

        # ── LESSON 6 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l6",
            "title": "Limiting Results — TOP / LIMIT",
            "order": 6,
            "duration_min": 12,
            "real_world_context": "You never want to dump a million rows into a report. LIMIT lets you get the top 10 customers, the 5 most recent orders, or page through large datasets efficiently.",
            "concept": """**LIMIT** restricts how many rows the query returns. Combined with ORDER BY, it's how you get "top N" results.

```sql
-- Get only 5 rows
SELECT * FROM orders LIMIT 5;

-- Top 10 highest-value orders
SELECT customer, amount FROM orders
ORDER BY amount DESC
LIMIT 10;

-- Most recent 5 orders
SELECT * FROM orders
ORDER BY order_date DESC
LIMIT 5;
```

**Note on database dialects:**
- **SQLite / MySQL / PostgreSQL**: use `LIMIT n`
- **SQL Server / MS Access**: use `TOP n` → `SELECT TOP 10 * FROM orders`
- **Oracle**: use `ROWNUM` or `FETCH FIRST n ROWS ONLY`

In this course we use SQLite, so always use `LIMIT`.

**OFFSET — skip rows (pagination):**
```sql
-- Skip the first 10 rows, return the next 10 (page 2)
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 10;

-- Page 3 (rows 21-30)
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 20;
```

This is how apps paginate data — "Show 20 results per page."

**LIMIT with subqueries — a preview:**
```sql
-- Find the 3 cheapest products in Electronics
SELECT * FROM products
WHERE category = 'Electronics'
ORDER BY price ASC
LIMIT 3;
```

**Business use cases:**
- Top 10 customers by revenue (customer ranking reports)
- 5 most recent support tickets (dashboard widgets)
- Bottom 20% performers (ORDER BY metric ASC LIMIT ...)
- Sample 100 rows for data exploration before running a heavy query""",
            "worked_example": {
                "description": "Build a sales dashboard excerpt — top 5 customers, most recent 3 orders, bottom 3 products by stock.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT, total_spent REAL, last_order TEXT
)''')
cursor.executemany('INSERT INTO customers VALUES (?,?,?,?)', [
    (1,'Alice',  45000,'2024-03-10'),
    (2,'Bob',    12000,'2024-01-05'),
    (3,'Carol',  78000,'2024-03-12'),
    (4,'Dave',    8500,'2023-12-20'),
    (5,'Eve',    62000,'2024-03-08'),
    (6,'Frank',  33000,'2024-02-14'),
    (7,'Grace',  91000,'2024-03-15'),
    (8,'Henry',  15000,'2024-01-22'),
])

# Top 5 customers by spending
print('=== Top 5 Customers ===')
for row in cursor.execute('''
    SELECT name, total_spent FROM customers
    ORDER BY total_spent DESC LIMIT 5
'''):
    print(f"  {row[0]:<8} ${row[1]:>8,.2f}")

# 3 most recently active
print('\\n=== 3 Most Recent Orders ===')
for row in cursor.execute('''
    SELECT name, last_order FROM customers
    ORDER BY last_order DESC LIMIT 3
'''):
    print(f"  {row[0]}: {row[1]}")

# Page 2 (rows 3-4 using OFFSET)
print('\\n=== Customers ranked 3-4 (OFFSET demo) ===')
for row in cursor.execute('''
    SELECT name, total_spent FROM customers
    ORDER BY total_spent DESC LIMIT 2 OFFSET 2
'''):
    print(f"  {row[0]}: ${row[1]:,.2f}")""",
                "explanation": "The first query ranks all 8 customers by spending but only returns the top 5. The second query sorts by most recent order date and limits to 3. The OFFSET demo skips the top 2 and returns ranks 3 and 4 — useful for pagination."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "SELECT * FROM table LIMIT n;",
                    "ORDER BY col DESC LIMIT n;   -- top N",
                    "LIMIT n OFFSET m;            -- skip m rows, return n",
                    "SELECT TOP n * FROM table;   -- SQL Server syntax"
                ],
                "notes": "Always use ORDER BY with LIMIT. Without ORDER BY, LIMIT returns an arbitrary set of rows — not necessarily the 'top' anything."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does LIMIT 10 OFFSET 20 return?",
                    "options": [
                        "A. The first 20 rows",
                        "B. Rows 10 through 20",
                        "C. 10 rows starting from row 21 (skipping the first 20)",
                        "D. The last 10 rows"
                    ],
                    "answer": 2,
                    "explanation": "OFFSET 20 skips the first 20 rows. LIMIT 10 then returns the next 10 rows (rows 21-30). This is standard pagination logic."
                },
                {
                    "type": "true_false",
                    "question": "Using LIMIT without ORDER BY reliably returns the 'top' rows based on insertion order.",
                    "answer": False,
                    "explanation": "Without ORDER BY, the database can return rows in any order. LIMIT without ORDER BY gives an arbitrary subset, not a meaningful 'top N'. Always pair them."
                },
                {
                    "type": "fill_blank",
                    "question": "Get the 3 most expensive products:",
                    "template": "SELECT * FROM products ORDER BY price DESC ___ 3;",
                    "answer": "LIMIT",
                    "explanation": "LIMIT placed after ORDER BY restricts the result to the specified number of rows from the sorted results."
                }
            ],
            "challenge": {
                "instructions": "Using the employees table provided, write three queries: (1) The top 3 highest-paid employees. (2) The 2 employees who have been with the company longest (earliest hire_date). (3) Employees ranked 4th and 5th by salary (use OFFSET to skip the top 3).",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE employees (
    id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL, hire_date TEXT
)''')
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?)', [
    (1, 'Alice',   'Engineering', 115000, '2018-03-15'),
    (2, 'Bob',     'Marketing',    72000, '2021-07-01'),
    (3, 'Carol',   'Engineering',  98000, '2019-11-20'),
    (4, 'Dave',    'Sales',        85000, '2017-05-10'),
    (5, 'Eve',     'Engineering', 125000, '2020-02-28'),
    (6, 'Frank',   'Marketing',    68000, '2022-09-01'),
    (7, 'Grace',   'Sales',        91000, '2016-08-14'),
])

# Top 3 highest-paid
print('=== Top 3 Salaries ===')
# your query here

# 2 longest-tenured employees
print('\\n=== Longest Tenure ===')
# your query here

# Rank 4 and 5 by salary (OFFSET)
print('\\n=== Salary Rank 4-5 ===')
# your query here
""",
                "tests": [
                    {"type": "output_contains", "value": "Eve"},
                    {"type": "code_contains", "value": "OFFSET"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE employees (
    id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL, hire_date TEXT
)''')
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?)', [
    (1, 'Alice',   'Engineering', 115000, '2018-03-15'),
    (2, 'Bob',     'Marketing',    72000, '2021-07-01'),
    (3, 'Carol',   'Engineering',  98000, '2019-11-20'),
    (4, 'Dave',    'Sales',        85000, '2017-05-10'),
    (5, 'Eve',     'Engineering', 125000, '2020-02-28'),
    (6, 'Frank',   'Marketing',    68000, '2022-09-01'),
    (7, 'Grace',   'Sales',        91000, '2016-08-14'),
])

print('=== Top 3 Salaries ===')
for row in cursor.execute('SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3'):
    print(f"  {row[0]}: ${row[1]:,.0f}")

print('\\n=== Longest Tenure ===')
for row in cursor.execute('SELECT name, hire_date FROM employees ORDER BY hire_date ASC LIMIT 2'):
    print(f"  {row[0]}: hired {row[1]}")

print('\\n=== Salary Rank 4-5 ===')
for row in cursor.execute('SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 2 OFFSET 3'):
    print(f"  {row[0]}: ${row[1]:,.0f}")
conn.close()"""
            },
            "challenge_variations": [
                "Find the top 5 products by revenue, the 3 lowest-stock items, and the 10 most recent transactions.",
                "Get the top 3 sales regions, the bottom 3, and show page 2 (rows 4-6) of the full ranking.",
                "Find the 5 most recent customer signups, the 5 oldest accounts, and customers ranked 6-10 by lifetime value.",
                "Show the 3 most expensive flights on a given route and the 3 cheapest available seats.",
                "Find top 10 recipes by rating, skip the top 3 and show ranks 4-10 using OFFSET.",
                "Get the 3 largest pending orders, the 5 smallest completed orders, and the most recent 10 orders.",
                "List the top 5 students by GPA per department using LIMIT in a filtered query.",
                "Find the 3 projects closest to deadline, the 3 furthest, and projects ranked 4-6.",
                "Show the 5 highest-salary job postings and the 5 lowest, with OFFSET for pagination.",
                "Get the 3 busiest warehouses by inventory count and the 2 most underutilized."
            ]
        },

        # ── LESSON 7 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l7",
            "title": "Aggregation — COUNT, SUM, AVG, MAX, MIN",
            "order": 7,
            "duration_min": 20,
            "real_world_context": "Business questions are almost always about summaries: How many customers do we have? What's total revenue this month? What's the average order size? These are aggregate queries.",
            "concept": """**Aggregate functions** collapse many rows into a single summary value. They're the foundation of every business report.

**The five core aggregates:**
```sql
COUNT(*) -- count rows
COUNT(col) -- count non-NULL values in a column
SUM(col)   -- add up all values
AVG(col)   -- arithmetic mean
MAX(col)   -- largest value
MIN(col)   -- smallest value
```

**Examples:**
```sql
SELECT COUNT(*) FROM customers;
-- Returns: 10000  (total rows in customers table)

SELECT COUNT(phone) FROM customers;
-- Returns: 8432  (only rows where phone is NOT NULL)
-- COUNT(col) skips NULLs; COUNT(*) counts everything

SELECT SUM(amount) FROM orders WHERE status = 'completed';
-- Returns: 1250000.00  (total revenue from completed orders)

SELECT AVG(salary) FROM employees WHERE department = 'Engineering';
-- Returns: 105000.00  (average engineering salary)

SELECT MAX(order_date) FROM orders;
-- Returns: '2024-03-15'  (most recent order date)

SELECT MIN(price), MAX(price) FROM products;
-- Returns one row: (4.99, 999.00)
```

**Multiple aggregates in one query:**
```sql
SELECT
    COUNT(*)        AS total_orders,
    SUM(amount)     AS total_revenue,
    AVG(amount)     AS avg_order_value,
    MAX(amount)     AS largest_order,
    MIN(amount)     AS smallest_order
FROM orders
WHERE status = 'completed';
```

**NULL behavior in aggregates — important!**
```sql
-- Table: bonuses — values: 500, 1000, NULL, NULL, 2000
SELECT AVG(bonus) FROM employees;
-- Returns: 1166.67 (averages only the 3 non-NULL values: 3500/3)
-- NULL values are IGNORED by SUM, AVG, MAX, MIN, COUNT(col)
-- This can make your averages misleading if NULLs represent zero!
```

**COUNT DISTINCT — count unique values:**
```sql
SELECT COUNT(DISTINCT city) FROM customers;
-- How many different cities do our customers come from?
```""",
            "worked_example": {
                "description": "Build a complete sales summary report using all five aggregate functions.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE orders (
    id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL,
    status TEXT, region TEXT, order_date TEXT, rep_bonus REAL
)''')
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?,?)', [
    (1,  101, 250.00, 'completed', 'West',    '2024-01-10', 25.00),
    (2,  102, 875.50, 'completed', 'East',    '2024-01-15', 87.55),
    (3,  103,  49.99, 'cancelled', 'West',    '2024-01-20', None),
    (4,  101, 1200.00,'completed', 'West',    '2024-02-01', 120.00),
    (5,  104, 333.00, 'completed', 'Central', '2024-02-10', 33.30),
    (6,  105, 780.00, 'pending',   'East',    '2024-02-15', None),
    (7,  102, 95.00,  'completed', 'East',    '2024-03-01', 9.50),
    (8,  106, 2100.00,'completed', 'West',    '2024-03-10', 210.00),
])

print('=== Sales Summary Report ===')
row = cursor.execute('''
    SELECT
        COUNT(*)         AS total_orders,
        COUNT(rep_bonus) AS orders_with_bonus,
        SUM(amount)      AS total_revenue,
        ROUND(AVG(amount), 2) AS avg_order,
        MAX(amount)      AS largest_order,
        MIN(amount)      AS smallest_order
    FROM orders
    WHERE status = 'completed'
''').fetchone()

print(f"  Total orders:      {row[0]}")
print(f"  With bonus:        {row[1]}")
print(f"  Total revenue:     ${row[2]:,.2f}")
print(f"  Avg order value:   ${row[3]:,.2f}")
print(f"  Largest order:     ${row[4]:,.2f}")
print(f"  Smallest order:    ${row[5]:,.2f}")

print('\\n=== Unique Customers and Regions ===')
row = cursor.execute('''
    SELECT COUNT(DISTINCT customer_id) AS unique_customers,
           COUNT(DISTINCT region) AS unique_regions
    FROM orders WHERE status = 'completed'
''').fetchone()
print(f"  Unique customers: {row[0]}, Unique regions: {row[1]}")""",
                "explanation": "COUNT(*) counts all rows including cancelled orders; COUNT(rep_bonus) counts only rows where bonus is not NULL. Notice AVG and SUM ignore the NULL bonus values automatically. ROUND(AVG(amount), 2) rounds to 2 decimal places."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "COUNT(*) -- all rows",
                    "COUNT(col) -- non-NULL values only",
                    "COUNT(DISTINCT col) -- unique values",
                    "SUM(col) AVG(col) MAX(col) MIN(col)",
                    "ROUND(value, decimal_places)",
                    "All aggregates ignore NULL except COUNT(*)"
                ],
                "notes": "AVG(col) divides by the count of non-NULL rows. If NULLs represent 'zero' in your data, use AVG(COALESCE(col, 0)) to include them."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "A column has values: 10, 20, NULL, 30, NULL. What does AVG(column) return?",
                    "options": ["A. 12 (60/5, treating NULL as 0)", "B. 20 (60/3, ignoring NULLs)", "C. NULL", "D. 60"],
                    "answer": 1,
                    "explanation": "AVG ignores NULL values. It adds 10+20+30=60 and divides by 3 (non-NULL count), giving 20. This is why it's important to understand your NULL values — they can skew averages."
                },
                {
                    "type": "true_false",
                    "question": "COUNT(*) and COUNT(column_name) always return the same number.",
                    "answer": False,
                    "explanation": "COUNT(*) counts all rows regardless of NULL. COUNT(column_name) counts only rows where that specific column is NOT NULL. They differ when the column contains NULL values."
                },
                {
                    "type": "fill_blank",
                    "question": "Count how many distinct products have been ordered:",
                    "template": "SELECT COUNT(___ product_id) FROM orders;",
                    "answer": "DISTINCT",
                    "explanation": "COUNT(DISTINCT col) counts unique values, not total rows. If product 5 appears in 100 orders, it still counts as 1 distinct product."
                }
            ],
            "challenge": {
                "instructions": "You're a data analyst at a retail company. Using the sales table provided, write a single query that calculates: total number of transactions, number of completed transactions, total revenue from completed transactions, average transaction amount (completed only), the single largest completed transaction, and the number of distinct customers who made completed purchases. Print each metric labeled clearly.",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE sales (
    id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT,
    amount REAL, status TEXT, sale_date TEXT
)''')
cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?,?)', [
    (1,  1, 'Laptop',   999.00, 'completed', '2024-01-05'),
    (2,  2, 'Mouse',     29.00, 'completed', '2024-01-06'),
    (3,  3, 'Keyboard',  79.00, 'refunded',  '2024-01-07'),
    (4,  1, 'Monitor',  349.00, 'completed', '2024-01-10'),
    (5,  4, 'USB Hub',   39.99, 'completed', '2024-01-12'),
    (6,  5, 'Laptop',   999.00, 'pending',   '2024-01-14'),
    (7,  2, 'Webcam',    79.99, 'completed', '2024-01-15'),
    (8,  3, 'Mouse',     29.00, 'completed', '2024-01-16'),
    (9,  6, 'Monitor',  349.00, 'completed', '2024-01-18'),
    (10, 4, 'Keyboard',  79.00, 'refunded',  '2024-01-20'),
])

# Write a query that returns all six metrics
result = cursor.execute('''
    SELECT
        -- your aggregates here
    FROM sales
    -- add WHERE for completed only where needed
''').fetchone()

# Print results
print('Total transactions:  ', )
print('Completed:           ', )
print('Total revenue:      $', )
print('Avg transaction:    $', )
print('Largest transaction:$', )
print('Unique customers:    ', )
""",
                "tests": [
                    {"type": "code_contains", "value": "COUNT"},
                    {"type": "code_contains", "value": "SUM"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE sales (
    id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT,
    amount REAL, status TEXT, sale_date TEXT
)''')
cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?,?)', [
    (1,  1, 'Laptop',   999.00, 'completed', '2024-01-05'),
    (2,  2, 'Mouse',     29.00, 'completed', '2024-01-06'),
    (3,  3, 'Keyboard',  79.00, 'refunded',  '2024-01-07'),
    (4,  1, 'Monitor',  349.00, 'completed', '2024-01-10'),
    (5,  4, 'USB Hub',   39.99, 'completed', '2024-01-12'),
    (6,  5, 'Laptop',   999.00, 'pending',   '2024-01-14'),
    (7,  2, 'Webcam',    79.99, 'completed', '2024-01-15'),
    (8,  3, 'Mouse',     29.00, 'completed', '2024-01-16'),
    (9,  6, 'Monitor',  349.00, 'completed', '2024-01-18'),
    (10, 4, 'Keyboard',  79.00, 'refunded',  '2024-01-20'),
])

total_row = cursor.execute('SELECT COUNT(*) FROM sales').fetchone()
result = cursor.execute('''
    SELECT
        COUNT(*)                  AS completed_count,
        SUM(amount)               AS total_revenue,
        ROUND(AVG(amount), 2)     AS avg_transaction,
        MAX(amount)               AS largest,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM sales WHERE status = 'completed'
''').fetchone()

print('Total transactions:  ', total_row[0])
print('Completed:           ', result[0])
print('Total revenue:      $', f"{result[1]:,.2f}")
print('Avg transaction:    $', f"{result[2]:,.2f}")
print('Largest transaction:$', f"{result[3]:,.2f}")
print('Unique customers:    ', result[4])
conn.close()"""
            },
            "challenge_variations": [
                "Calculate average, min, and max employee salary per company (all in one query, no GROUP BY yet).",
                "Find total inventory value (SUM of price * stock), count of products, and most expensive product.",
                "Calculate total flight revenue, average ticket price, and count of distinct routes.",
                "Find count, average GPA, highest GPA, and lowest GPA across all students.",
                "Count total reviews, average star rating, and count of 5-star reviews for a restaurant.",
                "Calculate total project budget, average budget, and count of active vs inactive projects.",
                "Find total loan amount, count of open loans, and largest single loan in a bank database.",
                "Count orders by status using conditional COUNTs: COUNT(CASE WHEN status='shipped' THEN 1 END).",
                "Find the date range of orders: MIN(order_date) and MAX(order_date) plus total count.",
                "Calculate total payroll (SUM salary), headcount, and average salary for a department."
            ]
        },

        # ── LESSON 8 ──────────────────────────────────────────────────────────
        {
            "id": "m3-l8",
            "title": "Grouping Data with GROUP BY",
            "order": 8,
            "duration_min": 20,
            "real_world_context": "The real power of SQL is segmented analysis — not just total revenue, but revenue BY region, BY product category, BY month. GROUP BY is how every business pivot table gets built.",
            "concept": """**GROUP BY** divides rows into groups and applies aggregate functions to each group separately.

```sql
-- Without GROUP BY: one total for all orders
SELECT SUM(amount) FROM orders;
-- Returns: 15250.00

-- With GROUP BY: one total per region
SELECT region, SUM(amount) AS revenue
FROM orders
GROUP BY region;
-- Returns:
-- West     | 8500.00
-- East     | 4250.00
-- Central  | 2500.00
```

**How GROUP BY works conceptually:**
1. SQL takes all rows from the table
2. Groups them into buckets based on the GROUP BY column(s)
3. Applies the aggregate function to each bucket
4. Returns one row per bucket

```sql
-- Group by multiple columns
SELECT region, status, COUNT(*) AS order_count, SUM(amount) AS revenue
FROM orders
GROUP BY region, status;
-- One row per unique (region, status) combination
```

**Every non-aggregate column in SELECT must appear in GROUP BY:**
```sql
-- WRONG: name is not in GROUP BY and not aggregated
SELECT name, department, SUM(salary)
FROM employees
GROUP BY department;  -- ERROR in strict mode

-- CORRECT
SELECT department, SUM(salary) AS total_payroll, COUNT(*) AS headcount
FROM employees
GROUP BY department;
```

**GROUP BY with ORDER BY — sort your summaries:**
```sql
SELECT category, SUM(revenue) AS total
FROM products
GROUP BY category
ORDER BY total DESC;  -- Show highest revenue category first
```

**GROUP BY with WHERE — filter before grouping:**
```sql
-- Only analyze completed orders, then group by region
SELECT region, COUNT(*) AS completed_orders, SUM(amount) AS revenue
FROM orders
WHERE status = 'completed'   -- filters rows BEFORE grouping
GROUP BY region
ORDER BY revenue DESC;
```""",
            "worked_example": {
                "description": "Build a regional sales report and a product category analysis using GROUP BY.",
                "code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE orders (
    id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT,
    category TEXT, amount REAL, status TEXT, region TEXT
)''')
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?,?)', [
    (1,  1, 'Laptop',   'Electronics', 999.00, 'completed', 'West'),
    (2,  2, 'Mouse',    'Electronics',  29.00, 'completed', 'East'),
    (3,  3, 'Notebook', 'Stationery',    9.99, 'completed', 'West'),
    (4,  1, 'Monitor',  'Electronics', 349.00, 'completed', 'West'),
    (5,  4, 'USB Hub',  'Electronics',  39.99, 'cancelled', 'Central'),
    (6,  5, 'Laptop',   'Electronics', 999.00, 'completed', 'East'),
    (7,  2, 'Pen Pack', 'Stationery',    6.49, 'completed', 'East'),
    (8,  3, 'Monitor',  'Electronics', 349.00, 'completed', 'Central'),
    (9,  6, 'Notebook', 'Stationery',    9.99, 'completed', 'Central'),
    (10, 7, 'Keyboard', 'Electronics',  79.00, 'completed', 'West'),
])

print('=== Revenue by Region (completed orders only) ===')
for row in cursor.execute('''
    SELECT region,
           COUNT(*)      AS orders,
           SUM(amount)   AS revenue,
           ROUND(AVG(amount), 2) AS avg_order
    FROM orders
    WHERE status = 'completed'
    GROUP BY region
    ORDER BY revenue DESC
'''):
    print(f"  {row[0]:<10} {row[1]} orders | ${row[2]:>8,.2f} revenue | ${row[3]:>7.2f} avg")

print('\\n=== Revenue by Category ===')
for row in cursor.execute('''
    SELECT category, COUNT(*) AS products_sold, SUM(amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY category
    ORDER BY revenue DESC
'''):
    print(f"  {row[0]:<15} {row[1]} sold | ${row[2]:,.2f}")""",
                "explanation": "The first query groups only completed orders by region. WHERE filters first, then GROUP BY creates three buckets (West, East, Central). The second query shows category-level analysis. Notice that 'cancelled' orders in Central don't affect the revenue figures because WHERE status='completed' removes them before grouping."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "SELECT col, AGG(col) FROM table GROUP BY col;",
                    "GROUP BY col1, col2  -- multi-column grouping",
                    "WHERE ... GROUP BY ... ORDER BY ...  -- clause order",
                    "Every SELECT column must be in GROUP BY or be aggregated"
                ],
                "notes": "SQLite is more permissive than other databases about non-aggregated columns in SELECT. Always follow the rule (include all non-aggregate columns in GROUP BY) to write portable SQL."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "You write: SELECT department, name, COUNT(*) FROM employees GROUP BY department. What's the issue?",
                    "options": [
                        "A. COUNT(*) is wrong — should be COUNT(name)",
                        "B. 'name' is in SELECT but not in GROUP BY and not aggregated",
                        "C. You can't GROUP BY department if it's also in SELECT",
                        "D. Nothing is wrong with this query"
                    ],
                    "answer": 1,
                    "explanation": "In strict SQL, every column in SELECT must either be in GROUP BY or wrapped in an aggregate function. 'name' is neither — this would cause an error in PostgreSQL or SQL Server (SQLite is lenient but returns unpredictable values)."
                },
                {
                    "type": "true_false",
                    "question": "WHERE and HAVING both filter rows, so they can be used interchangeably.",
                    "answer": False,
                    "explanation": "WHERE filters rows BEFORE grouping (operates on individual rows). HAVING filters groups AFTER GROUP BY (operates on aggregated results). You'll learn HAVING in the next lesson."
                },
                {
                    "type": "fill_blank",
                    "question": "Count orders per customer: SELECT customer_id, COUNT(*) FROM orders ___ customer_id;",
                    "template": "SELECT customer_id, COUNT(*) FROM orders ___ customer_id;",
                    "answer": "GROUP BY",
                    "explanation": "GROUP BY customer_id creates one bucket per customer. COUNT(*) then counts orders within each bucket."
                }
            ],
            "challenge": {
                "instructions": "You're analyzing a company's HR data. Write three GROUP BY queries: (1) Count employees and calculate average salary per department. (2) For each department, find the min and max salary. (3) Count how many employees were hired each year (use substr(hire_date, 1, 4) to extract the year). Sort all results meaningfully.",
                "starter_code": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE employees (
    id INTEGER PRIMARY KEY, name TEXT, department TEXT,
    salary REAL, hire_date TEXT
)''')
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?)', [
    (1,  'Alice',   'Engineering', 115000, '2018-03-15'),
    (2,  'Bob',     'Marketing',    72000, '2021-07-01'),
    (3,  'Carol',   'Engineering',  98000, '2019-11-20'),
    (4,  'Dave',    'Sales',        85000, '2017-05-10'),
    (5,  'Eve',     'Engineering', 125000, '2020-02-28'),
    (6,  'Frank',   'Marketing',    68000, '2022-09-01'),
    (7,  'Grace',   'Sales',        91000, '2016-08-14'),
    (8,  'Henry',   'Engineering',  88000, '2021-01-15'),
    (9,  'Iris',    'Marketing',    75000, '2019-06-30'),
    (10, 'Jack',    'Sales',        79000, '2023-03-20'),
])

# Q1: Employee count and avg salary per department
print('=== Department Summary ===')
# your query here

# Q2: Salary range per department
print('\\n=== Salary Ranges ===')
# your query here

# Q3: Hiring by year
print('\\n=== Hires by Year ===')
# your query here
""",
                "tests": [
                    {"type": "output_contains", "value": "Engineering"},
                    {"type": "code_contains", "value": "GROUP BY"}
                ],
                "solution": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE employees (
    id INTEGER PRIMARY KEY, name TEXT, department TEXT,
    salary REAL, hire_date TEXT
)''')
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?)', [
    (1,  'Alice',   'Engineering', 115000, '2018-03-15'),
    (2,  'Bob',     'Marketing',    72000, '2021-07-01'),
    (3,  'Carol',   'Engineering',  98000, '2019-11-20'),
    (4,  'Dave',    'Sales',        85000, '2017-05-10'),
    (5,  'Eve',     'Engineering', 125000, '2020-02-28'),
    (6,  'Frank',   'Marketing',    68000, '2022-09-01'),
    (7,  'Grace',   'Sales',        91000, '2016-08-14'),
    (8,  'Henry',   'Engineering',  88000, '2021-01-15'),
    (9,  'Iris',    'Marketing',    75000, '2019-06-30'),
    (10, 'Jack',    'Sales',        79000, '2023-03-20'),
])

print('=== Department Summary ===')
for row in cursor.execute('''
    SELECT department, COUNT(*) AS headcount, ROUND(AVG(salary),0) AS avg_salary
    FROM employees GROUP BY department ORDER BY avg_salary DESC
'''):
    print(f"  {row[0]:<15} {row[1]} employees | avg ${row[2]:,.0f}")

print('\\n=== Salary Ranges ===')
for row in cursor.execute('''
    SELECT department, MIN(salary) AS min_sal, MAX(salary) AS max_sal
    FROM employees GROUP BY department ORDER BY department
'''):
    print(f"  {row[0]:<15} ${row[1]:,.0f} - ${row[2]:,.0f}")

print('\\n=== Hires by Year ===')
for row in cursor.execute('''
    SELECT substr(hire_date,1,4) AS year, COUNT(*) AS hires
    FROM employees GROUP BY year ORDER BY year
'''):
    print(f"  {row[0]}: {row[1]} new hire(s)")
conn.close()"""
            },
            "challenge_variations": [
                "Group sales by product category: count transactions, total revenue, average price per category.",
                "Analyze orders by status (completed/pending/cancelled): count and total amount per status.",
                "Group customers by state: count customers and average lifetime value per state.",
                "Analyze website traffic by day of week: count visits per day using substr(visit_date, 1, 10).",
                "Group student grades by letter grade (A/B/C/D/F): count students per grade band.",
                "Analyze inventory by category: count products, total stock units, average price per category.",
                "Group transactions by month: extract month from date, sum amounts, count transactions.",
                "Analyze flight data by origin airport: count departures and average delay per airport.",
                "Group job postings by industry: count postings and average salary range per industry.",
                "Analyze sensor readings by location: avg, min, max reading per sensor location."
            ]
        },
        {
            "id": "m3-l9",
            "title": "HAVING — Filtering Your Groups",
            "subtitle": "WHERE can't touch aggregates — HAVING can",
            "difficulty": "intermediate",
            "business_context": "Your manager asks: 'Which departments spend over $500k on salaries?' You have GROUP BY to sum salaries by department, but now you need to filter those group totals — that's HAVING's job.",
            "concept": {
                "theory": "HAVING filters rows AFTER grouping, while WHERE filters rows BEFORE grouping. This means HAVING can reference aggregate functions like SUM(), AVG(), COUNT() — WHERE cannot. The order is: WHERE (filter rows) → GROUP BY (form groups) → HAVING (filter groups).",
                "business_angle": "HAVING is how you answer 'which groups meet a threshold' questions: which products sold more than 100 units, which customers spent over $1000, which sales reps closed more than 5 deals.",
                "worked_example_intro": "We'll find departments with an average salary above $85,000 and more than 2 employees.",
                "key_insight": "If your condition uses an aggregate function (COUNT, SUM, AVG, MIN, MAX), use HAVING. If it references a raw column value, use WHERE. You can use both in the same query."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE employees (
    id INTEGER, name TEXT, dept TEXT, salary REAL)''')
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?)', [
    (1,'Alice','Engineering',115000),(2,'Bob','Marketing',72000),
    (3,'Carol','Engineering',98000),(4,'Dave','Sales',85000),
    (5,'Eve','Engineering',125000),(6,'Frank','Marketing',68000),
    (7,'Grace','Sales',91000),(8,'Henry','Engineering',88000),
])

print('=== Departments with avg salary > $85k AND 2+ employees ===')
for row in cursor.execute('''
    SELECT dept, COUNT(*) AS headcount, ROUND(AVG(salary),0) AS avg_sal
    FROM employees
    GROUP BY dept
    HAVING AVG(salary) > 85000 AND COUNT(*) >= 2
    ORDER BY avg_sal DESC
'''):
    print(f"  {row[0]:<15} {row[1]} employees | avg ${row[2]:,.0f}")

# WHERE filters rows first, HAVING filters groups after
print('\\n=== WHERE + HAVING together ===')
for row in cursor.execute('''
    SELECT dept, COUNT(*) AS cnt, ROUND(AVG(salary),0) AS avg_sal
    FROM employees
    WHERE salary > 70000          -- exclude anyone under $70k first
    GROUP BY dept
    HAVING COUNT(*) >= 2          -- then keep only groups with 2+ members
    ORDER BY avg_sal DESC
'''):
    print(f"  {row[0]:<15} {row[1]} people | avg ${row[2]:,.0f}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "GROUP BY col HAVING aggregate_condition",
                        "HAVING COUNT(*) > 5",
                        "HAVING AVG(salary) >= 90000",
                        "WHERE raw_col = val ... HAVING COUNT(*) > 1"
                    ],
                    "notes": "HAVING comes AFTER GROUP BY. WHERE comes BEFORE GROUP BY. Both can appear in the same query."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "Which query correctly finds product categories where total revenue exceeds $10,000?",
                        "options": [
                            "SELECT category FROM sales WHERE SUM(revenue) > 10000",
                            "SELECT category, SUM(revenue) FROM sales GROUP BY category HAVING SUM(revenue) > 10000",
                            "SELECT category, SUM(revenue) FROM sales HAVING SUM(revenue) > 10000",
                            "SELECT category FROM sales GROUP BY category WHERE SUM(revenue) > 10000"
                        ],
                        "answer": 1,
                        "explanation": "HAVING must come after GROUP BY, and you need GROUP BY before you can aggregate. WHERE cannot filter on aggregate results — that's HAVING's job."
                    },
                    {
                        "type": "true_false",
                        "question": "You can use HAVING without GROUP BY.",
                        "answer": True,
                        "explanation": "Technically valid — without GROUP BY, the entire table is treated as one group. But it's rarely useful. Almost always, HAVING accompanies GROUP BY."
                    },
                    {
                        "type": "fill_blank",
                        "question": "Complete the query to find departments with MORE than 3 employees: SELECT dept, COUNT(*) FROM employees GROUP BY dept ___ COUNT(*) > 3",
                        "template": "SELECT dept, COUNT(*) FROM employees GROUP BY dept ___ COUNT(*) > 3",
                        "answer": "HAVING",
                        "explanation": "HAVING filters groups based on aggregate conditions. WHERE can't be used here because COUNT(*) is an aggregate computed after grouping."
                    }
                ]
            },
            "challenge": {
                "instructions": "Analyze a sales dataset. Find: (1) product categories where total units sold > 50, (2) sales reps where average deal size > $5,000 AND total deals >= 3. Print both results with headers.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE sales (
    id INTEGER, rep TEXT, category TEXT, units INTEGER, amount REAL)''')
cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?)', [
    (1,'Ana','Software',30,12000),(2,'Ana','Hardware',25,8000),
    (3,'Ben','Software',15,4500),(4,'Ben','Software',20,6000),
    (5,'Ben','Hardware',10,3000),(6,'Cara','Services',40,15000),
    (7,'Cara','Software',12,5500),(8,'Cara','Services',35,18000),
    (9,'Dan','Hardware',60,22000),(10,'Dan','Hardware',30,9000),
])

# Q1: categories where total units > 50
print('=== High-Volume Categories ===')
# your query here

# Q2: reps with avg deal > $5000 AND 3+ deals
print('\\n=== Top Sales Reps ===')
# your query here
conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "HAVING"},
                    {"type": "output_contains", "value": "Hardware"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE sales (
    id INTEGER, rep TEXT, category TEXT, units INTEGER, amount REAL)''')
cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?)', [
    (1,'Ana','Software',30,12000),(2,'Ana','Hardware',25,8000),
    (3,'Ben','Software',15,4500),(4,'Ben','Software',20,6000),
    (5,'Ben','Hardware',10,3000),(6,'Cara','Services',40,15000),
    (7,'Cara','Software',12,5500),(8,'Cara','Services',35,18000),
    (9,'Dan','Hardware',60,22000),(10,'Dan','Hardware',30,9000),
])
print('=== High-Volume Categories ===')
for r in cursor.execute('''SELECT category, SUM(units) AS total_units FROM sales GROUP BY category HAVING SUM(units) > 50 ORDER BY total_units DESC'''):
    print(f"  {r[0]}: {r[1]} units")
print('\\n=== Top Sales Reps ===')
for r in cursor.execute('''SELECT rep, COUNT(*) AS deals, ROUND(AVG(amount),0) AS avg_deal FROM sales GROUP BY rep HAVING AVG(amount) > 5000 AND COUNT(*) >= 3 ORDER BY avg_deal DESC'''):
    print(f"  {r[0]}: {r[1]} deals | avg ${r[2]:,.0f}")
conn.close()""",
                "challenge_variations": [
                    "Find months where total revenue exceeded $50,000. Group by month extracted from a date column.",
                    "Find customers who placed more than 2 orders AND spent over $500 total. Show customer name, order count, total spend.",
                    "Find zip codes where average house price is above the national average (calculate it as a subquery in HAVING).",
                    "Find product SKUs with a return rate above 10%: HAVING (SUM(returned) * 1.0 / COUNT(*)) > 0.10.",
                    "Find sales regions where both revenue > $100k AND headcount < 5 (use HAVING with two conditions).",
                    "Find marketing campaigns where cost-per-click > $2.50 AND total clicks < 1000.",
                    "Find suppliers where the average delivery delay is more than 3 days.",
                    "Find employee departments where the salary variance (MAX - MIN) is more than $50,000.",
                    "Find stores where inventory turnover (units sold / avg stock) exceeds 2.0.",
                    "Find job titles where more than 30% of employees have been there less than 1 year."
                ]
            }
        },
        {
            "id": "m3-l10",
            "title": "INNER JOIN — Combining Two Tables",
            "subtitle": "Only return rows that match in BOTH tables",
            "difficulty": "intermediate",
            "business_context": "Customer data lives in one table, order data in another. To answer 'what did each customer buy?' you need to combine them — that's a JOIN. INNER JOIN is the most common: it returns only rows with a match on both sides.",
            "concept": {
                "theory": "A JOIN combines rows from two tables based on a matching condition (usually a shared ID). INNER JOIN returns ONLY rows where the condition matches in BOTH tables. If a customer has no orders, they won't appear. If an order has no matching customer, it won't appear either.",
                "business_angle": "Real data is always spread across multiple tables (customers, orders, products, employees). JOINs are how you reassemble that data for analysis. Virtually every real business query uses at least one JOIN.",
                "worked_example_intro": "We'll join a customers table and an orders table to see who bought what.",
                "key_insight": "Think of INNER JOIN as a Venn diagram intersection — only the overlapping records come through. Use table aliases (c, o) to keep queries readable when joining multiple tables."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)')
cursor.execute('CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT, amount REAL)')

cursor.executemany('INSERT INTO customers VALUES (?,?,?)', [
    (1,'Alice','NYC'),(2,'Bob','LA'),(3,'Carol','Chicago'),(4,'Dave','NYC')
])
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', [
    (1,1,'Laptop',1200),(2,1,'Mouse',25),(3,2,'Keyboard',75),
    (4,3,'Monitor',450),(5,3,'Laptop',1200),(6,99,'Headset',80)  # customer 99 doesn't exist!
])

print('=== INNER JOIN: customers with orders ===')
for r in cursor.execute('''
    SELECT c.name, c.city, o.product, o.amount
    FROM customers AS c
    INNER JOIN orders AS o ON c.id = o.customer_id
    ORDER BY c.name, o.amount DESC
'''):
    print(f"  {r[0]:<10} ({r[1]:<8}) | {r[2]:<12} ${r[3]:,.0f}")

# Dave (id=4) had no orders → not in results
# Order for customer_id=99 → not in results (no match)
print('\\n=== Revenue per customer ===')
for r in cursor.execute('''
    SELECT c.name, COUNT(o.id) AS orders, SUM(o.amount) AS total
    FROM customers AS c
    INNER JOIN orders AS o ON c.id = o.customer_id
    GROUP BY c.id, c.name
    ORDER BY total DESC
'''):
    print(f"  {r[0]:<10} {r[1]} orders | ${r[2]:,.0f} total")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "FROM table1 INNER JOIN table2 ON table1.id = table2.foreign_id",
                        "FROM t1 AS a INNER JOIN t2 AS b ON a.id = b.a_id",
                        "SELECT a.col, b.col FROM a JOIN b ON a.id = b.a_id  -- INNER is optional"
                    ],
                    "notes": "INNER JOIN and JOIN mean the same thing. Always specify the ON condition or you get a cartesian product (every row × every row)."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "A customers table has 100 rows. An orders table has 250 rows. After INNER JOIN on customer_id, the result has 230 rows. What does this mean?",
                        "options": [
                            "230 customers placed orders",
                            "20 customers never placed an order",
                            "There are 230 order records that matched a valid customer",
                            "Both B and C are true"
                        ],
                        "answer": 3,
                        "explanation": "230 rows means 230 order records matched a valid customer. Since the orders table has 250 rows, 20 orders had no matching customer (possibly bad data). Some of the 100 customers may also have zero orders."
                    },
                    {
                        "type": "true_false",
                        "question": "INNER JOIN and JOIN produce identical results in SQL.",
                        "answer": True,
                        "explanation": "INNER is the default join type — writing JOIN alone is the same as INNER JOIN. The distinction matters for LEFT JOIN, RIGHT JOIN, and FULL JOIN, which have different behaviors."
                    },
                    {
                        "type": "fill_blank",
                        "question": "Complete the join: SELECT c.name, o.product FROM customers AS c ___ orders AS o ON c.id = o.customer_id",
                        "template": "SELECT c.name, o.product FROM customers AS c ___ orders AS o ON c.id = o.customer_id",
                        "answer": "INNER JOIN",
                        "explanation": "INNER JOIN (or just JOIN) links the two tables on the matching key. The ON clause specifies which columns must be equal."
                    }
                ]
            },
            "challenge": {
                "instructions": "Join a products table and an order_items table. Print: product name, total quantity sold, total revenue. Only include products that have been ordered at least once. Sort by revenue descending.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE products (id INTEGER, name TEXT, price REAL)')
cursor.execute('CREATE TABLE order_items (id INTEGER, product_id INTEGER, qty INTEGER)')
cursor.executemany('INSERT INTO products VALUES (?,?,?)', [
    (1,'Laptop',999),(2,'Mouse',29),(3,'Keyboard',79),(4,'Monitor',399),(5,'Webcam',89)
])
cursor.executemany('INSERT INTO order_items VALUES (?,?,?)', [
    (1,1,3),(2,2,15),(3,3,8),(4,1,2),(5,4,5),(6,2,10),(7,3,4),(8,1,1)
])
# Webcam (id=5) has no orders — should NOT appear in results

print('=== Product Sales Summary ===')
# Write your INNER JOIN query here

conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "JOIN"},
                    {"type": "output_contains", "value": "Laptop"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE products (id INTEGER, name TEXT, price REAL)')
cursor.execute('CREATE TABLE order_items (id INTEGER, product_id INTEGER, qty INTEGER)')
cursor.executemany('INSERT INTO products VALUES (?,?,?)', [(1,'Laptop',999),(2,'Mouse',29),(3,'Keyboard',79),(4,'Monitor',399),(5,'Webcam',89)])
cursor.executemany('INSERT INTO order_items VALUES (?,?,?)', [(1,1,3),(2,2,15),(3,3,8),(4,1,2),(5,4,5),(6,2,10),(7,3,4),(8,1,1)])
print('=== Product Sales Summary ===')
for r in cursor.execute('''
    SELECT p.name, SUM(oi.qty) AS total_qty, SUM(oi.qty * p.price) AS revenue
    FROM products AS p INNER JOIN order_items AS oi ON p.id = oi.product_id
    GROUP BY p.id, p.name ORDER BY revenue DESC
'''):
    print(f"  {r[0]:<12} qty={r[1]:>3} | revenue=${r[2]:,.0f}")
conn.close()""",
                "challenge_variations": [
                    "Join employees and departments tables: show each employee's name, department name, and salary.",
                    "Join students and grades tables: show student name, course name, and grade for all graded students.",
                    "Join flights and airports tables: show flight number, origin city, destination city.",
                    "Join invoices and clients: show client name, invoice date, and invoice total for all paid invoices.",
                    "Join movies and genres via a movie_genres junction table. Show movie title and its genres.",
                    "Join users and login_events: show username and their last login date using MAX(login_date).",
                    "Join suppliers and products: show supplier name and count of products they supply.",
                    "Join transactions and accounts: calculate total deposits and withdrawals per account.",
                    "Join recipes and ingredients via a recipe_ingredients table. Count ingredients per recipe.",
                    "Join employees to their managers (self-join): SELECT e.name AS employee, m.name AS manager FROM employees e JOIN employees m ON e.manager_id = m.id."
                ]
            }
        },
        {
            "id": "m3-l11",
            "title": "LEFT JOIN — Keep Everyone, Even Without a Match",
            "subtitle": "Find the gaps: customers with no orders, products never sold",
            "difficulty": "intermediate",
            "business_context": "Your marketing team asks 'which customers haven't bought anything in 6 months?' An INNER JOIN would hide them — they have no matching orders. LEFT JOIN keeps ALL customers and shows NULL where there's no order data, making the gaps visible.",
            "concept": {
                "theory": "LEFT JOIN returns ALL rows from the left table, plus matching rows from the right table. When there's no match in the right table, those columns are filled with NULL. This is perfect for finding 'missing' relationships — customers without orders, employees without managers, products never purchased.",
                "business_angle": "The most powerful business use of LEFT JOIN is NULL detection: WHERE right_table.id IS NULL. This pattern finds 'orphan' records — things that should have a relationship but don't. It's how you build re-engagement campaigns, find data quality issues, and audit coverage.",
                "worked_example_intro": "We'll find all customers including those with no orders, then specifically filter to just the ones who've never ordered.",
                "key_insight": "LEFT JOIN + WHERE right_table.id IS NULL is the standard pattern for 'find everything in A that has NO match in B'. This is one of the most-used query patterns in business analytics."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE customers (id INTEGER, name TEXT, email TEXT)')
cursor.execute('CREATE TABLE orders (id INTEGER, customer_id INTEGER, amount REAL, date TEXT)')
cursor.executemany('INSERT INTO customers VALUES (?,?,?)', [
    (1,'Alice','alice@co.com'),(2,'Bob','bob@co.com'),
    (3,'Carol','carol@co.com'),(4,'Dave','dave@co.com'),(5,'Eve','eve@co.com')
])
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', [
    (1,1,250,'2024-01-15'),(2,1,180,'2024-03-10'),
    (3,3,420,'2024-02-20'),(4,3,90,'2024-04-01')
])
# Bob, Dave, Eve have NO orders

print('=== All customers + their order count (LEFT JOIN) ===')
for r in cursor.execute('''
    SELECT c.name, COUNT(o.id) AS order_count, COALESCE(SUM(o.amount), 0) AS total_spent
    FROM customers AS c
    LEFT JOIN orders AS o ON c.id = o.customer_id
    GROUP BY c.id, c.name
    ORDER BY total_spent DESC
'''):
    print(f"  {r[0]:<8} | orders: {r[1]} | spent: ${r[2]:,.0f}")

print('\\n=== Customers who have NEVER ordered (NULL pattern) ===')
for r in cursor.execute('''
    SELECT c.name, c.email
    FROM customers AS c
    LEFT JOIN orders AS o ON c.id = o.customer_id
    WHERE o.id IS NULL
'''):
    print(f"  {r[0]} — {r[1]} (send re-engagement email!)")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "FROM left_table LEFT JOIN right_table ON left_table.id = right_table.fk",
                        "WHERE right_table.id IS NULL  -- find unmatched left rows",
                        "COALESCE(possibly_null_col, 0)  -- replace NULL with 0"
                    ],
                    "notes": "RIGHT JOIN is the mirror image (keep all right rows). In practice, most SQL developers use LEFT JOIN and just flip the table order instead of RIGHT JOIN."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "You LEFT JOIN products (left) to order_items (right). A product that was never ordered will appear in results with...",
                        "options": [
                            "It won't appear — LEFT JOIN only shows matched rows",
                            "NULL values in all order_items columns",
                            "Zero values in all order_items columns",
                            "An error because there's no match"
                        ],
                        "answer": 1,
                        "explanation": "LEFT JOIN keeps all left-table rows. For unmatched rows, the right-table columns are filled with NULL, not zero. Use COALESCE(col, 0) if you want to display zero instead of NULL."
                    },
                    {
                        "type": "true_false",
                        "question": "The query 'FROM A LEFT JOIN B ON A.id = B.a_id WHERE B.id IS NULL' finds rows in A that have no matching row in B.",
                        "answer": True,
                        "explanation": "This is the classic anti-join pattern. LEFT JOIN includes all A rows, and filtering WHERE B.id IS NULL keeps only the ones with no B match — exactly the 'orphan' records."
                    },
                    {
                        "type": "fill_blank",
                        "question": "To replace NULL with 0 in LEFT JOIN results, wrap the column: SELECT c.name, ___(SUM(o.amount), 0) FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.name",
                        "template": "SELECT c.name, ___(SUM(o.amount), 0) AS total FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.name",
                        "answer": "COALESCE",
                        "explanation": "COALESCE(value, fallback) returns the first non-NULL argument. COALESCE(SUM(o.amount), 0) returns 0 for customers with no orders instead of NULL."
                    }
                ]
            },
            "challenge": {
                "instructions": "Find: (1) all products with their total units sold (include products with zero sales), (2) specifically list products that have NEVER been sold. Use LEFT JOIN.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT)')
cursor.execute('CREATE TABLE sales (id INTEGER, product_id INTEGER, units INTEGER)')
cursor.executemany('INSERT INTO products VALUES (?,?,?)', [
    (1,'Laptop','Electronics'),(2,'Mouse','Electronics'),(3,'Keyboard','Electronics'),
    (4,'Desk Chair','Furniture'),(5,'Standing Desk','Furniture'),(6,'Whiteboard','Office')
])
cursor.executemany('INSERT INTO sales VALUES (?,?,?)', [
    (1,1,5),(2,2,20),(3,2,15),(4,3,8),(5,1,3)
])
# Desk Chair, Standing Desk, Whiteboard never sold

print('=== All Products — Sales Summary ===')
# LEFT JOIN with COALESCE for 0 sales

print('\\n=== Products Never Sold ===')
# LEFT JOIN + WHERE sales.id IS NULL

conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "LEFT JOIN"},
                    {"type": "output_contains", "value": "Whiteboard"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT)')
cursor.execute('CREATE TABLE sales (id INTEGER, product_id INTEGER, units INTEGER)')
cursor.executemany('INSERT INTO products VALUES (?,?,?)', [(1,'Laptop','Electronics'),(2,'Mouse','Electronics'),(3,'Keyboard','Electronics'),(4,'Desk Chair','Furniture'),(5,'Standing Desk','Furniture'),(6,'Whiteboard','Office')])
cursor.executemany('INSERT INTO sales VALUES (?,?,?)', [(1,1,5),(2,2,20),(3,2,15),(4,3,8),(5,1,3)])
print('=== All Products — Sales Summary ===')
for r in cursor.execute('''SELECT p.name, p.category, COALESCE(SUM(s.units),0) AS units_sold FROM products p LEFT JOIN sales s ON p.id = s.product_id GROUP BY p.id, p.name, p.category ORDER BY units_sold DESC'''):
    print(f"  {r[0]:<16} ({r[1]}) | {r[2]} units")
print('\\n=== Products Never Sold ===')
for r in cursor.execute('''SELECT p.name, p.category FROM products p LEFT JOIN sales s ON p.id = s.product_id WHERE s.id IS NULL'''):
    print(f"  {r[0]} ({r[1]}) — consider discontinuing or promoting")
conn.close()""",
                "challenge_variations": [
                    "Find employees who have never been assigned to any project. Use employees LEFT JOIN project_assignments WHERE assignment IS NULL.",
                    "Find courses with zero student enrollments using LEFT JOIN.",
                    "Find all regions including those with zero sales. Show region name and COALESCE total revenue.",
                    "Find students who haven't submitted any assignments this semester.",
                    "Find vendors who haven't had any purchase orders in the last 90 days.",
                    "Find all marketing campaigns including ones with zero clicks. Show campaign name and click count.",
                    "Find blog authors who haven't published any posts in 2024.",
                    "Use LEFT JOIN to count how many users have completed each onboarding step, including steps with zero completions.",
                    "Find all menu items including those with zero orders last month.",
                    "Find warehouses with no current inventory by LEFT JOINing warehouses to inventory WHERE inventory.id IS NULL."
                ]
            }
        },
        {
            "id": "m3-l12",
            "title": "Multi-Table JOINs & Aliases",
            "subtitle": "Chain multiple joins to answer complex business questions",
            "difficulty": "intermediate",
            "business_context": "Real business questions cross 3+ tables: 'Show me each customer's name, what they ordered, and the product category.' That requires joining customers → orders → products. Multi-table JOINs let you traverse the entire data model in one query.",
            "concept": {
                "theory": "You can chain as many JOINs as needed — each JOIN adds another table to the result. The query builds up row by row: start with table A, join B on a matching key, then join C on a matching key from B or A. Table aliases (short names like c, o, p) are essential to keep queries readable and to disambiguate columns with the same name.",
                "business_angle": "A typical analytics query might join 4-5 tables: customer info + orders + order line items + products + product categories. Mastering multi-table JOINs lets you write queries that answer questions no single table can answer alone.",
                "worked_example_intro": "We'll join 3 tables: customers, orders, and products to build a complete order summary.",
                "key_insight": "Always alias your tables (AS c, AS o, AS p). When two tables have a column with the same name (like 'name' or 'id'), you must prefix with the alias (c.name, p.name) or SQL won't know which you mean."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE customers (id INTEGER, name TEXT, city TEXT)')
c.execute('CREATE TABLE orders (id INTEGER, cust_id INTEGER, prod_id INTEGER, qty INTEGER, date TEXT)')
c.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)')
c.executemany('INSERT INTO customers VALUES (?,?,?)',[(1,'Alice','NYC'),(2,'Bob','LA'),(3,'Carol','Chicago')])
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?)',[(1,1,2,3,'2024-01-10'),(2,1,1,1,'2024-02-15'),(3,2,3,2,'2024-01-20'),(4,3,1,1,'2024-03-05'),(5,3,2,5,'2024-03-10')])
c.executemany('INSERT INTO products VALUES (?,?,?,?)',[(1,'Laptop','Electronics',999),(2,'Mouse','Electronics',29),(3,'Keyboard','Electronics',79)])

print('=== Full Order Detail (3-table JOIN) ===')
for r in c.execute('''
    SELECT
        cu.name     AS customer,
        cu.city,
        o.date,
        pr.name     AS product,
        pr.category,
        o.qty,
        ROUND(o.qty * pr.price, 2) AS line_total
    FROM orders AS o
    INNER JOIN customers AS cu ON o.cust_id = cu.id
    INNER JOIN products  AS pr ON o.prod_id = pr.id
    ORDER BY cu.name, o.date
'''):
    print(f"  {r[0]:<8} ({r[1]:<9}) | {r[2]} | {r[3]:<10} x{r[4]} = ${r[6]:.0f}")

print('\\n=== Revenue by customer & category ===')
for r in c.execute('''
    SELECT cu.name, pr.category, SUM(o.qty * pr.price) AS revenue
    FROM orders o
    JOIN customers cu ON o.cust_id = cu.id
    JOIN products  pr ON o.prod_id = pr.id
    GROUP BY cu.name, pr.category
    ORDER BY cu.name, revenue DESC
'''):
    print(f"  {r[0]:<8} | {r[1]:<13} | ${r[2]:,.0f}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "FROM a JOIN b ON a.id = b.a_id JOIN c ON b.c_id = c.id",
                        "SELECT a.name, b.value, c.label FROM a JOIN b ON ... JOIN c ON ...",
                        "Always alias: FROM orders AS o JOIN customers AS c ON o.cust_id = c.id"
                    ],
                    "notes": "Each JOIN adds one table. The ON clause can reference any previously joined table. Alias every table when joining 3+."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "In a 3-table JOIN (orders JOIN customers JOIN products), which table do you typically start FROM?",
                        "options": [
                            "Always start from the largest table",
                            "Start from the fact table (orders) and join dimension tables to it",
                            "Alphabetically first table",
                            "It doesn't matter — results are the same regardless"
                        ],
                        "answer": 3,
                        "explanation": "SQL's query optimizer reorders joins internally, so results are identical regardless of table order. However, conventionally starting from the central 'fact' table (orders, transactions) and joining lookup 'dimension' tables to it improves readability."
                    },
                    {
                        "type": "true_false",
                        "question": "When two joined tables both have a column named 'name', you must prefix with the table alias to avoid an ambiguity error.",
                        "answer": True,
                        "explanation": "SQL raises an 'ambiguous column' error if you use an unqualified column name that exists in multiple joined tables. Always use table_alias.column_name when joining tables with overlapping column names."
                    },
                    {
                        "type": "fill_blank",
                        "question": "Complete the 3-table join: FROM orders AS o JOIN customers AS c ON o.cust_id = c.id ___ products AS p ON o.prod_id = p.id",
                        "template": "FROM orders AS o JOIN customers AS c ON o.cust_id = c.id ___ products AS p ON o.prod_id = p.id",
                        "answer": "JOIN",
                        "explanation": "Each additional table needs its own JOIN ... ON clause. You can chain as many JOINs as needed, each linking via its foreign key relationship."
                    }
                ]
            },
            "challenge": {
                "instructions": "Build a complete sales report joining 4 tables: reps, regions, sales, products. Print each sale with rep name, region, product name, quantity, and total value. Then summarize revenue by region.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE regions (id INTEGER, name TEXT)')
cur.execute('CREATE TABLE reps (id INTEGER, name TEXT, region_id INTEGER)')
cur.execute('CREATE TABLE products (id INTEGER, name TEXT, price REAL)')
cur.execute('CREATE TABLE sales (id INTEGER, rep_id INTEGER, product_id INTEGER, qty INTEGER)')
cur.executemany('INSERT INTO regions VALUES (?,?)',[(1,'East'),(2,'West'),(3,'Central')])
cur.executemany('INSERT INTO reps VALUES (?,?,?)',[(1,'Ana',1),(2,'Ben',2),(3,'Cara',1),(4,'Dan',3)])
cur.executemany('INSERT INTO products VALUES (?,?,?)',[(1,'Widget',50),(2,'Gadget',120),(3,'Doohickey',35)])
cur.executemany('INSERT INTO sales VALUES (?,?,?,?)',[(1,1,1,10),(2,1,2,3),(3,2,3,20),(4,3,1,5),(5,3,2,8),(6,4,3,15)])

print('=== Full Sales Detail ===')
# 4-table JOIN here

print('\\n=== Revenue by Region ===')
# Aggregate with GROUP BY region

conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "JOIN"},
                    {"type": "output_contains", "value": "East"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE regions (id INTEGER, name TEXT)')
cur.execute('CREATE TABLE reps (id INTEGER, name TEXT, region_id INTEGER)')
cur.execute('CREATE TABLE products (id INTEGER, name TEXT, price REAL)')
cur.execute('CREATE TABLE sales (id INTEGER, rep_id INTEGER, product_id INTEGER, qty INTEGER)')
cur.executemany('INSERT INTO regions VALUES (?,?)',[(1,'East'),(2,'West'),(3,'Central')])
cur.executemany('INSERT INTO reps VALUES (?,?,?)',[(1,'Ana',1),(2,'Ben',2),(3,'Cara',1),(4,'Dan',3)])
cur.executemany('INSERT INTO products VALUES (?,?,?)',[(1,'Widget',50),(2,'Gadget',120),(3,'Doohickey',35)])
cur.executemany('INSERT INTO sales VALUES (?,?,?,?)',[(1,1,1,10),(2,1,2,3),(3,2,3,20),(4,3,1,5),(5,3,2,8),(6,4,3,15)])
print('=== Full Sales Detail ===')
for r in cur.execute('''SELECT rp.name, rg.name, pr.name, s.qty, s.qty*pr.price AS total FROM sales s JOIN reps rp ON s.rep_id=rp.id JOIN regions rg ON rp.region_id=rg.id JOIN products pr ON s.product_id=pr.id ORDER BY rg.name, rp.name'''):
    print(f"  {r[0]:<6} | {r[1]:<8} | {r[2]:<12} x{r[3]} = ${r[4]:.0f}")
print('\\n=== Revenue by Region ===')
for r in cur.execute('''SELECT rg.name, SUM(s.qty*pr.price) AS revenue FROM sales s JOIN reps rp ON s.rep_id=rp.id JOIN regions rg ON rp.region_id=rg.id JOIN products pr ON s.product_id=pr.id GROUP BY rg.name ORDER BY revenue DESC'''):
    print(f"  {r[0]}: ${r[1]:,.0f}")
conn.close()""",
                "challenge_variations": [
                    "Join 4 tables: students, courses, enrollments, grades. Show each student's name, course, and grade.",
                    "Join employees, departments, projects, and assignments. Show who is working on what project in which department.",
                    "Join flights, airports (twice — for origin and destination), and airlines. Show flight number, origin city, destination city, airline name.",
                    "Join invoices, line_items, products, and clients. Calculate total invoice value per client.",
                    "Join blog_posts, authors, tags, and post_tags. Show post title, author name, and all associated tags.",
                    "Join orders, customers, shipping_addresses, and carriers. Show order ID, customer, ship-to address, and carrier name.",
                    "Join movies, actors, roles, and studios. Show movie title, actor name, character, and studio.",
                    "Join recipes, ingredients, recipe_ingredients, and nutritional_info. Calculate total calories per recipe.",
                    "Join hospitals, doctors, specialties, and appointments. Show doctor name, specialty, and patient count.",
                    "Self-join employees to get employee name AND manager name by joining employees to itself on manager_id."
                ]
            }
        },
        {
            "id": "m3-l13",
            "title": "Subqueries — Queries Inside Queries",
            "subtitle": "Use a query result as the input to another query",
            "difficulty": "intermediate",
            "business_context": "You want customers who spent MORE than the average customer. You can't know the average until you've looked at all customers. The solution: calculate the average in an inner query first, then use that result to filter in the outer query.",
            "concept": {
                "theory": "A subquery is a SELECT statement nested inside another SELECT, WHERE, FROM, or HAVING clause. The inner query runs first, producing a value or set of values that the outer query uses. Subqueries can return a single value (scalar), a list (used with IN), or a full table (used in FROM).",
                "business_angle": "Subqueries answer questions that require two steps: 'Find products priced above average' (step 1: calculate average, step 2: filter), 'Find customers in the top 10% by spend', 'Find all orders placed after the first order from customer X'.",
                "worked_example_intro": "We'll find customers who spent above average, and products priced below the category average.",
                "key_insight": "If you find yourself doing a query, writing down the result, then doing another query using that number — you need a subquery. Common patterns: WHERE col > (SELECT AVG(col) ...), WHERE id IN (SELECT id FROM ... WHERE ...), FROM (SELECT ...) AS derived_table."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE customers (id INTEGER, name TEXT)')
cur.execute('CREATE TABLE orders (id INTEGER, cust_id INTEGER, amount REAL)')
cur.executemany('INSERT INTO customers VALUES (?,?)',[(1,'Alice'),(2,'Bob'),(3,'Carol'),(4,'Dave'),(5,'Eve')])
cur.executemany('INSERT INTO orders VALUES (?,?,?)',[(1,1,500),(2,1,300),(3,2,150),(4,3,800),(5,3,200),(6,4,1200),(7,5,50)])

# Scalar subquery in WHERE
print('=== Customers who spent above overall average ===')
for r in cur.execute('''
    SELECT c.name, SUM(o.amount) AS total
    FROM customers c JOIN orders o ON c.id = o.cust_id
    GROUP BY c.id, c.name
    HAVING SUM(o.amount) > (SELECT AVG(total_spent) FROM
        (SELECT SUM(amount) AS total_spent FROM orders GROUP BY cust_id))
    ORDER BY total DESC
'''):
    print(f"  {r[0]}: ${r[1]:,.0f}")

# Subquery with IN
print('\\n=== Customers who ordered in January 2024 ===')
cur.execute('ALTER TABLE orders ADD COLUMN date TEXT')
cur.execute("UPDATE orders SET date = CASE id WHEN 1 THEN '2024-01-05' WHEN 2 THEN '2024-02-10' WHEN 3 THEN '2024-01-22' ELSE '2024-03-15' END")
for r in cur.execute('''
    SELECT name FROM customers
    WHERE id IN (
        SELECT cust_id FROM orders
        WHERE date LIKE '2024-01%'
    )
'''):
    print(f"  {r[0]}")

# Derived table in FROM
print('\\n=== Average spend per customer tier ===')
for r in cur.execute('''
    SELECT
        CASE WHEN total >= 800 THEN 'High'
             WHEN total >= 400 THEN 'Mid'
             ELSE 'Low' END AS tier,
        COUNT(*) AS customers,
        ROUND(AVG(total),0) AS avg_spend
    FROM (
        SELECT cust_id, SUM(amount) AS total FROM orders GROUP BY cust_id
    ) AS customer_totals
    GROUP BY tier
'''):
    print(f"  {r[0]}: {r[1]} customers | avg ${r[2]:,.0f}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "WHERE col > (SELECT AVG(col) FROM table)  -- scalar subquery",
                        "WHERE id IN (SELECT id FROM other_table WHERE condition)  -- list subquery",
                        "FROM (SELECT ... FROM ...) AS derived  -- derived table"
                    ],
                    "notes": "Scalar subqueries must return exactly one value. IN subqueries return a column of values. Derived tables in FROM must be aliased."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "What does 'WHERE salary > (SELECT AVG(salary) FROM employees)' do?",
                        "options": [
                            "Syntax error — can't use SELECT inside WHERE",
                            "Returns employees with salary above the company average",
                            "Returns employees with salary equal to the average",
                            "Calculates each employee's salary relative to average"
                        ],
                        "answer": 1,
                        "explanation": "The inner query (SELECT AVG(salary) FROM employees) runs first and returns a single number. The outer WHERE then filters employees whose salary exceeds that number. This is a scalar subquery."
                    },
                    {
                        "type": "true_false",
                        "question": "A derived table subquery in the FROM clause must be given an alias.",
                        "answer": True,
                        "explanation": "When you put a subquery in the FROM clause (like FROM (SELECT ...) AS derived), SQL requires an alias. Without it, you get a syntax error. The alias lets you reference columns from the subquery in the outer SELECT."
                    },
                    {
                        "type": "fill_blank",
                        "question": "Find products whose price is above average: SELECT name FROM products WHERE price > (SELECT ___(price) FROM products)",
                        "template": "SELECT name FROM products WHERE price > (SELECT ___(price) FROM products)",
                        "answer": "AVG",
                        "explanation": "AVG(price) computes the average price across all products. The subquery runs first and returns that single average value, which the outer WHERE uses to filter."
                    }
                ]
            },
            "challenge": {
                "instructions": "Using subqueries: (1) find products priced above their category average, (2) find customers who placed orders in both January AND February 2024 using IN with two subqueries and INTERSECT (or two INs). Print results with explanatory headers.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)')
cur.execute('CREATE TABLE orders (id INTEGER, cust_id INTEGER, prod_id INTEGER, date TEXT)')
cur.execute('CREATE TABLE customers (id INTEGER, name TEXT)')
cur.executemany('INSERT INTO products VALUES (?,?,?,?)',[(1,'Pro Laptop','Electronics',1200),(2,'Basic Laptop','Electronics',600),(3,'Standing Desk','Furniture',800),(4,'Basic Chair','Furniture',200),(5,'Pro Chair','Furniture',900)])
cur.executemany('INSERT INTO customers VALUES (?,?)',[(1,'Alice'),(2,'Bob'),(3,'Carol')])
cur.executemany('INSERT INTO orders VALUES (?,?,?,?)',[(1,1,1,'2024-01-10'),(2,1,3,'2024-02-15'),(3,2,2,'2024-01-20'),(4,3,5,'2024-03-01'),(5,2,4,'2024-02-08')])

print('=== Products priced above their category average ===')
# Hint: subquery that calculates avg price per category, then join back
# SELECT p.name, p.category, p.price FROM products p
# WHERE p.price > (SELECT AVG(...) FROM products WHERE category = p.category)

print('\\n=== Customers who ordered in BOTH Jan AND Feb 2024 ===')
# Hint: WHERE cust_id IN (...jan...) AND cust_id IN (...feb...)

conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "SELECT"},
                    {"type": "output_contains", "value": "Laptop"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)')
cur.execute('CREATE TABLE orders (id INTEGER, cust_id INTEGER, prod_id INTEGER, date TEXT)')
cur.execute('CREATE TABLE customers (id INTEGER, name TEXT)')
cur.executemany('INSERT INTO products VALUES (?,?,?,?)',[(1,'Pro Laptop','Electronics',1200),(2,'Basic Laptop','Electronics',600),(3,'Standing Desk','Furniture',800),(4,'Basic Chair','Furniture',200),(5,'Pro Chair','Furniture',900)])
cur.executemany('INSERT INTO customers VALUES (?,?)',[(1,'Alice'),(2,'Bob'),(3,'Carol')])
cur.executemany('INSERT INTO orders VALUES (?,?,?,?)',[(1,1,1,'2024-01-10'),(2,1,3,'2024-02-15'),(3,2,2,'2024-01-20'),(4,3,5,'2024-03-01'),(5,2,4,'2024-02-08')])
print('=== Products priced above their category average ===')
for r in cur.execute("SELECT name, category, price FROM products p WHERE price > (SELECT AVG(price) FROM products WHERE category = p.category) ORDER BY category, price DESC"):
    print(f"  {r[0]} ({r[1]}): ${r[2]:,.0f}")
print('\\n=== Customers who ordered in BOTH Jan AND Feb 2024 ===')
for r in cur.execute("SELECT c.name FROM customers c WHERE c.id IN (SELECT cust_id FROM orders WHERE date LIKE '2024-01%') AND c.id IN (SELECT cust_id FROM orders WHERE date LIKE '2024-02%')"):
    print(f"  {r[0]}")
conn.close()""",
                "challenge_variations": [
                    "Find employees earning more than the average salary in their own department (correlated subquery).",
                    "Find the top 3 customers by total spend using a subquery with ORDER BY + LIMIT.",
                    "Find products that have never been ordered using NOT IN with a subquery.",
                    "Find orders placed after the most recent order by customer 'Alice' using a scalar subquery.",
                    "Calculate what percentage of orders are above average value using a subquery in SELECT.",
                    "Find cities with more restaurants than the average city (subquery in HAVING).",
                    "Use a derived table to calculate monthly revenue, then find months above the annual average.",
                    "Find students who scored above the class average on at least one test.",
                    "Find the second-highest salary using a subquery: WHERE salary = (SELECT MAX(salary) WHERE salary < (SELECT MAX(salary) ...)).",
                    "Find categories where every product is priced above $100 (ALL keyword with subquery)."
                ]
            }
        },
        {
            "id": "m3-l14",
            "title": "Primary Keys & Foreign Keys",
            "subtitle": "The rules that keep your data from turning into chaos",
            "difficulty": "beginner",
            "business_context": "What happens if you delete a customer who still has open orders? Without key constraints, you'd have 'orphan' orders pointing to a customer that no longer exists — broken data. Primary and foreign keys are the database's built-in safety net.",
            "concept": {
                "theory": "A Primary Key (PK) is a column (or set of columns) that uniquely identifies each row in a table. No duplicates, no NULLs. A Foreign Key (FK) is a column that references another table's primary key, creating a link between tables. Foreign key constraints enforce referential integrity — you can't reference a row that doesn't exist.",
                "business_angle": "PKs and FKs are the backbone of relational databases. They enforce data quality automatically: you can't place an order for a product that doesn't exist, you can't assign an employee to a department that was deleted. This saves countless bugs and bad reports.",
                "worked_example_intro": "We'll create tables with proper PK and FK constraints, see what happens when you violate them, and understand cascade behavior.",
                "key_insight": "INTEGER PRIMARY KEY in SQLite creates an auto-incrementing ID (alias for rowid). FOREIGN KEY constraints must be enabled in SQLite with 'PRAGMA foreign_keys = ON'. Without it, SQLite accepts invalid foreign keys silently."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')  # MUST enable in SQLite!
cur = conn.cursor()

cur.execute('''CREATE TABLE departments (
    id   INTEGER PRIMARY KEY,  -- auto-increment unique ID
    name TEXT NOT NULL UNIQUE  -- no duplicate dept names
)''')

cur.execute('''CREATE TABLE employees (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    dept_id INTEGER NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(id)
        ON DELETE RESTRICT   -- can't delete dept if employees exist
)''')

cur.executemany('INSERT INTO departments VALUES (?,?)',[(1,'Engineering'),(2,'Sales'),(3,'Marketing')])
cur.executemany('INSERT INTO employees VALUES (?,?,?)',[(1,'Alice',1),(2,'Bob',2),(3,'Carol',1)])

print('=== Employees with departments (FK join) ===')
for r in cur.execute('SELECT e.name, d.name FROM employees e JOIN departments d ON e.dept_id = d.id'):
    print(f"  {r[0]} → {r[1]}")

# Try to insert employee with non-existent dept_id
try:
    cur.execute('INSERT INTO employees VALUES (4, "Dave", 99)')  # dept 99 doesn't exist!
    print('Inserted (bad!)')
except Exception as e:
    print(f'\\nFK Violation caught: {e}')

# Try to delete a dept that has employees
try:
    cur.execute('DELETE FROM departments WHERE id = 1')
    print('Deleted (bad!)')
except Exception as e:
    print(f'Delete Violation caught: {e}')

print('\\n=== Data integrity preserved ===')
for r in cur.execute('SELECT COUNT(*) FROM employees'):
    print(f"  Employees still intact: {r[0]}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "id INTEGER PRIMARY KEY  -- unique, not null, auto-increment",
                        "FOREIGN KEY (col) REFERENCES other_table(id)",
                        "ON DELETE CASCADE  -- auto-delete child rows when parent deleted",
                        "ON DELETE RESTRICT  -- prevent deleting parent if children exist",
                        "PRAGMA foreign_keys = ON  -- SQLite-specific, must enable FK checks"
                    ],
                    "notes": "SQLite has FKs but doesn't enforce them by default — always add PRAGMA foreign_keys = ON at the start of your connection."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "What does ON DELETE CASCADE do?",
                        "options": [
                            "Prevents deleting a parent row if children exist",
                            "Automatically deletes all child rows when the parent is deleted",
                            "Sets foreign key columns to NULL when parent is deleted",
                            "Creates a backup of deleted rows"
                        ],
                        "answer": 1,
                        "explanation": "ON DELETE CASCADE means: when you delete a row in the parent table, automatically delete all rows in the child table that reference it. Useful for 'if we delete a customer, delete all their orders too.'"
                    },
                    {
                        "type": "true_false",
                        "question": "A primary key column can contain NULL values.",
                        "answer": False,
                        "explanation": "Primary keys must be NOT NULL and UNIQUE. NULL means 'unknown' — you can't uniquely identify a row with an unknown value. Most databases enforce this automatically when you declare PRIMARY KEY."
                    },
                    {
                        "type": "fill_blank",
                        "question": "To enable foreign key enforcement in SQLite, add: ___ foreign_keys = ON after opening a connection.",
                        "template": "___ foreign_keys = ON",
                        "answer": "PRAGMA",
                        "explanation": "PRAGMA is SQLite's way of setting database-level options. PRAGMA foreign_keys = ON must be run on each new connection — SQLite disables FK enforcement by default for backwards compatibility."
                    }
                ]
            },
            "challenge": {
                "instructions": "Build a library database with books, authors, and borrow_records. Enforce: no book can have an invalid author_id, no borrow record can reference a non-existent book. Enable FK enforcement. Try inserting a bad record and catch the error. Then print a report of all borrowed books with author names.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

# Create tables with PK and FK constraints
# authors: id (PK), name
# books: id (PK), title, author_id (FK -> authors.id)
# borrow_records: id (PK), book_id (FK -> books.id), borrower, date

# Insert 3 authors, 5 books, 4 borrow records

# Try inserting a book with author_id = 999 (doesn't exist)
# Catch the error and print it

print('=== Currently Borrowed Books ===')
# Join borrow_records + books + authors
# Show: borrower, book title, author name, date

conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "FOREIGN KEY"},
                    {"type": "code_contains", "value": "PRAGMA foreign_keys"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()
cur.execute('CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
cur.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL, FOREIGN KEY (author_id) REFERENCES authors(id))')
cur.execute('CREATE TABLE borrow_records (id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL, borrower TEXT, date TEXT, FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE)')
cur.executemany('INSERT INTO authors VALUES (?,?)',[(1,'Orwell'),(2,'Hemingway'),(3,'Austen')])
cur.executemany('INSERT INTO books VALUES (?,?,?)',[(1,'1984',1),(2,'Animal Farm',1),(3,'The Sun Also Rises',2),(4,'A Farewell to Arms',2),(5,'Pride and Prejudice',3)])
cur.executemany('INSERT INTO borrow_records VALUES (?,?,?,?)',[(1,1,'Alice','2024-03-01'),(2,3,'Bob','2024-03-05'),(3,5,'Carol','2024-03-10'),(4,2,'Dave','2024-03-12')])
try:
    cur.execute('INSERT INTO books VALUES (6, "Fake Book", 999)')
except Exception as e:
    print(f'FK Violation: {e}')
print('\\n=== Currently Borrowed Books ===')
for r in cur.execute('SELECT br.borrower, b.title, a.name, br.date FROM borrow_records br JOIN books b ON br.book_id=b.id JOIN authors a ON b.author_id=a.id ORDER BY br.date'):
    print(f"  {r[0]:<8} | '{r[1]}' by {r[2]} | {r[3]}")
conn.close()""",
                "challenge_variations": [
                    "Create an e-commerce schema with categories, products, and inventory. Enforce that products must belong to valid categories.",
                    "Build a school database with classes, students, and enrollments. Use FK to ensure students can't enroll in non-existent classes.",
                    "Add ON DELETE CASCADE to a user/posts relationship. Verify that deleting a user removes all their posts.",
                    "Add ON DELETE SET NULL to an employee/manager relationship. Verify that deleting a manager sets reports' manager_id to NULL.",
                    "Create a COMPOSITE primary key on an enrollment table: PRIMARY KEY (student_id, course_id) — no duplicate enrollments.",
                    "Add a UNIQUE constraint to email in a users table and verify it rejects duplicate emails.",
                    "Create a CHECK constraint: salary REAL CHECK(salary > 0). Verify it rejects negative salaries.",
                    "Build a multi-level FK: companies → departments → employees. Cascade delete from company level.",
                    "Add a DEFAULT constraint to order status: status TEXT DEFAULT 'pending'. Verify inserts without status use the default.",
                    "Demonstrate the difference between ON DELETE RESTRICT and ON DELETE CASCADE with the same parent row."
                ]
            }
        },
        {
            "id": "m3-l15",
            "title": "Database Normalization",
            "subtitle": "Designing tables that eliminate redundancy and prevent update anomalies",
            "difficulty": "intermediate",
            "business_context": "A colleague stores customer name, address, AND order details all in one massive table. When the customer moves, they have to update 50 rows. If they miss one, the data is inconsistent. Normalization is the discipline that prevents this — it's how professional databases are designed.",
            "concept": {
                "theory": "Normalization is the process of organizing tables to reduce redundancy. The three main normal forms are: 1NF (atomic values — no lists in cells), 2NF (no partial dependencies on composite keys), 3NF (no transitive dependencies — each non-key column depends only on the primary key). In practice, most business databases aim for 3NF.",
                "business_angle": "Unnormalized databases cause 'update anomalies': you update a customer address in row 1 but miss row 47 — now you have two different addresses for the same customer. Normalization means each fact lives in exactly one place, so updating it updates everywhere.",
                "worked_example_intro": "We'll start with a denormalized 'flat' table with all data in one place, then refactor it to 3NF.",
                "key_insight": "The practical test for 3NF: every column in a table should describe ONLY the primary key of that table — nothing else. If a column in 'orders' describes the customer (like customer_city), it belongs in a customers table, not the orders table."
            },
            "worked_example": """import sqlite3

# BEFORE: Unnormalized (everything in one table)
print('=== UNNORMALIZED: Everything in one table ===')
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('''CREATE TABLE orders_flat (
    order_id INTEGER, order_date TEXT,
    customer_id INTEGER, customer_name TEXT, customer_email TEXT, customer_city TEXT,
    product_id INTEGER, product_name TEXT, product_category TEXT, product_price REAL,
    quantity INTEGER
)''')
cur.executemany('INSERT INTO orders_flat VALUES (?,?,?,?,?,?,?,?,?,?,?)',[
    (1,'2024-01-10',1,'Alice','a@co.com','NYC',10,'Laptop','Electronics',999,1),
    (2,'2024-02-05',1,'Alice','a@co.com','NYC',11,'Mouse','Electronics',29,2),  # Alice duplicated!
    (3,'2024-01-15',2,'Bob','b@co.com','LA',10,'Laptop','Electronics',999,1),   # Laptop duplicated!
])
for r in cur.execute('SELECT * FROM orders_flat'):
    print(f"  Order {r[0]}: {r[3]} bought {r[7]} x{r[10]}")
print("  Problem: Alice's info duplicated across 2 rows. Laptop info duplicated across 2 rows.")
conn.close()

# AFTER: Normalized to 3NF
print('\\n=== NORMALIZED: 3NF design ===')
conn2 = sqlite3.connect(':memory:')
cur2 = conn2.cursor()
cur2.execute('CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT)')
cur2.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
cur2.execute('CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, date TEXT, FOREIGN KEY(customer_id) REFERENCES customers(id))')
cur2.execute('CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER, PRIMARY KEY(order_id, product_id))')
cur2.executemany('INSERT INTO customers VALUES (?,?,?,?)',[(1,'Alice','a@co.com','NYC'),(2,'Bob','b@co.com','LA')])
cur2.executemany('INSERT INTO products VALUES (?,?,?,?)',[(10,'Laptop','Electronics',999),(11,'Mouse','Electronics',29)])
cur2.executemany('INSERT INTO orders VALUES (?,?,?)',[(1,1,'2024-01-10'),(2,1,'2024-02-05'),(3,2,'2024-01-15')])
cur2.executemany('INSERT INTO order_items VALUES (?,?,?)',[(1,10,1),(2,11,2),(3,10,1)])
print("  Alice lives in ONE place (customers table). Update once — fixed everywhere.")
print("  Laptop price lives in ONE place (products table).")

# Reconstruct the full view via JOIN
for r in cur2.execute('''
    SELECT c.name, o.date, p.name, oi.qty, oi.qty*p.price AS total
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN customers c ON o.customer_id = c.id
    JOIN products p ON oi.product_id = p.id
'''):
    print(f"  {r[0]}: {r[2]} x{r[3]} on {r[1]} = ${r[4]:.0f}")
conn2.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "1NF: each cell holds one atomic value (no comma-separated lists)",
                        "2NF: non-key columns depend on the WHOLE primary key (no partial deps)",
                        "3NF: non-key columns depend ONLY on the primary key (no transitive deps)"
                    ],
                    "notes": "Quick test: if updating one column requires updating other columns in the same table, you have a normalization problem."
                },
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "A table has columns: order_id, product_id, product_name, product_price, quantity. What's wrong with this design?",
                        "options": [
                            "Nothing — this is a good design",
                            "product_name and product_price describe the product, not the order — they belong in a products table",
                            "quantity should be in a separate table",
                            "order_id should not be in the table"
                        ],
                        "answer": 1,
                        "explanation": "product_name and product_price are facts about the product, not the order. If a product's price changes, you'd have to update every row in this table. 3NF says: move product facts to a products table, and only store product_id here as a foreign key."
                    },
                    {
                        "type": "true_false",
                        "question": "A column storing values like 'red,blue,green' in a single cell violates First Normal Form (1NF).",
                        "answer": True,
                        "explanation": "1NF requires atomic (indivisible) values. A cell containing 'red,blue,green' is storing multiple values, violating 1NF. The fix is to create a separate colors table with one row per color per item."
                    },
                    {
                        "type": "fill_blank",
                        "question": "In 3NF, every non-key column should depend only on the ___ key — not on other non-key columns.",
                        "template": "Every non-key column should depend only on the ___ key.",
                        "answer": "primary",
                        "explanation": "3NF eliminates transitive dependencies. If column C depends on column B (not the PK) which depends on column A (the PK), then C should be moved to a separate table where B is the PK."
                    }
                ]
            },
            "challenge": {
                "instructions": "You're given a denormalized 'student_records' table. Normalize it to 3NF by splitting into: students, courses, instructors, enrollments. Then verify the data is correct by running a JOIN that reconstructs the original flat view.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()

# Denormalized source data
flat_data = [
    # (student_id, student_name, student_email, course_id, course_name, instructor_id, instructor_name, grade)
    (1, 'Alice', 'alice@u.edu', 101, 'Statistics', 201, 'Dr. Smith', 'A'),
    (1, 'Alice', 'alice@u.edu', 102, 'Python',     202, 'Prof. Lee', 'B+'),
    (2, 'Bob',   'bob@u.edu',   101, 'Statistics', 201, 'Dr. Smith', 'B'),
    (3, 'Carol', 'carol@u.edu', 102, 'Python',     202, 'Prof. Lee', 'A-'),
    (3, 'Carol', 'carol@u.edu', 103, 'ML Basics',  201, 'Dr. Smith', 'A'),
]

# TODO: Create 4 normalized tables and insert data
# 1. students (id, name, email)
# 2. instructors (id, name)
# 3. courses (id, name, instructor_id FK)
# 4. enrollments (student_id FK, course_id FK, grade) — composite PK

# TODO: JOIN all 4 tables and reconstruct the full view
print('=== Reconstructed View from Normalized Tables ===')

conn.close()""",
                "tests": [
                    {"type": "code_contains", "value": "FOREIGN KEY"},
                    {"type": "output_contains", "value": "Alice"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
cur.execute('CREATE TABLE instructors (id INTEGER PRIMARY KEY, name TEXT)')
cur.execute('CREATE TABLE courses (id INTEGER PRIMARY KEY, name TEXT, instructor_id INTEGER, FOREIGN KEY(instructor_id) REFERENCES instructors(id))')
cur.execute('CREATE TABLE enrollments (student_id INTEGER, course_id INTEGER, grade TEXT, PRIMARY KEY(student_id, course_id), FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(course_id) REFERENCES courses(id))')
cur.executemany('INSERT OR IGNORE INTO students VALUES (?,?,?)',[(1,'Alice','alice@u.edu'),(2,'Bob','bob@u.edu'),(3,'Carol','carol@u.edu')])
cur.executemany('INSERT OR IGNORE INTO instructors VALUES (?,?)',[(201,'Dr. Smith'),(202,'Prof. Lee')])
cur.executemany('INSERT OR IGNORE INTO courses VALUES (?,?,?)',[(101,'Statistics',201),(102,'Python',202),(103,'ML Basics',201)])
cur.executemany('INSERT INTO enrollments VALUES (?,?,?)',[(1,101,'A'),(1,102,'B+'),(2,101,'B'),(3,102,'A-'),(3,103,'A')])
print('=== Reconstructed View from Normalized Tables ===')
for r in cur.execute('SELECT s.name, c.name, i.name, e.grade FROM enrollments e JOIN students s ON e.student_id=s.id JOIN courses c ON e.course_id=c.id JOIN instructors i ON c.instructor_id=i.id ORDER BY s.name, c.name'):
    print(f"  {r[0]:<8} | {r[1]:<12} | {r[2]:<12} | {r[3]}")
conn.close()""",
                "challenge_variations": [
                    "Normalize a hospital records table (patient, doctor, department, visit_date, diagnosis) to 3NF.",
                    "Convert a music library flat table (artist, album, track, genre, year, duration) to normalized form.",
                    "Normalize an e-commerce flat table into categories, products, customers, orders, order_items.",
                    "Identify which normal form is violated: a cell containing 'Python; SQL; ML' as skills for one employee.",
                    "Split a real estate table: property, agent, agency, buyer, sale_date into proper 3NF tables.",
                    "Design a normalized schema for a social media app: users, posts, comments, likes, followers.",
                    "Normalize a gradebook: student, teacher, class, room_number, grade, semester.",
                    "Identify the transitive dependency in: invoice_id, customer_id, customer_city, city_tax_rate — and fix it.",
                    "Design a normalized restaurant schema: restaurants, menus, dishes, orders, order_items, ingredients.",
                    "Explain why OLAP (data warehouses) often intentionally denormalize and when that is the right tradeoff."
                ]
            }
        },
        {
            "id": "m3-l16",
            "title": "Entity-Relationship Diagrams (ERDs)",
            "subtitle": "Visualize your database before you build it",
            "difficulty": "beginner",
            "business_context": "Before writing a single line of SQL, professional database designers draw an ERD — a map of all tables, their columns, and how they connect. It prevents costly redesigns later and helps communicate the data model to non-technical stakeholders.",
            "concept": {
                "theory": "An ERD shows entities (tables), attributes (columns), and relationships (foreign key links). Relationships have cardinality: one-to-one (1:1), one-to-many (1:N), or many-to-many (M:N). M:N relationships require a junction/bridge table. ERDs are the blueprint — SQL is the construction.",
                "business_angle": "Reading an ERD lets you instantly understand a new codebase's data model, identify what JOINs you'll need, and spot missing relationships. Every analytics role expects you to read — and ideally draw — ERDs.",
                "worked_example_intro": "We'll implement an ERD for a simple e-commerce system: customers, orders, products, and the bridge table order_items.",
                "key_insight": "Many-to-many relationships can't be implemented directly in SQL. An order can contain many products; a product can appear on many orders. The solution: a bridge table (order_items) with two foreign keys, one pointing to each side."
            },
            "worked_example": """import sqlite3

# ERD for a mini e-commerce system:
#
#   customers  ──<  orders  >──  order_items  ──<  products
#   (1 customer   (1 order     (bridge table:     (1 product
#   many orders)  many items)  order_id + prod_id) many items)
#
# Cardinalities:
#   customers 1:N orders     (one customer, many orders)
#   orders    1:N order_items (one order, many line items)
#   products  1:N order_items (one product, many line items)

conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

cur.execute('''CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE)''')
cur.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL)''')
cur.execute('''CREATE TABLE orders (
    id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id))''')
cur.execute('''CREATE TABLE order_items (
    order_id INTEGER, product_id INTEGER, qty INTEGER DEFAULT 1,
    PRIMARY KEY(order_id, product_id),           -- composite PK prevents duplicate line items
    FOREIGN KEY(order_id)   REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id))''')

cur.executemany('INSERT INTO customers VALUES(?,?,?)',[(1,'Alice','a@co.com'),(2,'Bob','b@co.com')])
cur.executemany('INSERT INTO products VALUES(?,?,?)',[(1,'Laptop',999),(2,'Mouse',29),(3,'Keyboard',79)])
cur.executemany('INSERT INTO orders VALUES(?,?,?)',[(1,1,'2024-01-10'),(2,2,'2024-02-05')])
cur.executemany('INSERT INTO order_items VALUES(?,?,?)',[(1,1,1),(1,2,2),(2,2,1),(2,3,1)])

# Traverse all 4 tables in one query
print('=== Complete Order Summary ===')
for r in cur.execute('''
    SELECT c.name, o.date, p.name, oi.qty, oi.qty*p.price AS total
    FROM order_items oi
    JOIN orders o ON oi.order_id=o.id
    JOIN customers c ON o.customer_id=c.id
    JOIN products p ON oi.product_id=p.id
    ORDER BY c.name, o.date
'''):
    print(f"  {r[0]:<8} | {r[1]} | {r[2]:<10} x{r[3]} = ${r[4]:.0f}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "1:N  — one customer has many orders (FK in 'many' table)",
                        "M:N  — requires a bridge/junction table with two FKs",
                        "1:1  — rare, use when splitting large table for performance"
                    ],
                    "notes": "Always resolve M:N relationships with a junction table. Name junction tables after the relationship: order_items, student_courses, employee_skills."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Students can enroll in many courses; courses can have many students. This is a ___ relationship.", "options": ["1:1","1:N","M:N","None of the above"], "answer": 2, "explanation": "Many students ↔ many courses is M:N. Implement with a junction table: enrollments(student_id, course_id, grade)."},
                    {"type": "true_false", "question": "A foreign key always goes in the 'many' side of a 1:N relationship.", "answer": True, "explanation": "In 1:N, the FK lives in the 'many' table pointing back to the 'one' table. Orders (many) have a customer_id FK pointing to customers (one)."},
                    {"type": "fill_blank", "question": "A table that resolves a many-to-many relationship by holding two foreign keys is called a ___ table.", "template": "A ___ table resolves M:N by holding two FKs.", "answer": "junction", "explanation": "Junction tables (also called bridge or associative tables) sit between two M:N related tables, holding one FK to each side. Examples: order_items, enrollments, employee_projects."}
                ]
            },
            "challenge": {
                "instructions": "Design and implement an ERD for a movie streaming service. Tables: users, movies, genres, movie_genres (M:N bridge), watch_history. Print a report: for each user, list movies watched with genre.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

# Create: users, movies, genres, movie_genres (bridge), watch_history
# Relationships:
#   users 1:N watch_history N:1 movies
#   movies M:N genres (via movie_genres bridge)

# Insert sample data: 2 users, 4 movies, 3 genres

print('=== Watch History with Genre ===')
# Query joining all tables

conn.close()""",
                "tests": [{"type": "code_contains", "value": "FOREIGN KEY"}, {"type": "code_contains", "value": "JOIN"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()
cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
cur.execute('CREATE TABLE genres (id INTEGER PRIMARY KEY, name TEXT)')
cur.execute('CREATE TABLE movies (id INTEGER PRIMARY KEY, title TEXT)')
cur.execute('CREATE TABLE movie_genres (movie_id INTEGER, genre_id INTEGER, PRIMARY KEY(movie_id,genre_id), FOREIGN KEY(movie_id) REFERENCES movies(id), FOREIGN KEY(genre_id) REFERENCES genres(id))')
cur.execute('CREATE TABLE watch_history (user_id INTEGER, movie_id INTEGER, watched_on TEXT, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(movie_id) REFERENCES movies(id))')
cur.executemany('INSERT INTO users VALUES(?,?)',[(1,'Alice'),(2,'Bob')])
cur.executemany('INSERT INTO genres VALUES(?,?)',[(1,'Action'),(2,'Drama'),(3,'Sci-Fi')])
cur.executemany('INSERT INTO movies VALUES(?,?)',[(1,'Inception'),(2,'The Matrix'),(3,'Titanic'),(4,'Mad Max')])
cur.executemany('INSERT INTO movie_genres VALUES(?,?)',[(1,3),(2,1),(2,3),(3,2),(4,1)])
cur.executemany('INSERT INTO watch_history VALUES(?,?,?)',[(1,1,'2024-01-10'),(1,2,'2024-01-12'),(2,3,'2024-01-11'),(2,4,'2024-01-15')])
print('=== Watch History with Genre ===')
for r in cur.execute('SELECT u.name, m.title, g.name FROM watch_history wh JOIN users u ON wh.user_id=u.id JOIN movies m ON wh.movie_id=m.id JOIN movie_genres mg ON m.id=mg.movie_id JOIN genres g ON mg.genre_id=g.id ORDER BY u.name'):
    print(f"  {r[0]}: {r[1]} ({r[2]})")
conn.close()""",
                "challenge_variations": [
                    "Draw (describe in comments) an ERD for a hospital: patients, doctors, appointments, diagnoses.",
                    "Implement a social network ERD: users, posts, likes (M:N bridge), followers (self-referential M:N).",
                    "Build a recipe app ERD: recipes, ingredients, recipe_ingredients (with quantity column in bridge).",
                    "Design a university ERD: students, courses, instructors, enrollments, departments.",
                    "Implement a ticket system: users, tickets, comments, tags, ticket_tags (M:N).",
                    "Build a music ERD: artists, albums, tracks, playlists, playlist_tracks (M:N with position).",
                    "Design a real estate ERD: properties, agents, clients, showings, offers.",
                    "Implement a job board: companies, jobs, applicants, applications (with status).",
                    "Create a supply chain ERD: suppliers, products, warehouses, inventory (quantity at each warehouse).",
                    "Design a conference ERD: speakers, sessions, attendees, registrations, session_speakers (M:N)."
                ]
            }
        },
        {
            "id": "m3-l17",
            "title": "CREATE TABLE — Defining Your Database Schema",
            "subtitle": "Data types, constraints, and defaults that protect your data",
            "difficulty": "beginner",
            "business_context": "A poorly designed table schema causes problems for years. Allowing negative prices, duplicate emails, or NULL in required fields means bad data silently enters the system and corrupts every report built on it. Good schema design is your first line of defense.",
            "concept": {
                "theory": "CREATE TABLE defines a table's structure: column names, data types, and constraints. SQLite data types: INTEGER (whole numbers), REAL (decimals), TEXT (strings), BLOB (binary). Constraints: NOT NULL (required), UNIQUE (no duplicates), DEFAULT (fallback value), CHECK (custom rule), PRIMARY KEY, FOREIGN KEY.",
                "business_angle": "Every constraint you add to a schema is a business rule enforced automatically. 'Price must be positive', 'Email must be unique', 'Status must be pending/active/closed' — these protect data quality without relying on application code to catch every edge case.",
                "worked_example_intro": "We'll create a well-constrained products table and an orders table, testing each constraint.",
                "key_insight": "In SQLite, INTEGER PRIMARY KEY is a special alias for the rowid — it auto-increments. Use IF NOT EXISTS to make CREATE TABLE idempotent (safe to run multiple times without error)."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY,           -- auto-increment PK
    name        TEXT    NOT NULL,              -- required
    sku         TEXT    NOT NULL UNIQUE,       -- no duplicates
    price       REAL    NOT NULL CHECK(price > 0),    -- must be positive
    category    TEXT    DEFAULT 'Uncategorized',       -- fallback value
    in_stock    INTEGER DEFAULT 1,             -- 1=true, 0=false
    created_at  TEXT    DEFAULT (date('now'))  -- auto-set to today
)''')

# Valid insert
cur.execute("INSERT INTO products(name,sku,price) VALUES ('Laptop','SKU-001',999)")
print('Inserted laptop successfully')

# Test constraints
tests = [
    ("NULL name",   "INSERT INTO products(name,sku,price) VALUES (NULL,'SKU-002',50)"),
    ("Dup SKU",     "INSERT INTO products(name,sku,price) VALUES ('Mouse','SKU-001',29)"),
    ("Neg price",   "INSERT INTO products(name,sku,price) VALUES ('Kbd','SKU-003',-10)"),
]
for label, sql in tests:
    try:
        cur.execute(sql)
        print(f"  {label}: inserted (constraint failed!)")
    except Exception as e:
        print(f"  {label}: BLOCKED — {e}")

# Show defaults applied
for r in cur.execute("SELECT id, name, category, in_stock, created_at FROM products"):
    print(f"\\nRow: id={r[0]}, name={r[1]}, category={r[2]}, in_stock={r[3]}, created={r[4]}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "col TEXT NOT NULL  -- rejects NULL",
                        "col TEXT UNIQUE    -- rejects duplicates",
                        "col REAL CHECK(col > 0)  -- custom rule",
                        "col TEXT DEFAULT 'pending'  -- auto-fill",
                        "CREATE TABLE IF NOT EXISTS  -- safe re-run"
                    ],
                    "notes": "SQLite is flexible with types (type affinity) — storing '99' in an INTEGER column works. Other databases are stricter. Always validate at the app layer too."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Which constraint prevents inserting a row with a duplicate email?", "options": ["NOT NULL","CHECK","UNIQUE","PRIMARY KEY"], "answer": 2, "explanation": "UNIQUE enforces that no two rows have the same value in that column. It differs from PRIMARY KEY only in that a table can have multiple UNIQUE columns but only one PRIMARY KEY."},
                    {"type": "true_false", "question": "DEFAULT values are applied when a column is omitted from an INSERT statement.", "answer": True, "explanation": "If you INSERT without specifying a column, SQLite uses its DEFAULT value. If no default is defined and the column is NOT NULL, the insert fails."},
                    {"type": "fill_blank", "question": "To ensure a column called 'quantity' is always greater than zero, use: quantity INTEGER ___(quantity > 0)", "template": "quantity INTEGER ___(quantity > 0)", "answer": "CHECK", "explanation": "CHECK constraints enforce arbitrary conditions. CHECK(quantity > 0) rejects any insert or update that would set quantity to zero or negative."}
                ]
            },
            "challenge": {
                "instructions": "Create a well-constrained 'employees' table with: auto-increment id, required name, unique email, salary > 0, department (default 'General'), status (CHECK in 'active'/'inactive'/'terminated', default 'active'), hire_date (default today). Test all constraints. Print the inserted row.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()

# Create employees table with all constraints listed above

# Insert one valid employee (omit department and status to test defaults)

# Test: try inserting employee with negative salary (catch error)

# Test: try inserting employee with invalid status 'fired' (catch error)

# Print the valid employee row showing defaults were applied
print('=== Employee Record ===')

conn.close()""",
                "tests": [{"type": "code_contains", "value": "CHECK"}, {"type": "code_contains", "value": "DEFAULT"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute(\'\'\'CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    salary REAL NOT NULL CHECK(salary > 0),
    department TEXT DEFAULT 'General',
    status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive','terminated')),
    hire_date TEXT DEFAULT (date('now'))
)''')
cur.execute("INSERT INTO employees(name,email,salary) VALUES('Alice','alice@co.com',75000)")
try:
    cur.execute("INSERT INTO employees(name,email,salary) VALUES('Bob','bob@co.com',-1000)")
except Exception as e:
    print(f'Neg salary blocked: {e}')
try:
    cur.execute("INSERT INTO employees(name,email,salary,status) VALUES('Carol','c@co.com',60000,'fired')")
except Exception as e:
    print(f'Bad status blocked: {e}')
print('=== Employee Record ===')
for r in cur.execute('SELECT * FROM employees'):
    print(f"  id={r[0]}, name={r[1]}, dept={r[4]}, status={r[5]}, hired={r[6]}")
conn.close()""",
                "challenge_variations": [
                    "Create a transactions table with: amount CHECK > 0, type CHECK IN ('debit','credit'), timestamp DEFAULT now.",
                    "Add a UNIQUE constraint on the combination of (user_id, date) so a user can only have one record per day.",
                    "Create a products table where price_sale must be less than price_regular using CHECK(price_sale < price_regular).",
                    "Use CREATE TABLE AS SELECT to create a new table from a query result (backup/snapshot pattern).",
                    "Add a column to an existing table using ALTER TABLE employees ADD COLUMN phone TEXT.",
                    "Create a table with a composite primary key: PRIMARY KEY(order_id, line_number).",
                    "Design a table for storing configuration key-value pairs where key is UNIQUE and NOT NULL.",
                    "Create a users table where username is UNIQUE and length checked: CHECK(length(username) >= 3).",
                    "Use AUTOINCREMENT vs INTEGER PRIMARY KEY and explain the difference in SQLite.",
                    "Create a versioned records table: (id, version, data) where PRIMARY KEY(id, version) prevents overwriting."
                ]
            }
        },
        {
            "id": "m3-l18",
            "title": "INSERT INTO — Adding Data",
            "subtitle": "Single rows, bulk inserts, and insert-or-replace patterns",
            "difficulty": "beginner",
            "business_context": "Loading data into a database is a daily task in analytics: importing CSV files, ingesting API responses, logging events. Python's sqlite3 module makes this fast with executemany() for bulk inserts and parameterized queries to handle any data safely.",
            "concept": {
                "theory": "INSERT INTO adds rows to a table. You can insert one row at a time or many at once with executemany(). INSERT OR REPLACE (UPSERT) handles the case where a row might already exist — it replaces it instead of failing. INSERT OR IGNORE silently skips duplicate rows without raising an error.",
                "business_angle": "In real workflows, you'll insert thousands of rows from CSV files or API calls. executemany() with a list of tuples is 10-100x faster than looping with individual execute() calls. Always use parameterized inserts (? placeholders) — never format SQL strings with user data.",
                "worked_example_intro": "We'll insert data in all the common patterns: single row, bulk with executemany, and upsert with INSERT OR REPLACE.",
                "key_insight": "executemany() sends all rows in a single database transaction, which is dramatically faster than individual inserts inside a loop. For 10,000 rows, executemany() takes milliseconds; a loop takes seconds."
            },
            "worked_example": """import sqlite3, time

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER DEFAULT 0)')

# 1. Single row insert
cur.execute('INSERT INTO products(name, price) VALUES (?, ?)', ('Laptop', 999.99))
print('Single insert done')

# 2. Bulk insert with executemany (fast!)
bulk_data = [
    ('Mouse', 29.99, 150), ('Keyboard', 79.99, 80),
    ('Monitor', 399.99, 40), ('Webcam', 89.99, 60),
    ('Headset', 59.99, 90),
]
cur.executemany('INSERT INTO products(name, price, stock) VALUES (?, ?, ?)', bulk_data)
print(f'Bulk inserted {len(bulk_data)} rows')

# 3. INSERT OR IGNORE — skip if PK conflict
cur.execute('INSERT OR IGNORE INTO products(id, name, price) VALUES (1, "Laptop V2", 1099)')
print(f'After OR IGNORE — Laptop name: {cur.execute("SELECT name FROM products WHERE id=1").fetchone()[0]}')

# 4. INSERT OR REPLACE — overwrite if PK conflict
cur.execute('INSERT OR REPLACE INTO products(id, name, price) VALUES (1, "Pro Laptop", 1199)')
print(f'After OR REPLACE — Laptop name: {cur.execute("SELECT name FROM products WHERE id=1").fetchone()[0]}')

# 5. Performance: executemany vs loop
import timeit
conn2 = sqlite3.connect(':memory:')
conn2.execute('CREATE TABLE t (id INTEGER, val REAL)')
data = [(i, i*1.5) for i in range(10000)]
t1 = timeit.timeit(lambda: conn2.executemany('INSERT INTO t VALUES(?,?)', data), number=1)
conn2.execute('DELETE FROM t')
t2 = timeit.timeit(lambda: [conn2.execute('INSERT INTO t VALUES(?,?)', r) for r in data], number=1)
print(f'\\nexecutemany: {t1:.3f}s | loop: {t2:.3f}s | {t2/t1:.0f}x faster')
conn.close(); conn2.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "cur.execute('INSERT INTO t(a,b) VALUES(?,?)', (val_a, val_b))",
                        "cur.executemany('INSERT INTO t VALUES(?,?)', list_of_tuples)",
                        "INSERT OR IGNORE INTO t VALUES(...)  -- skip on conflict",
                        "INSERT OR REPLACE INTO t VALUES(...)  -- overwrite on conflict"
                    ],
                    "notes": "Always use ? placeholders. Never: f'INSERT INTO t VALUES ({user_input})' — this is a SQL injection vulnerability."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Which is fastest for inserting 50,000 rows from a Python list?", "options": ["for row in data: cur.execute(...)", "cur.executemany(..., data)", "pandas df.to_sql(...)", "Both B and C are fast; A is slow"], "answer": 3, "explanation": "executemany() and pandas to_sql() both batch operations efficiently. A plain for-loop calling execute() on each row is dramatically slower because it creates 50,000 separate database roundtrips instead of one."},
                    {"type": "true_false", "question": "INSERT OR IGNORE will raise an error if a duplicate primary key is inserted.", "answer": False, "explanation": "INSERT OR IGNORE silently skips the insert when there's a constraint violation (like a duplicate PK or UNIQUE column). It does NOT raise an error — use it when you want to load data without caring about duplicates."},
                    {"type": "fill_blank", "question": "To insert many rows efficiently: cur.___(\"INSERT INTO t VALUES(?,?)\", list_of_tuples)", "template": "cur.___('INSERT INTO t VALUES(?,?)', list_of_tuples)", "answer": "executemany", "explanation": "executemany() takes a SQL string and an iterable of parameter tuples. It executes the statement once per tuple but handles all of them in one efficient database operation."}
                ]
            },
            "challenge": {
                "instructions": "Load a CSV-style dataset (provided as a list of dicts) into SQLite using executemany(). Handle potential duplicate records using INSERT OR IGNORE. Then show a count of rows per category.",
                "starter_code": """import sqlite3

# Simulated CSV data (as if read from a file)
csv_rows = [
    {'id':1,'name':'Widget A','category':'Tools','price':15.99},
    {'id':2,'name':'Widget B','category':'Tools','price':22.50},
    {'id':3,'name':'Gadget X','category':'Electronics','price':89.99},
    {'id':4,'name':'Gadget Y','category':'Electronics','price':124.00},
    {'id':5,'name':'Widget A','category':'Tools','price':15.99},  # duplicate id=1
    {'id':6,'name':'Supply Z','category':'Office','price':8.75},
]

conn = sqlite3.connect(':memory:')
cur = conn.cursor()

# Create products table

# Convert list of dicts to list of tuples
# Use INSERT OR IGNORE to skip the duplicate

print(f'Rows inserted: {cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]}')

print('\\n=== Count by Category ===')
# GROUP BY category

conn.close()""",
                "tests": [{"type": "code_contains", "value": "executemany"}, {"type": "output_contains", "value": "Tools"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
csv_rows = [{'id':1,'name':'Widget A','category':'Tools','price':15.99},{'id':2,'name':'Widget B','category':'Tools','price':22.50},{'id':3,'name':'Gadget X','category':'Electronics','price':89.99},{'id':4,'name':'Gadget Y','category':'Electronics','price':124.00},{'id':5,'name':'Widget A','category':'Tools','price':15.99},{'id':6,'name':'Supply Z','category':'Office','price':8.75}]
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
tuples = [(r['id'],r['name'],r['category'],r['price']) for r in csv_rows]
cur.executemany('INSERT OR IGNORE INTO products VALUES(?,?,?,?)', tuples)
print(f'Rows inserted: {cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]}')
print('\\n=== Count by Category ===')
for r in cur.execute('SELECT category, COUNT(*) as cnt, ROUND(AVG(price),2) as avg_price FROM products GROUP BY category ORDER BY cnt DESC'):
    print(f"  {r[0]}: {r[1]} products | avg ${r[2]}")
conn.close()""",
                "challenge_variations": [
                    "Read a real CSV file using Python's csv module and insert all rows into SQLite with executemany().",
                    "Insert JSON API response data (list of dicts) into SQLite. Use INSERT OR REPLACE to update existing records.",
                    "Batch insert 100,000 rows and compare performance: executemany() vs. executemany() inside with conn: (transaction).",
                    "Use INSERT INTO ... SELECT to copy rows from one table to another with a filter.",
                    "Insert rows with a generated column: INSERT with CURRENT_TIMESTAMP as the value for a timestamp column.",
                    "Load a pandas DataFrame into SQLite using df.to_sql() and compare with manual executemany().",
                    "Build a deduplication pipeline: load all rows, use INSERT OR IGNORE to skip duplicates, report how many were skipped.",
                    "Insert rows incrementally: only insert new records that don't already exist using INSERT WHERE NOT EXISTS.",
                    "Use Python's pathlib to read a .csv file and bulk-insert every row — handle header row separately.",
                    "Implement an upsert: INSERT OR REPLACE that updates price and stock but keeps the original created_at timestamp."
                ]
            }
        },
        {
            "id": "m3-l19",
            "title": "UPDATE & DELETE — Modifying Existing Data",
            "subtitle": "Always use WHERE — or you'll change every row",
            "difficulty": "beginner",
            "business_context": "Prices change. Customers move. Products get discontinued. UPDATE and DELETE are how you keep data current — but a missing WHERE clause is one of the most common (and costly) mistakes in SQL. One wrong UPDATE can corrupt an entire table.",
            "concept": {
                "theory": "UPDATE changes values in existing rows. DELETE removes rows. Both support WHERE to target specific rows — without WHERE, the operation applies to EVERY row in the table. Transactions (BEGIN/COMMIT/ROLLBACK) let you wrap updates in a safety net: if something goes wrong, ROLLBACK undoes everything.",
                "business_angle": "Safe update patterns are critical: always SELECT before UPDATE to verify your WHERE clause selects the right rows. Use transactions for multi-step updates (e.g., transfer funds: debit one account, credit another — both must succeed or both must fail).",
                "worked_example_intro": "We'll update prices, deactivate records, delete rows, and use a transaction to safely transfer inventory.",
                "key_insight": "Before running UPDATE or DELETE, run the equivalent SELECT with the same WHERE clause first. If the SELECT returns the right rows, your UPDATE/DELETE will affect those exact rows. This preview habit prevents disasters."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, active INTEGER DEFAULT 1)')
cur.executemany('INSERT INTO products VALUES(?,?,?,?)',[(1,'Laptop',999,1),(2,'Mouse',29,1),(3,'Keyboard',79,1),(4,'Old Widget',5,1)])

print('=== Before updates ===')
for r in cur.execute('SELECT id, name, price, active FROM products'):
    print(f"  {r[0]}. {r[1]:<12} ${r[2]:.2f} active={r[3]}")

# UPDATE with WHERE (targeted)
cur.execute('UPDATE products SET price = price * 1.10 WHERE name LIKE "%Laptop%"')
print('\\nLaptop price increased 10%')

# UPDATE multiple columns
cur.execute('UPDATE products SET price = 0.01, active = 0 WHERE id = 4')
print('Widget discontinued')

# Preview DELETE before running it
candidates = cur.execute('SELECT id, name FROM products WHERE active = 0').fetchall()
print(f'\\nWould delete: {candidates}')

# DELETE with WHERE
cur.execute('DELETE FROM products WHERE active = 0')
print('Inactive products deleted')

# Transaction: safe multi-step update
cur.execute('CREATE TABLE inventory (product_id INTEGER, warehouse TEXT, qty INTEGER)')
cur.executemany('INSERT INTO inventory VALUES(?,?,?)',[(1,'East',100),(1,'West',50)])
try:
    conn.execute('BEGIN')
    conn.execute('UPDATE inventory SET qty = qty - 20 WHERE product_id=1 AND warehouse="East"')
    conn.execute('UPDATE inventory SET qty = qty + 20 WHERE product_id=1 AND warehouse="West"')
    conn.execute('COMMIT')
    print('\\nInventory transfer committed')
except Exception as e:
    conn.execute('ROLLBACK')
    print(f'Transfer rolled back: {e}')

print('\\n=== After all changes ===')
for r in cur.execute('SELECT id, name, price FROM products'):
    print(f"  {r[0]}. {r[1]:<12} ${r[2]:.2f}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "UPDATE table SET col = val WHERE condition",
                        "DELETE FROM table WHERE condition",
                        "conn.execute('BEGIN') / COMMIT / ROLLBACK",
                        "Run SELECT with same WHERE first to preview affected rows"
                    ],
                    "notes": "UPDATE without WHERE modifies ALL rows. DELETE without WHERE removes ALL rows. Always double-check your WHERE clause."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "You run: UPDATE employees SET salary = 0. What happens?", "options": ["Only employees with salary=0 are affected","Nothing — UPDATE requires a WHERE clause","All employees get salary set to 0","SQL error: missing WHERE"], "answer": 2, "explanation": "Without WHERE, UPDATE modifies every row in the table. This is valid SQL — just catastrophic if unintentional. Always verify with a SELECT first."},
                    {"type": "true_false", "question": "ROLLBACK undoes all changes made since the last BEGIN (or connection open if no explicit BEGIN).", "answer": True, "explanation": "ROLLBACK reverses all changes in the current transaction back to the last COMMIT or BEGIN point. This is your 'undo' for database operations. conn.execute('ROLLBACK') in Python triggers it."},
                    {"type": "fill_blank", "question": "To safely transfer: first run a ___ with the same WHERE clause to preview which rows will be affected.", "template": "Run a ___ with the same WHERE to preview affected rows before UPDATE/DELETE.", "answer": "SELECT", "explanation": "The preview SELECT habit: before UPDATE products SET price=0 WHERE category='Tools', first run SELECT * FROM products WHERE category='Tools' to confirm you're targeting the right rows."}
                ]
            },
            "challenge": {
                "instructions": "Manage a product catalog: (1) Apply a 15% price increase to all 'Premium' products, (2) Discontinue (set active=0) any product with 0 stock, (3) Delete discontinued products older than 2023, (4) Use a transaction to atomically move 50 units between two warehouses. Print the catalog before and after.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, tier TEXT, price REAL, stock INTEGER, active INTEGER DEFAULT 1, added_year INTEGER)')
cur.execute('CREATE TABLE inventory (product_id INTEGER, location TEXT, qty INTEGER)')
cur.executemany('INSERT INTO products VALUES(?,?,?,?,?,?,?)', [
    (1,'Pro Headset','Premium',120,30,1,2024),(2,'Basic Cable','Standard',8,0,1,2022),
    (3,'Pro Keyboard','Premium',200,15,1,2024),(4,'Old Stand','Standard',20,0,1,2021),
])
cur.executemany('INSERT INTO inventory VALUES(?,?,?)', [(1,'East',100),(1,'West',50)])

print('=== BEFORE ===')
for r in cur.execute('SELECT id,name,price,stock,active FROM products'):
    print(f"  {r[0]}. {r[1]:<14} ${r[2]:.2f} stock={r[3]} active={r[4]}")

# 1. 15% price increase for Premium tier

# 2. Discontinue zero-stock products

# 3. Delete discontinued products added before 2023

# 4. Move 50 units East→West in a transaction

print('\\n=== AFTER ===')
for r in cur.execute('SELECT id,name,price,stock,active FROM products'):
    print(f"  {r[0]}. {r[1]:<14} ${r[2]:.2f} stock={r[3]} active={r[4]}")
print('\\n=== Inventory ===')
for r in cur.execute('SELECT location, qty FROM inventory WHERE product_id=1'):
    print(f"  {r[0]}: {r[1]} units")
conn.close()""",
                "tests": [{"type": "code_contains", "value": "UPDATE"}, {"type": "code_contains", "value": "DELETE"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, tier TEXT, price REAL, stock INTEGER, active INTEGER DEFAULT 1, added_year INTEGER)')
cur.execute('CREATE TABLE inventory (product_id INTEGER, location TEXT, qty INTEGER)')
cur.executemany('INSERT INTO products VALUES(?,?,?,?,?,?,?)',[(1,'Pro Headset','Premium',120,30,1,2024),(2,'Basic Cable','Standard',8,0,1,2022),(3,'Pro Keyboard','Premium',200,15,1,2024),(4,'Old Stand','Standard',20,0,1,2021)])
cur.executemany('INSERT INTO inventory VALUES(?,?,?)',[(1,'East',100),(1,'West',50)])
print('=== BEFORE ===')
for r in cur.execute('SELECT id,name,price,stock,active FROM products'):print(f"  {r[0]}. {r[1]:<14} ${r[2]:.2f} stock={r[3]} active={r[4]}")
cur.execute("UPDATE products SET price = ROUND(price * 1.15, 2) WHERE tier = 'Premium'")
cur.execute("UPDATE products SET active = 0 WHERE stock = 0")
cur.execute("DELETE FROM products WHERE active = 0 AND added_year < 2023")
conn.execute('BEGIN')
conn.execute("UPDATE inventory SET qty = qty - 50 WHERE product_id=1 AND location='East'")
conn.execute("UPDATE inventory SET qty = qty + 50 WHERE product_id=1 AND location='West'")
conn.execute('COMMIT')
print('\\n=== AFTER ===')
for r in cur.execute('SELECT id,name,price,stock,active FROM products'):print(f"  {r[0]}. {r[1]:<14} ${r[2]:.2f} stock={r[3]} active={r[4]}")
print('\\n=== Inventory ===')
for r in cur.execute('SELECT location, qty FROM inventory WHERE product_id=1'):print(f"  {r[0]}: {r[1]} units")
conn.close()""",
                "challenge_variations": [
                    "Safely archive old orders: INSERT INTO orders_archive SELECT * FROM orders WHERE date < '2023-01-01', then DELETE the originals in a transaction.",
                    "Update employee titles based on years of service using a CASE expression in UPDATE SET.",
                    "Implement a 'soft delete' pattern: instead of DELETE, set deleted_at = CURRENT_TIMESTAMP and filter WHERE deleted_at IS NULL.",
                    "Run a rollback scenario: simulate a failed payment transfer and verify the transaction was rolled back correctly.",
                    "Use UPDATE with a subquery: UPDATE products SET price = price * 1.05 WHERE id IN (SELECT product_id FROM top_sellers).",
                    "Bulk update 10,000 rows using executemany() with UPDATE — benchmark vs. individual execute() calls.",
                    "Implement optimistic locking: add a version column, increment on every UPDATE, reject if version doesn't match expected.",
                    "DELETE with JOIN (SQLite syntax): DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE status='cancelled').",
                    "Track data changes: create an audit_log table and use Python to INSERT a log entry whenever you UPDATE a record.",
                    "Simulate a point-of-sale system: UPDATE stock (decrement), INSERT sales record, all in one transaction."
                ]
            }
        },
        {
            "id": "m3-l20",
            "title": "Python + SQLite — Connecting Code to Data",
            "subtitle": "The sqlite3 module: connections, cursors, and fetching results",
            "difficulty": "beginner",
            "business_context": "Every data pipeline, web app, and analytics script needs to talk to a database. Python's built-in sqlite3 module is your bridge — no installation required, works on any machine, and the patterns transfer directly to PostgreSQL, MySQL, and other production databases.",
            "concept": {
                "theory": "sqlite3 workflow: (1) connect with sqlite3.connect(), (2) get a cursor with conn.cursor(), (3) execute SQL with cur.execute() or executemany(), (4) fetch results with fetchone() / fetchall() / fetchmany(n), (5) commit changes with conn.commit(), (6) close with conn.close(). Context managers (with conn:) handle commit/close automatically.",
                "business_angle": "The same sqlite3 patterns apply to any relational database via different drivers: psycopg2 for PostgreSQL, pymysql for MySQL, pyodbc for SQL Server. Master sqlite3 and you've mastered the interface for all of them.",
                "worked_example_intro": "We'll build a complete Python + SQLite workflow with best practices: context managers, parameterized queries, and result iteration.",
                "key_insight": "Use 'with sqlite3.connect(...) as conn:' — this auto-commits on success or rolls back on exception, and closes the connection. Always iterate over cursor results directly (for row in cursor) instead of fetchall() for large result sets, to avoid loading millions of rows into memory."
            },
            "worked_example": """import sqlite3

DB_PATH = ':memory:'  # use 'mydb.sqlite' for a real file

# Best practice: context manager handles commit/rollback/close
with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row   # makes rows dict-like: row['name'] instead of row[0]
    cur = conn.cursor()

    cur.execute('''CREATE TABLE employees (
        id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary REAL)''')
    cur.executemany('INSERT INTO employees VALUES(?,?,?,?)', [
        (1,'Alice','Engineering',115000),(2,'Bob','Marketing',72000),
        (3,'Carol','Engineering',98000),(4,'Dave','Sales',85000),
    ])

    # fetchone() — single row
    row = cur.execute('SELECT * FROM employees WHERE id = 1').fetchone()
    print(f"fetchone: {row['name']} — ${row['salary']:,.0f}")

    # fetchall() — all rows as a list (careful with huge tables!)
    rows = cur.execute('SELECT name, salary FROM employees ORDER BY salary DESC').fetchall()
    print(f"\\nfetchall ({len(rows)} rows):")
    for r in rows:
        print(f"  {r['name']}: ${r['salary']:,.0f}")

    # Iterate directly — memory-efficient for large results
    print("\\nDirect iteration:")
    for r in cur.execute('SELECT dept, COUNT(*) n, AVG(salary) avg FROM employees GROUP BY dept'):
        print(f"  {r['dept']}: {r['n']} people | avg ${r['avg']:,.0f}")

    # fetchmany(n) — process in batches
    cur.execute('SELECT id, name FROM employees')
    batch = cur.fetchmany(2)
    print(f"\\nBatch of 2: {[r['name'] for r in batch]}")

    # Row count after INSERT/UPDATE/DELETE
    cur.execute('UPDATE employees SET salary = salary * 1.05 WHERE dept = ?', ('Engineering',))
    print(f"\\nRows updated: {cur.rowcount}")

# Connection closed automatically when 'with' block exits
print("Connection closed.")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "conn = sqlite3.connect('file.db')  -- or ':memory:'",
                        "conn.row_factory = sqlite3.Row  -- dict-like rows",
                        "cur.fetchone() / cur.fetchall() / cur.fetchmany(n)",
                        "cur.rowcount  -- rows affected by last INSERT/UPDATE/DELETE",
                        "with sqlite3.connect(db) as conn:  -- auto-commit/rollback"
                    ],
                    "notes": "':memory:' creates an in-memory database — great for testing. For production, use a file path like 'data/myapp.db'."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "What does conn.row_factory = sqlite3.Row enable?", "options": ["Faster queries","Accessing columns by name: row['salary'] instead of row[0]","Automatic connection pooling","JSON output format"], "answer": 1, "explanation": "sqlite3.Row makes each result row dict-like AND index-accessible. row['salary'] is much more readable than row[2] when you have many columns. It also supports iteration and len()."},
                    {"type": "true_false", "question": "fetchall() loads all result rows into memory at once.", "answer": True, "explanation": "fetchall() returns a Python list containing every result row. For tables with millions of rows, this can exhaust memory. Use direct iteration (for row in cursor) or fetchmany(n) for large results."},
                    {"type": "fill_blank", "question": "To get the number of rows affected by an UPDATE, check: cur.___", "template": "cur.___  # rows affected by last INSERT/UPDATE/DELETE", "answer": "rowcount", "explanation": "cur.rowcount returns the number of rows modified by the most recent execute() call. It's 0 if no rows matched the WHERE clause, -1 if the database couldn't determine the count."}
                ]
            },
            "challenge": {
                "instructions": "Build a complete 'inventory manager' using Python + SQLite. Use row_factory for named column access. Functions: add_product(), update_stock(), get_low_stock(threshold). All using parameterized queries. Print a low-stock report.",
                "starter_code": """import sqlite3

def get_conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    return conn

def setup_db(conn):
    conn.execute('''CREATE TABLE products (
        id INTEGER PRIMARY KEY, name TEXT, category TEXT, stock INTEGER, reorder_point INTEGER)''')
    conn.executemany('INSERT INTO products VALUES(?,?,?,?,?)', [
        (1,'Laptop','Electronics',5,10),(2,'Mouse','Electronics',50,20),
        (3,'Paper','Office',200,50),(4,'Pens','Office',8,25),(5,'Monitor','Electronics',3,5),
    ])
    conn.commit()

def add_product(conn, name, category, stock, reorder_point):
    # INSERT new product, return its id
    pass

def update_stock(conn, product_id, qty_change):
    # UPDATE stock by qty_change (positive=restock, negative=sold)
    pass

def get_low_stock(conn, threshold=None):
    # Return products where stock <= their reorder_point (or <= threshold)
    pass

conn = get_conn()
setup_db(conn)

add_product(conn, 'Keyboard', 'Electronics', 15, 10)
update_stock(conn, 1, -3)   # sold 3 laptops
update_stock(conn, 2, 100)  # restocked 100 mice

print('=== Low Stock Alert ===')
for row in get_low_stock(conn):
    print(f"  {row['name']:<12} stock={row['stock']} | reorder at {row['reorder_point']}")

conn.close()""",
                "tests": [{"type": "code_contains", "value": "row_factory"}, {"type": "code_contains", "value": "fetchall"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
def get_conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    return conn
def setup_db(conn):
    conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, stock INTEGER, reorder_point INTEGER)')
    conn.executemany('INSERT INTO products VALUES(?,?,?,?,?)',[(1,'Laptop','Electronics',5,10),(2,'Mouse','Electronics',50,20),(3,'Paper','Office',200,50),(4,'Pens','Office',8,25),(5,'Monitor','Electronics',3,5)])
    conn.commit()
def add_product(conn, name, category, stock, reorder_point):
    cur = conn.execute('INSERT INTO products(name,category,stock,reorder_point) VALUES(?,?,?,?)',(name,category,stock,reorder_point))
    conn.commit()
    return cur.lastrowid
def update_stock(conn, product_id, qty_change):
    conn.execute('UPDATE products SET stock = stock + ? WHERE id = ?',(qty_change, product_id))
    conn.commit()
def get_low_stock(conn, threshold=None):
    if threshold:
        return conn.execute('SELECT * FROM products WHERE stock <= ?',(threshold,)).fetchall()
    return conn.execute('SELECT * FROM products WHERE stock <= reorder_point ORDER BY stock').fetchall()
conn = get_conn()
setup_db(conn)
add_product(conn,'Keyboard','Electronics',15,10)
update_stock(conn,1,-3)
update_stock(conn,2,100)
print('=== Low Stock Alert ===')
for row in get_low_stock(conn):
    print(f"  {row['name']:<12} stock={row['stock']} | reorder at {row['reorder_point']}")
conn.close()""",
                "challenge_variations": [
                    "Build a contact book app: add_contact(), search_by_name(), delete_contact() using sqlite3.",
                    "Create a logging function that writes all queries to an audit table with timestamp and user.",
                    "Connect to a real .sqlite file, insert 10,000 rows, then query them — use context manager.",
                    "Build a sqlite3 connection pool (list of connections) and demonstrate reuse.",
                    "Convert all results to pandas DataFrames using pd.read_sql_query(sql, conn).",
                    "Implement a pagination function: get_page(conn, page_num, page_size) using LIMIT and OFFSET.",
                    "Build a CSV importer: read a .csv file with Python csv module and insert rows using executemany().",
                    "Write a backup function that copies a SQLite database to a timestamped file.",
                    "Use sqlite3.connect() with check_same_thread=False for multi-threaded access and demonstrate thread safety.",
                    "Profile query performance: use time.perf_counter() around execute() calls to identify slow queries."
                ]
            }
        },
        {
            "id": "m3-l21",
            "title": "Parameterized Queries — Safe SQL from Python",
            "subtitle": "Never build SQL from user input — always use ? placeholders",
            "difficulty": "beginner",
            "business_context": "A hacker enters '; DROP TABLE users; --' in your search box. If you built SQL by string concatenation, that table is gone. Parameterized queries completely prevent this — the single most important database security practice.",
            "concept": {
                "theory": "SQL injection occurs when untrusted data embeds into SQL strings. Parameterized queries separate SQL structure from data values — the database driver handles escaping safely. In sqlite3, use ? for positional parameters or :name for named parameters.",
                "business_angle": "SQL injection is consistently OWASP's #1 web vulnerability. Parameterized queries cost nothing to use and prevent entire classes of attacks. This is non-negotiable in professional code.",
                "worked_example_intro": "We'll show the dangerous string-format pattern, then the correct approach with both ? and :name syntax.",
                "key_insight": "The ? placeholder tells the database: treat this as data, not SQL code. Even if input contains quotes, semicolons, or DROP TABLE, it cannot alter the SQL structure."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)')
cur.executemany('INSERT INTO users VALUES(?,?,?)',[(1,'Alice','admin'),(2,'Bob','user'),(3,'Carol','user')])

# DANGEROUS (never do this):
# user_input = "alice' OR '1'='1"
# cur.execute(f"SELECT * FROM users WHERE name = '{user_input}'")  # INJECTION!

# SAFE: positional parameter
injection = "alice' OR '1'='1"
result = cur.execute('SELECT * FROM users WHERE name = ?', (injection,)).fetchall()
print(f'Injection attempt returned {len(result)} rows (blocked!)')

# Legitimate search
alice = cur.execute('SELECT id, name, role FROM users WHERE name = ?', ('Alice',)).fetchone()
print(f'Legitimate: {alice}')

# Named parameters (:name syntax)
params = {'role': 'admin', 'min_id': 1}
for r in cur.execute('SELECT name FROM users WHERE role = :role AND id >= :min_id', params):
    print(f'Named param result: {r[0]}')

# Bulk parameterized insert
new_users = [('Dave','user'),('Eve','admin')]
cur.executemany('INSERT INTO users(name,role) VALUES(?,?)', new_users)
print(f'Total users: {cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]}')
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "cur.execute('SELECT * FROM t WHERE col = ?', (value,))",
                        "cur.execute('SELECT * FROM t WHERE col = :name', {'name': value})",
                        "NEVER: f\"SELECT ... WHERE x = '{user_input}'\"  -- injection risk",
                        "Single-element tuple: (value,) — the comma is required!"
                    ],
                    "notes": "? is positional (order matters). :name is named (dict keys). Both are equally safe."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "SQL injection can allow an attacker to:", "options": ["Only read data they shouldn't see","Read, modify, or delete any data in the database","Only slow down queries","Only affects MySQL, not SQLite"], "answer": 1, "explanation": "SQL injection allows running arbitrary SQL — reading all data, modifying records, deleting tables. Parameterized queries prevent this entirely by treating all input as data, never as SQL code."},
                    {"type": "true_false", "question": "cur.execute('SELECT * FROM t WHERE id = ?', (user_id,)) is safe even if user_id contains malicious SQL.", "answer": True, "explanation": "The ? placeholder means the database treats the value as pure data regardless of its content. Even if user_id = '1 OR 1=1', the query only looks for a row where id literally equals that string."},
                    {"type": "fill_blank", "question": "Pass a single parameter: cur.execute('SELECT * FROM t WHERE id = ?', ___)", "template": "cur.execute('SELECT * FROM t WHERE id = ?', ___)", "answer": "(user_id,)", "explanation": "sqlite3 requires an iterable. For one parameter: (value,) with a trailing comma. Without the comma, (value) is just parentheses around a value, not a tuple — you'll get a TypeError."}
                ]
            },
            "challenge": {
                "instructions": "Build a safe search function for products. Accept category (optional) and price range parameters. Demonstrate that SQL injection input returns 0 rows while legitimate searches work. Use only parameterized queries.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)')
cur.executemany('INSERT INTO products VALUES(?,?,?,?)',[(1,'Laptop','Electronics',999),(2,'Mouse','Electronics',29),(3,'Desk','Furniture',350),(4,'Chair','Furniture',250)])

def search_products(conn, category=None, min_price=0, max_price=99999):
    # Return list of (name, category, price) using ? placeholders
    pass

# Legitimate search
print(search_products(conn, category='Electronics', max_price=100))

# Injection attempt — should return []
print(search_products(conn, category="Electronics' OR '1'='1"))
conn.close()""",
                "tests": [{"type": "code_contains", "value": "?"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)')
cur.executemany('INSERT INTO products VALUES(?,?,?,?)',[(1,'Laptop','Electronics',999),(2,'Mouse','Electronics',29),(3,'Desk','Furniture',350),(4,'Chair','Furniture',250)])
def search_products(conn, category=None, min_price=0, max_price=99999):
    if category:
        return conn.execute('SELECT name,category,price FROM products WHERE category=? AND price BETWEEN ? AND ?',(category,min_price,max_price)).fetchall()
    return conn.execute('SELECT name,category,price FROM products WHERE price BETWEEN ? AND ?',(min_price,max_price)).fetchall()
print(search_products(conn, category='Electronics', max_price=100))
print(search_products(conn, category="Electronics' OR '1'='1"))
conn.close()""",
                "challenge_variations": [
                    "Build a safe login: verify username AND password with parameterized query — show injection doesn't bypass it.",
                    "Create a search function that accepts a list of IDs and safely uses IN with executemany-style querying.",
                    "Use named :name parameters for a multi-filter query with department, min_salary, max_salary.",
                    "Demonstrate safe LIKE search: LIKE ? with value = '%' + search_term + '%'.",
                    "Write unit tests proving injection attempts return empty results.",
                    "Build a dynamic WHERE clause that safely adds conditions from a dict of filters.",
                    "Show the performance difference between a parameterized query called 10,000 times vs 10,000 formatted strings.",
                    "Sanitize ORDER BY direction using a Python allowlist (ORDER BY can't be parameterized — explain why).",
                    "Create a query logger decorator that records the SQL and parameters (not the injected value) to an audit table.",
                    "Show how RETURNING clause works in SQLite 3.35+: INSERT INTO t VALUES(?) RETURNING id — all parameterized."
                ]
            }
        },
        {
            "id": "m3-l22",
            "title": "SQLAlchemy — Python Objects Meet SQL Tables",
            "subtitle": "The industry-standard ORM: define tables as classes, query with Python",
            "difficulty": "advanced",
            "business_context": "Professional Python apps rarely write raw SQL strings. SQLAlchemy's ORM (Object-Relational Mapper) lets you define database tables as Python classes and rows as objects. Flask, FastAPI, and most enterprise Python apps use SQLAlchemy under the hood.",
            "concept": {
                "theory": "An ORM maps Python classes to database tables and instances to rows. SQLAlchemy's declarative ORM: define a class inheriting from Base, declare columns as class attributes, use Session to add/query/delete. SQLAlchemy generates SQL for you from Python method chains.",
                "business_angle": "ORMs speed development: no manual CREATE TABLE SQL, no column mapping, built-in relationship traversal. The tradeoff: complex analytics queries are sometimes clearer in raw SQL. Production code often mixes both.",
                "worked_example_intro": "We'll define models for a task tracker, insert and update records using ORM style, then query with filters and relationships.",
                "key_insight": "session.add() stages the change in memory. session.commit() writes to the database. session.query(Model).filter(condition).all() is SELECT ... WHERE. Relationships let you navigate: order.customer.name without writing a JOIN."
            },
            "worked_example": """from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')

class Customer(Base):
    __tablename__ = 'customers'
    id     = Column(Integer, primary_key=True)
    name   = Column(String, nullable=False)
    city   = Column(String)
    orders = relationship('Order', back_populates='customer')

class Order(Base):
    __tablename__ = 'orders'
    id          = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product     = Column(String)
    amount      = Column(Float)
    customer    = relationship('Customer', back_populates='orders')

Base.metadata.create_all(engine)

with Session(engine) as session:
    c1 = Customer(name='Alice', city='NYC')
    c2 = Customer(name='Bob',   city='LA')
    session.add_all([c1, c2])
    session.flush()  # assigns IDs without committing

    session.add_all([
        Order(customer_id=c1.id, product='Laptop', amount=999),
        Order(customer_id=c1.id, product='Mouse',  amount=29),
        Order(customer_id=c2.id, product='Keyboard', amount=79),
    ])
    session.commit()

    print('=== All customers with order count ===')
    for c in session.query(Customer).order_by(Customer.name):
        print(f"  {c.name} ({c.city}): {len(c.orders)} orders")

    print('\\n=== Orders over $50 (ORM filter) ===')
    for o in session.query(Order).filter(Order.amount > 50):
        print(f"  {o.customer.name}: {o.product} ${o.amount}")

    # Raw SQL when ORM gets complex
    from sqlalchemy import text
    result = session.execute(text('SELECT c.name, SUM(o.amount) FROM customers c JOIN orders o ON c.id=o.customer_id GROUP BY c.name')).fetchall()
    print('\\n=== Revenue (raw SQL via SQLAlchemy) ===')
    for r in result:
        print(f"  {r[0]}: ${r[1]:.0f}")""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "class Model(Base): __tablename__ = '...'; col = Column(type, ...)",
                        "Base.metadata.create_all(engine)  -- creates tables",
                        "session.add(obj); session.commit()",
                        "session.query(Model).filter(Model.col == val).all()",
                        "relationship('OtherModel', back_populates='...')  -- navigate between objects"
                    ],
                    "notes": "SQLAlchemy 2.0 uses select(Model).where() style. session.query() is 1.x style — both work, 2.0 is preferred in new projects."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "What does Base.metadata.create_all(engine) do?", "options": ["Drops all tables","Creates all tables defined as Base subclasses","Inserts sample data","Validates the schema"], "answer": 1, "explanation": "create_all() inspects all classes inheriting from Base and runs CREATE TABLE IF NOT EXISTS for each one. It's the SQLAlchemy equivalent of running all your CREATE TABLE statements manually."},
                    {"type": "true_false", "question": "session.add() immediately writes the record to the database.", "answer": False, "explanation": "session.add() stages the object in memory within the session. The SQL INSERT runs on session.flush() or session.commit(). You can rollback any time before committing."},
                    {"type": "fill_blank", "question": "Filter orders with amount > 100: session.query(Order).___(Order.amount > 100).all()", "template": "session.query(Order).___(Order.amount > 100).all()", "answer": "filter", "explanation": "filter() is SQLAlchemy's WHERE clause. Use Python comparison operators: == for equality, > < >= <=, .in_([vals]) for IN. Chain multiple filters: .filter(A).filter(B) or .filter(A, B)."}
                ]
            },
            "challenge": {
                "instructions": "Build a SQLAlchemy library system: Book (title, author, available=True) and Loan (book_id FK, borrower, date). Insert 5 books, check out 2, query available books and current loans via relationships.",
                "starter_code": """from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')

# Define Book and Loan models

Base.metadata.create_all(engine)

with Session(engine) as session:
    # Add 5 books, check out 2 (available=False + Loan record)
    session.commit()

    print('=== Available Books ===')
    # Query available=True books

    print('\\n=== Current Loans ===')
    # Query loans and access book.title via relationship
""",
                "tests": [{"type": "code_contains", "value": "Column"}, {"type": "code_contains", "value": "relationship"}, {"type": "runs_without_error"}],
                "solution": """from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
class Book(Base):
    __tablename__='books'
    id=Column(Integer,primary_key=True); title=Column(String); author=Column(String); available=Column(Boolean,default=True)
    loans=relationship('Loan',back_populates='book')
class Loan(Base):
    __tablename__='loans'
    id=Column(Integer,primary_key=True); book_id=Column(Integer,ForeignKey('books.id')); borrower=Column(String)
    book=relationship('Book',back_populates='loans')
Base.metadata.create_all(engine)
with Session(engine) as session:
    books=[Book(title='1984',author='Orwell'),Book(title='Dune',author='Herbert'),Book(title='Foundation',author='Asimov'),Book(title='Neuromancer',author='Gibson'),Book(title='Snow Crash',author='Stephenson')]
    session.add_all(books); session.flush()
    books[0].available=False; books[2].available=False
    session.add_all([Loan(book_id=books[0].id,borrower='Alice'),Loan(book_id=books[2].id,borrower='Bob')])
    session.commit()
    print('=== Available Books ===')
    for b in session.query(Book).filter(Book.available==True): print(f"  {b.title} by {b.author}")
    print('\\n=== Current Loans ===')
    for l in session.query(Loan): print(f"  {l.borrower} has '{l.book.title}'")""",
                "challenge_variations": [
                    "Add a Category model and many-to-many relationship to Book via a bridge table.",
                    "Use session.query().join() for a joined ORM query without using raw SQL.",
                    "Implement soft delete: add deleted_at = Column(DateTime) and filter(deleted_at == None).",
                    "Export ORM query results to pandas: pd.read_sql(session.query(Book).statement, engine).",
                    "Add a hybrid_property: @hybrid_property def age(self): return 2024 - self.year.",
                    "Use SQLAlchemy events to auto-set created_at timestamp on insert.",
                    "Implement pagination: session.query(Book).offset(page*10).limit(10).",
                    "Connect to PostgreSQL by changing the connection string format (show the pattern).",
                    "Use session.merge() to upsert: insert if not exists, update if exists.",
                    "Write a test using SQLAlchemy with an in-memory database that rolls back after each test."
                ]
            }
        },
        {
            "id": "m3-l23",
            "title": "CASE, COALESCE & NULLIF — Conditional Logic in SQL",
            "subtitle": "Write if-else and NULL-handling logic directly in your queries",
            "difficulty": "intermediate",
            "business_context": "Your boss wants customers labeled 'VIP', 'Regular', or 'At Risk' based on spend. You could do this in Python post-fetch — or inside SQL with CASE. Keeping transformation logic in SQL means it runs at the database level, closer to the data.",
            "concept": {
                "theory": "CASE is SQL's if-else: CASE WHEN cond THEN val ... ELSE default END. COALESCE(a, b) returns the first non-NULL argument — standard NULL replacement. NULLIF(a, b) returns NULL if a equals b, preventing division-by-zero errors.",
                "business_angle": "These functions power classification (customer tiers, risk labels), NULL-safe math (COALESCE for totals), and safe percentages (NULLIF for denominators). They eliminate a whole class of Python post-processing.",
                "worked_example_intro": "We'll classify customer tiers, handle NULL spend with COALESCE, and compute safe conversion rates with NULLIF.",
                "key_insight": "NULLIF(denominator, 0) is the division-by-zero fix: it returns NULL when the denominator is 0. NULL divided by NULL gives NULL — no error. Wrap in COALESCE to show 0 or 'N/A' instead."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE customers (id INTEGER, name TEXT, spend REAL, last_order TEXT)')
cur.executemany('INSERT INTO customers VALUES(?,?,?,?)',[(1,'Alice',2500,'2024-03-01'),(2,'Bob',150,None),(3,'Carol',850,'2024-01-15'),(4,'Dave',0,None),(5,'Eve',5000,'2024-03-10'),(6,'Frank',None,None)])

print('=== Customer Tiers (CASE + COALESCE) ===')
for r in cur.execute('''
    SELECT name,
        COALESCE(spend, 0) AS safe_spend,
        CASE
            WHEN COALESCE(spend,0) >= 2000 THEN 'VIP'
            WHEN COALESCE(spend,0) >= 500  THEN 'Regular'
            WHEN COALESCE(spend,0) >  0    THEN 'New'
            ELSE 'Inactive'
        END AS tier,
        COALESCE(last_order, 'Never') AS last_order
    FROM customers ORDER BY safe_spend DESC
'''):
    print(f"  {r[0]:<8} ${r[1]:>6,.0f}  [{r[2]:<10}]  last: {r[3]}")

cur.execute('CREATE TABLE sales (rep TEXT, calls INTEGER, deals INTEGER)')
cur.executemany('INSERT INTO sales VALUES(?,?,?)',[('Ana',50,12),('Ben',0,0),('Cara',30,9)])

print('\\n=== Conversion Rate (NULLIF prevents /0) ===')
for r in cur.execute('''
    SELECT rep, calls, deals,
        ROUND(100.0 * deals / NULLIF(calls,0), 1) AS conv_pct
    FROM sales
'''):
    print(f"  {r[0]}: {r[2]}/{r[1]} = {r[3] or 'N/A'}%")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "CASE WHEN cond THEN val WHEN ... ELSE default END",
                        "COALESCE(col, fallback)  -- first non-NULL wins",
                        "NULLIF(a, b)  -- returns NULL if a=b, else a",
                        "ROUND(100.0 * n / NULLIF(d,0), 1)  -- safe %"
                    ],
                    "notes": "Use 100.0 (not 100) for decimal division. SQL integer division truncates: 5/2 = 2."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "COALESCE(discount, 0) when discount IS NULL returns:", "options": ["NULL","0","Error","discount"], "answer": 1, "explanation": "COALESCE returns the first non-NULL. When discount IS NULL, it falls through to 0. This is critical for math — NULL + 10 = NULL, so COALESCE(discount, 0) + 10 = 10 instead of NULL."},
                    {"type": "true_false", "question": "NULLIF(total, 0) returns 0 when total is 0.", "answer": False, "explanation": "NULLIF returns NULL (not 0) when the two arguments are equal. NULLIF(0, 0) = NULL. That's its purpose — turn the problematic 0 into NULL so dividing by it gives NULL instead of a division error."},
                    {"type": "fill_blank", "question": "Label scores A(90+) B(80+) F: SELECT name, CASE ___ score>=90 THEN 'A' WHEN score>=80 THEN 'B' ELSE 'F' END FROM grades", "template": "CASE ___ score>=90 THEN 'A' WHEN score>=80 THEN 'B' ELSE 'F' END", "answer": "WHEN", "explanation": "CASE syntax always starts with WHEN, not IF. Full syntax: CASE WHEN condition THEN result WHEN ... ELSE fallback END. The ELSE is optional but recommended to handle unexpected values."}
                ]
            },
            "challenge": {
                "instructions": "Build a sales performance report using CASE for labels ('Exceeded'/'Met'/'Missed'), COALESCE for NULL commissions, NULLIF for safe conversion rates. Sort by revenue descending. Print a formatted table.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE reps (name TEXT, target REAL, actual REAL, leads INTEGER, deals INTEGER, commission REAL)')
cur.executemany('INSERT INTO reps VALUES(?,?,?,?,?,?)',[('Alice',100000,118000,80,24,5000),('Bob',80000,76000,60,12,None),('Carol',90000,90000,45,18,4200),('Dave',70000,30000,20,0,None),('Eve',110000,155000,100,40,8000)])

print('=== Sales Performance Report ===')
# Use CASE: Exceeded (>=100%), Met (>=90%), Missed
# Use COALESCE for commission (0 if NULL)
# Use NULLIF for deals/leads %
# Sort by actual DESC
conn.close()""",
                "tests": [{"type": "code_contains", "value": "CASE"}, {"type": "code_contains", "value": "COALESCE"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE reps (name TEXT, target REAL, actual REAL, leads INTEGER, deals INTEGER, commission REAL)')
cur.executemany('INSERT INTO reps VALUES(?,?,?,?,?,?)',[('Alice',100000,118000,80,24,5000),('Bob',80000,76000,60,12,None),('Carol',90000,90000,45,18,4200),('Dave',70000,30000,20,0,None),('Eve',110000,155000,100,40,8000)])
print('=== Sales Performance Report ===')
for r in cur.execute('''SELECT name, actual, target, COALESCE(commission,0) AS comm,
    ROUND(100.0*deals/NULLIF(leads,0),1) AS conv,
    CASE WHEN actual>=target THEN 'Exceeded' WHEN actual>=target*0.9 THEN 'Met' ELSE 'Missed' END AS status
    FROM reps ORDER BY actual DESC'''):
    print(f"  {r[0]:<8} ${r[1]:>9,.0f}  conv={r[4] or 0}%  comm=${r[3]:,.0f}  [{r[5]}]")
conn.close()""",
                "challenge_variations": [
                    "CASE in ORDER BY: sort urgent tickets first, then by date — CASE WHEN priority='urgent' THEN 1 ELSE 2 END.",
                    "CASE in GROUP BY: bucket ages into Young/Mid/Senior bands.",
                    "Chain three fallbacks: COALESCE(mobile, home, work, 'No phone').",
                    "Use CASE to output different columns based on a user flag.",
                    "NULLIF to handle empty strings: NULLIF(TRIM(email), '') to treat '' as NULL.",
                    "Build a risk score: CASE with multiple WHEN conditions based on 3 different columns.",
                    "Use COALESCE in a LEFT JOIN to show 'None' for customers with no manager.",
                    "Calculate safe running total using COALESCE to replace cumulative NULLs with 0.",
                    "Use CASE in INSERT: INSERT SELECT with a CASE to transform source data during load.",
                    "Implement a letter-grade curve: CASE with adjusted thresholds based on class average (subquery)."
                ]
            }
        },
        {
            "id": "m3-l24",
            "title": "Views & Indexes — Speed and Simplicity",
            "subtitle": "Reusable saved queries and the B-tree structures that make queries fast",
            "difficulty": "intermediate",
            "business_context": "Your analytics team runs the same 5-table JOIN every day. Save it as a VIEW — a named virtual table they can query like any real table. And when that query takes 30 seconds on 10 million rows, an INDEX brings it to milliseconds.",
            "concept": {
                "theory": "A VIEW is a stored SELECT query that behaves like a table — SELECT from it without knowing the underlying JOIN logic. It re-runs the underlying query each call (no cached data). An INDEX is a B-tree structure that finds rows matching a WHERE condition without scanning every row. Indexes speed reads but slow writes.",
                "business_angle": "Views publish 'clean' data to business users without exposing raw tables or requiring them to know JOIN syntax. Indexes are non-negotiable for production — a missing index on a 10M-row table can turn a millisecond query into minutes.",
                "worked_example_intro": "We'll create a view encapsulating a 3-table JOIN, add indexes, and see the query plan change.",
                "key_insight": "Index foreign key columns and any column in frequent WHERE/JOIN conditions. Primary keys are auto-indexed. EXPLAIN QUERY PLAN shows whether your query uses an index."
            },
            "worked_example": """import sqlite3, time, random

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)')
cur.execute('CREATE TABLE products  (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
cur.execute('CREATE TABLE orders    (id INTEGER PRIMARY KEY, cust_id INTEGER, prod_id INTEGER, date TEXT, qty INTEGER)')
random.seed(1)
cur.executemany('INSERT INTO customers VALUES(?,?,?)',[(i,f'C{i}',['NYC','LA','Chicago'][i%3]) for i in range(1,501)])
cur.executemany('INSERT INTO products VALUES(?,?,?,?)',[(i,f'P{i}',['Electronics','Office'][i%2],round(random.uniform(10,500),2)) for i in range(1,101)])
cur.executemany('INSERT INTO orders VALUES(?,?,?,?,?)',[(i,random.randint(1,500),random.randint(1,100),f'2024-0{random.randint(1,3)}-{random.randint(1,28):02d}',random.randint(1,10)) for i in range(1,10001)])

# CREATE VIEW — encapsulates JOIN logic
cur.execute('''CREATE VIEW order_detail AS
    SELECT o.id, c.name AS customer, c.city, p.name AS product,
           p.category, o.qty, ROUND(o.qty*p.price,2) AS total, o.date
    FROM orders o
    JOIN customers c ON o.cust_id=c.id
    JOIN products  p ON o.prod_id=p.id''')

# Query view like a table
print('=== NYC orders over $200 (from view) ===')
for r in cur.execute("SELECT customer, product, total FROM order_detail WHERE city='NYC' AND total > 200 LIMIT 3"):
    print(f"  {r[0]}: {r[1]} ${r[2]:.2f}")

# Index performance
t0 = time.perf_counter()
cur.execute("SELECT COUNT(*) FROM orders WHERE cust_id=42").fetchone()
no_idx = (time.perf_counter()-t0)*1000

cur.execute('CREATE INDEX idx_orders_cust ON orders(cust_id)')
cur.execute('CREATE INDEX idx_orders_prod ON orders(prod_id)')

t0 = time.perf_counter()
cur.execute("SELECT COUNT(*) FROM orders WHERE cust_id=42").fetchone()
with_idx = (time.perf_counter()-t0)*1000

print(f"\\nWithout index: {no_idx:.3f}ms | With index: {with_idx:.3f}ms")
plan = cur.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE cust_id=42").fetchall()
print(f"Plan: {plan[0][-1]}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "CREATE VIEW v AS SELECT ...",
                        "SELECT * FROM v WHERE condition",
                        "DROP VIEW IF EXISTS v",
                        "CREATE INDEX idx_name ON table(column)",
                        "EXPLAIN QUERY PLAN SELECT ...  -- check index use"
                    ],
                    "notes": "Views don't store data — they re-run the query each time. Over-indexing slows INSERT/UPDATE/DELETE. Index what you query, not everything."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Which column to index first on an orders table?", "options": ["The product description (long text)","customer_id (FK in WHERE/JOIN)","The order notes field","Row created_at (rarely queried)"], "answer": 1, "explanation": "Index customer_id because it's a foreign key used in JOIN ON and WHERE conditions constantly. Long text fields rarely benefit from standard indexes. Rarely-queried columns don't need indexes."},
                    {"type": "true_false", "question": "A VIEW stores a cached copy of query results.", "answer": False, "explanation": "A standard VIEW stores only the SQL definition. It re-runs the underlying query every time you SELECT from it. PostgreSQL/Oracle have materialized views that DO cache, but SQLite does not support them."},
                    {"type": "fill_blank", "question": "Create an index on orders.customer_id: CREATE ___ idx_ord_cust ON orders(customer_id)", "template": "CREATE ___ idx_ord_cust ON orders(customer_id)", "answer": "INDEX", "explanation": "CREATE INDEX name ON table(column) creates a B-tree index. Add UNIQUE to also enforce uniqueness. Naming convention: idx_tablename_column makes EXPLAIN output readable."}
                ]
            },
            "challenge": {
                "instructions": "Create a 'monthly_revenue' view joining orders+customers+products that shows month, city, category, and revenue. Add indexes on FK columns. Query the view to show top 3 cities by total revenue.",
                "starter_code": """import sqlite3, random
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)')
cur.execute('CREATE TABLE products  (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
cur.execute('CREATE TABLE orders    (id INTEGER PRIMARY KEY, cust_id INTEGER, prod_id INTEGER, month TEXT, qty INTEGER)')
random.seed(1)
cur.executemany('INSERT INTO customers VALUES(?,?,?)',[(i,f'C{i}',['NYC','LA','Chicago'][i%3]) for i in range(1,201)])
cur.executemany('INSERT INTO products VALUES(?,?,?,?)',[(i,f'P{i}',['Electronics','Office'][i%2],round(random.uniform(20,500),2)) for i in range(1,51)])
cur.executemany('INSERT INTO orders VALUES(?,?,?,?,?)',[(i,random.randint(1,200),random.randint(1,50),f'2024-0{random.randint(1,3)}',random.randint(1,5)) for i in range(1,5001)])

# Create the monthly_revenue view

# Add indexes on cust_id and prod_id

print('=== Top 3 Cities by Revenue ===')
# Query the view, GROUP BY city

conn.close()""",
                "tests": [{"type": "code_contains", "value": "CREATE VIEW"}, {"type": "code_contains", "value": "CREATE INDEX"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3, random
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)')
cur.execute('CREATE TABLE products  (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
cur.execute('CREATE TABLE orders    (id INTEGER PRIMARY KEY, cust_id INTEGER, prod_id INTEGER, month TEXT, qty INTEGER)')
random.seed(1)
cur.executemany('INSERT INTO customers VALUES(?,?,?)',[(i,f'C{i}',['NYC','LA','Chicago'][i%3]) for i in range(1,201)])
cur.executemany('INSERT INTO products VALUES(?,?,?,?)',[(i,f'P{i}',['Electronics','Office'][i%2],round(random.uniform(20,500),2)) for i in range(1,51)])
cur.executemany('INSERT INTO orders VALUES(?,?,?,?,?)',[(i,random.randint(1,200),random.randint(1,50),f'2024-0{random.randint(1,3)}',random.randint(1,5)) for i in range(1,5001)])
cur.execute('CREATE VIEW monthly_revenue AS SELECT o.month,c.city,p.category,ROUND(SUM(o.qty*p.price),2) AS revenue FROM orders o JOIN customers c ON o.cust_id=c.id JOIN products p ON o.prod_id=p.id GROUP BY o.month,c.city,p.category')
cur.execute('CREATE INDEX idx_ord_cust ON orders(cust_id)')
cur.execute('CREATE INDEX idx_ord_prod ON orders(prod_id)')
print('=== Top 3 Cities by Revenue ===')
for r in cur.execute('SELECT city, ROUND(SUM(revenue),0) AS total FROM monthly_revenue GROUP BY city ORDER BY total DESC LIMIT 3'):
    print(f"  {r[0]}: ${r[1]:,.0f}")
conn.close()""",
                "challenge_variations": [
                    "Create a view for customer lifetime value and add an index to speed the underlying JOIN.",
                    "Use EXPLAIN QUERY PLAN to verify an index is actually being used by your WHERE clause.",
                    "Create a UNIQUE index on (user_id, date) to prevent duplicate daily rows.",
                    "Build a partial index: CREATE INDEX idx_active ON users(email) WHERE active=1.",
                    "Drop and recreate a view with modified logic using DROP VIEW IF EXISTS.",
                    "Create a composite index on (category, price) for a category+price range filter.",
                    "Analyze the performance difference of an indexed vs non-indexed column on 500k rows.",
                    "Build a 'clean data' view using COALESCE and CASE to handle NULLs before consumers see them.",
                    "Create a view that uses a window function, then query it with a WHERE on the window result.",
                    "Simulate role-based access by creating views that expose only certain columns to different 'users'."
                ]
            }
        },
        {
            "id": "m3-l25",
            "title": "Window Functions — Analytics Without Losing Rows",
            "subtitle": "Running totals, rankings, and MoM comparisons while keeping every row",
            "difficulty": "advanced",
            "business_context": "You want to show each order alongside that customer's running total — not just a GROUP BY summary. Window functions compute aggregates OVER a defined window of rows while keeping every individual row intact. They power executive dashboards.",
            "concept": {
                "theory": "Window functions use OVER() to define the computation window. PARTITION BY divides rows into groups (like GROUP BY but without collapsing). ORDER BY inside OVER() determines sequence for running totals and rankings. Key functions: ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD(), SUM() OVER(), AVG() OVER().",
                "business_angle": "Window functions power the metrics every executive asks for: running revenue, month-over-month growth, sales rep rankings, moving averages. They're required for any analyst or data science role.",
                "worked_example_intro": "We'll build rankings, running totals, MoM comparisons, and moving averages with window functions.",
                "key_insight": "Mental model: OVER() means 'compute against this window of rows but keep every original row visible.' SUM() GROUP BY collapses. SUM() OVER() keeps all rows and adds the aggregate as an extra column."
            },
            "worked_example": """import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE sales (rep TEXT, month TEXT, revenue REAL)')
cur.executemany('INSERT INTO sales VALUES(?,?,?)',[
    ('Alice','2024-01',45000),('Alice','2024-02',52000),('Alice','2024-03',48000),
    ('Bob','2024-01',38000),('Bob','2024-02',41000),('Bob','2024-03',55000),
    ('Carol','2024-01',62000),('Carol','2024-02',58000),('Carol','2024-03',71000),
])

print('=== Monthly Rankings ===')
for r in cur.execute('''
    SELECT rep, month, revenue,
        RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank_in_month
    FROM sales ORDER BY month, rank_in_month
'''):
    print(f"  {r[1]} {r[0]:<8} ${r[2]:>7,.0f}  #{r[3]}")

print('\\n=== Running Revenue per Rep ===')
for r in cur.execute('''
    SELECT rep, month, revenue,
        SUM(revenue) OVER (PARTITION BY rep ORDER BY month) AS running
    FROM sales ORDER BY rep, month
'''):
    print(f"  {r[0]:<8} {r[1]}  ${r[2]:>7,.0f}  running=${r[3]:>9,.0f}")

print('\\n=== Month-over-Month Change ===')
for r in cur.execute('''
    SELECT rep, month, revenue,
        ROUND(revenue - LAG(revenue) OVER (PARTITION BY rep ORDER BY month), 0) AS change
    FROM sales ORDER BY rep, month
'''):
    chg = f"+${r[3]:,.0f}" if r[3] and r[3]>0 else (f"-${abs(r[3]):,.0f}" if r[3] else "first month")
    print(f"  {r[0]:<8} {r[1]}  ${r[2]:>7,.0f}  MoM: {chg}")
conn.close()""",
            "quiz": {
                "reference": {
                    "key_syntax": [
                        "ROW_NUMBER() OVER (ORDER BY col)",
                        "RANK() OVER (PARTITION BY grp ORDER BY col)  -- gaps on tie",
                        "DENSE_RANK()  -- no gaps on tie",
                        "SUM(col) OVER (PARTITION BY grp ORDER BY col)  -- running total",
                        "LAG(col) OVER (PARTITION BY grp ORDER BY col)  -- previous row",
                        "LEAD(col) OVER (...)  -- next row"
                    ],
                    "notes": "Window functions require SQLite 3.25+ (2018). Check: SELECT sqlite_version(). PARTITION BY is optional — without it, window is the entire result set."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "Two rows tie for 2nd place. RANK() vs DENSE_RANK() gives:", "options": ["Both give 2,2,3 (no difference)","RANK() gives 2,2,4; DENSE_RANK() gives 2,2,3","RANK() gives 2,3; DENSE_RANK() gives 2,2","RANK() errors on ties"], "answer": 1, "explanation": "RANK() skips ranks after ties (2,2,4 — skips 3). DENSE_RANK() never skips (2,2,3). Use DENSE_RANK for leaderboards where gaps look confusing; RANK() for official competition-style rankings."},
                    {"type": "true_false", "question": "Window functions collapse rows the same way GROUP BY does.", "answer": False, "explanation": "This is the critical distinction. GROUP BY collapses many rows to one per group. Window functions compute over a window but preserve every original row — you see both individual data AND the window aggregate in the same output."},
                    {"type": "fill_blank", "question": "Get each row's previous month revenue: ___(revenue) OVER (PARTITION BY rep ORDER BY month)", "template": "___(revenue) OVER (PARTITION BY rep ORDER BY month)", "answer": "LAG", "explanation": "LAG(col, n) looks back n rows in the window order. LAG(revenue) with no n defaults to 1 (the previous row). The first row in each partition returns NULL. LEAD() looks forward."}
                ]
            },
            "challenge": {
                "instructions": "Build a comprehensive window function report: (1) rank all reps by Q1 total revenue, (2) MoM % change per rep, (3) each month's revenue as % of rep's 3-month total, (4) 2-month moving average.",
                "starter_code": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE sales (rep TEXT, month TEXT, revenue REAL)')
cur.executemany('INSERT INTO sales VALUES(?,?,?)',[
    ('Alice','2024-01',45000),('Alice','2024-02',52000),('Alice','2024-03',48000),
    ('Bob','2024-01',38000),('Bob','2024-02',61000),('Bob','2024-03',55000),
    ('Carol','2024-01',72000),('Carol','2024-02',68000),('Carol','2024-03',81000),
    ('Dave','2024-01',28000),('Dave','2024-02',32000),('Dave','2024-03',29000),
])

print('=== 1. Overall Rankings ===')
# RANK each rep by SUM of all 3 months (use a subquery or CTE)

print('\\n=== 2. MoM % Change ===')
# LAG to get prev month, compute (current-prev)/prev * 100

print('\\n=== 3. % of Rep 3-Month Total ===')
# SUM(revenue) OVER (PARTITION BY rep) in denominator

print('\\n=== 4. 2-Month Moving Average ===')
# AVG OVER ROWS BETWEEN 1 PRECEDING AND CURRENT ROW

conn.close()""",
                "tests": [{"type": "code_contains", "value": "OVER"}, {"type": "code_contains", "value": "PARTITION BY"}, {"type": "runs_without_error"}],
                "solution": """import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('CREATE TABLE sales (rep TEXT, month TEXT, revenue REAL)')
cur.executemany('INSERT INTO sales VALUES(?,?,?)',[('Alice','2024-01',45000),('Alice','2024-02',52000),('Alice','2024-03',48000),('Bob','2024-01',38000),('Bob','2024-02',61000),('Bob','2024-03',55000),('Carol','2024-01',72000),('Carol','2024-02',68000),('Carol','2024-03',81000),('Dave','2024-01',28000),('Dave','2024-02',32000),('Dave','2024-03',29000)])
print('=== 1. Overall Rankings ===')
for r in cur.execute("SELECT rep, SUM(revenue) AS total, RANK() OVER (ORDER BY SUM(revenue) DESC) AS rnk FROM sales GROUP BY rep ORDER BY rnk"):
    print(f"  #{r[2]} {r[0]}: ${r[1]:,.0f}")
print('\\n=== 2. MoM % Change ===')
for r in cur.execute("SELECT rep,month,revenue, ROUND(100.0*(revenue-LAG(revenue)OVER(PARTITION BY rep ORDER BY month))/LAG(revenue)OVER(PARTITION BY rep ORDER BY month),1) AS pct FROM sales ORDER BY rep,month"):
    print(f"  {r[0]:<8} {r[1]} ${r[2]:>7,.0f}  MoM:{(str(r[3])+'%') if r[3] is not None else '—'}")
print('\\n=== 3. % of Total ===')
for r in cur.execute("SELECT rep,month,revenue, ROUND(100.0*revenue/SUM(revenue)OVER(PARTITION BY rep),1) AS pct FROM sales ORDER BY rep,month"):
    print(f"  {r[0]:<8} {r[1]} ${r[2]:>7,.0f}  {r[3]}%")
print('\\n=== 4. 2-Mo Moving Avg ===')
for r in cur.execute("SELECT rep,month,revenue, ROUND(AVG(revenue)OVER(PARTITION BY rep ORDER BY month ROWS BETWEEN 1 PRECEDING AND CURRENT ROW),0) AS ma FROM sales ORDER BY rep,month"):
    print(f"  {r[0]:<8} {r[1]} ${r[2]:>7,.0f}  2mo avg:${r[3]:,.0f}")
conn.close()""",
                "challenge_variations": [
                    "3-month rolling average for daily stock prices: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.",
                    "NTILE(4) to split customers into quartiles by total spend.",
                    "FIRST_VALUE() and LAST_VALUE() to get first and last order date per customer.",
                    "Cumulative market share: running SUM / total * 100 using SUM OVER / total subquery.",
                    "ROW_NUMBER() to deduplicate: keep most recent record per customer (WHERE rn=1).",
                    "7-day rolling sum of daily signups for a weekly trend line.",
                    "LEAD() to compute days until next order and flag customers with 30+ day gaps.",
                    "Dual rank: rank within category AND overall rank in the same SELECT.",
                    "Cohort retention: for each signup month, % of users who return each subsequent month.",
                    "Percentile rank per department: what percentile is each employee's salary within their dept?"
                ]
            }
        },
        {
            "id": "m3-capstone",
            "title": "Module 3 Capstone — Build a Complete Sales Database",
            "subtitle": "Design, populate, and analyze a real multi-table business database from scratch",
            "difficulty": "advanced",
            "business_context": "You're the first data analyst at a growing e-commerce company. Data is scattered in spreadsheets. Your job: design a proper SQLite database, import the data, and answer 6 executive-level business questions — the CEO is presenting on Monday.",
            "concept": {
                "theory": "This capstone integrates every Module 3 skill: normalized schema with PKs/FKs, bulk INSERT, SELECT with WHERE/ORDER BY/LIMIT, GROUP BY+HAVING, multi-table JOINs (INNER + LEFT), subqueries, CASE/COALESCE, views, and window functions.",
                "business_angle": "The 6 questions simulate real executive asks: revenue by period, top customers, product performance, regional breakdown, churn risk, and growth. The ability to answer all of these from a blank schema is the core analyst skill.",
                "worked_example_intro": "Build the full schema, load data, answer all 6 questions. No shortcuts — this is what analysts actually do.",
                "key_insight": "Always start from the business questions, not the schema. Design the tables to support the answers you need to produce."
            },
            "worked_example": """import sqlite3, random
random.seed(42)
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE regions   (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE categories(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER, joined TEXT,
                        FOREIGN KEY(region_id) REFERENCES regions(id));
CREATE TABLE products  (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER, price REAL,
                        FOREIGN KEY(category_id) REFERENCES categories(id));
CREATE TABLE orders    (id INTEGER PRIMARY KEY, customer_id INTEGER, date TEXT,
                        FOREIGN KEY(customer_id) REFERENCES customers(id));
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER,
                        PRIMARY KEY(order_id,product_id),
                        FOREIGN KEY(order_id) REFERENCES orders(id),
                        FOREIGN KEY(product_id) REFERENCES products(id));
''')

regions = [(1,'East'),(2,'West'),(3,'Central'),(4,'South')]
cats    = [(1,'Electronics'),(2,'Furniture'),(3,'Office'),(4,'Clothing')]
cur.executemany('INSERT INTO regions VALUES(?,?)', regions)
cur.executemany('INSERT INTO categories VALUES(?,?)', cats)
products_data = [(i,f'Product_{i}',random.randint(1,4),round(random.uniform(15,800),2)) for i in range(1,31)]
cur.executemany('INSERT INTO products VALUES(?,?,?,?)', products_data)
months = ['2024-01','2024-02','2024-03','2024-04','2024-05','2024-06']
customers_data = [(i,f'Customer_{i}',random.randint(1,4),random.choice(months[:3])) for i in range(1,101)]
cur.executemany('INSERT INTO customers VALUES(?,?,?,?)', customers_data)
orders_data = [(i,random.randint(1,100),f'{random.choice(months)}-{random.randint(1,28):02d}') for i in range(1,401)]
cur.executemany('INSERT INTO orders VALUES(?,?,?)', orders_data)
items_seen = set()
items_data = []
for oid in range(1,401):
    for _ in range(random.randint(1,4)):
        pid = random.randint(1,30)
        if (oid,pid) not in items_seen:
            items_data.append((oid,pid,random.randint(1,5)))
            items_seen.add((oid,pid))
cur.executemany('INSERT INTO order_items VALUES(?,?,?)', items_data)
conn.commit()

print('Q1: Monthly Revenue')
for r in cur.execute("SELECT substr(o.date,1,7) AS mo, ROUND(SUM(oi.qty*p.price),0) AS rev FROM order_items oi JOIN orders o ON oi.order_id=o.id JOIN products p ON oi.product_id=p.id GROUP BY mo ORDER BY mo"):
    print(f"  {r[0]}: ${r[1]:>10,.0f}")

print('\\nQ2: Top 5 Customers by Lifetime Value')
for r in cur.execute("SELECT c.name, rg.name AS region, ROUND(SUM(oi.qty*p.price),0) AS ltv FROM customers c JOIN orders o ON c.id=o.customer_id JOIN order_items oi ON o.id=oi.order_id JOIN products p ON oi.product_id=p.id JOIN regions rg ON c.region_id=rg.id GROUP BY c.id ORDER BY ltv DESC LIMIT 5"):
    print(f"  {r[0]:<14} ({r[1]:<8}) ${r[2]:>8,.0f}")

print('\\nQ3: Revenue by Product Category')
for r in cur.execute("SELECT cat.name, ROUND(SUM(oi.qty*p.price),0) AS rev FROM order_items oi JOIN products p ON oi.product_id=p.id JOIN categories cat ON p.category_id=cat.id GROUP BY cat.name ORDER BY rev DESC"):
    print(f"  {r[0]:<15} ${r[1]:>10,.0f}")

print('\\nQ4: Churn Risk (no order in last 2 months)')
for r in cur.execute("SELECT c.name, MAX(o.date) AS last_order FROM customers c LEFT JOIN orders o ON c.id=o.customer_id GROUP BY c.id HAVING MAX(o.date) < '2024-05-01' OR MAX(o.date) IS NULL ORDER BY last_order LIMIT 5"):
    print(f"  {r[0]:<16} last: {r[1] or 'Never'}")

print('\\nQ5: Month-over-Month Revenue Growth')
for r in cur.execute("SELECT mo, rev, LAG(rev)OVER(ORDER BY mo) AS prev, ROUND(100.0*(rev-LAG(rev)OVER(ORDER BY mo))/LAG(rev)OVER(ORDER BY mo),1) AS pct FROM (SELECT substr(o.date,1,7) AS mo, ROUND(SUM(oi.qty*p.price),0) AS rev FROM order_items oi JOIN orders o ON oi.order_id=o.id JOIN products p ON oi.product_id=p.id GROUP BY mo ORDER BY mo)"):
    chg = f"{'+' if r[3] and r[3]>0 else ''}{r[3]}%" if r[3] else "—"
    print(f"  {r[0]}: ${r[1]:>10,.0f}  MoM: {chg}")

print('\\nQ6: Top Product per Region')
for r in cur.execute("SELECT region, product, revenue, rnk FROM (SELECT rg.name AS region, p.name AS product, ROUND(SUM(oi.qty*p.price),0) AS revenue, RANK() OVER (PARTITION BY rg.name ORDER BY SUM(oi.qty*p.price) DESC) AS rnk FROM order_items oi JOIN orders o ON oi.order_id=o.id JOIN customers c ON o.customer_id=c.id JOIN regions rg ON c.region_id=rg.id JOIN products p ON oi.product_id=p.id GROUP BY rg.name,p.name) WHERE rnk=1"):
    print(f"  {r[0]:<10} #{r[3]}: {r[1]:<16} ${r[2]:>8,.0f}")

conn.close()
print('\\nCapstone complete — 6 business questions answered!')""",
            "quiz": {
                "reference": {
                    "key_syntax": ["Star schema: fact (orders,order_items) + dimensions (customers,products,regions,categories)", "LEFT JOIN + HAVING for churn detection", "Window RANK() OVER(PARTITION BY) for top-per-group", "MoM growth with LAG() in a subquery"],
                    "notes": "Real analyst workflow: understand business questions first, design schema to support them, then write SQL."
                },
                "questions": [
                    {"type": "multiple_choice", "question": "To find the #1 product in each region, you use:", "options": ["GROUP BY region, product ORDER BY revenue DESC LIMIT 1","RANK() OVER(PARTITION BY region ORDER BY revenue DESC) then WHERE rank=1","TOP 1 per region (SQL Server only)","A separate query per region"], "answer": 1, "explanation": "RANK() OVER(PARTITION BY region ORDER BY revenue DESC) assigns rank 1 to the top product within each region independently. Wrap in a subquery and filter WHERE rnk=1 to get one row per region."},
                    {"type": "true_false", "question": "In a star schema, the 'fact table' (orders) holds foreign keys that point to 'dimension tables' (customers, products).", "answer": True, "explanation": "Star schema design: the central fact table holds measurable events (orders, transactions) with foreign keys to dimension tables that describe who/what/where/when. This design makes analytical queries fast and joins intuitive."},
                    {"type": "fill_blank", "question": "To safely handle customers with no orders in a churn query, use ___ JOIN orders ON customer_id then filter with HAVING MAX(order_date) < cutoff OR IS NULL.", "template": "Use ___ JOIN to include customers with zero orders.", "answer": "LEFT", "explanation": "LEFT JOIN keeps all customers — including those with no orders. WHERE order_date < cutoff would filter BEFORE grouping and lose zero-order customers. HAVING on the MAX() after LEFT JOIN is the correct pattern."}
                ]
            },
            "challenge": {
                "instructions": "Run the full capstone above, then add Q7: 'Average Order Value (AOV = total revenue / distinct orders) by region, ranked highest to lowest.' Also add Q8: 'Which product category has the highest repeat purchase rate (% of customers who bought from it more than once)?'",
                "starter_code": """# Copy and run the full capstone code above.
# Then add:

print('\\nQ7: Average Order Value by Region')
# AOV = SUM(qty*price) / COUNT(DISTINCT order_id) per region

print('\\nQ8: Category with Highest Repeat Purchase Rate')
# % of customers who bought from each category 2+ times
""",
                "tests": [{"type": "code_contains", "value": "GROUP BY"}, {"type": "output_contains", "value": "Q"}, {"type": "runs_without_error"}],
                "solution": """# Q7:
for r in cur.execute("SELECT rg.name, COUNT(DISTINCT o.id) AS orders, ROUND(SUM(oi.qty*p.price)/COUNT(DISTINCT o.id),2) AS aov FROM order_items oi JOIN orders o ON oi.order_id=o.id JOIN customers c ON o.customer_id=c.id JOIN regions rg ON c.region_id=rg.id JOIN products p ON oi.product_id=p.id GROUP BY rg.name ORDER BY aov DESC"):
    print(f"  {r[0]:<10} {r[1]} orders | AOV ${r[2]:,.2f}")
# Q8:
for r in cur.execute("SELECT cat.name, COUNT(DISTINCT c.id) AS buyers, SUM(CASE WHEN cnt>1 THEN 1 ELSE 0 END) AS repeat_buyers, ROUND(100.0*SUM(CASE WHEN cnt>1 THEN 1 ELSE 0 END)/COUNT(DISTINCT c.id),1) AS repeat_rate FROM (SELECT c.id, cat.id AS cat_id, COUNT(DISTINCT o.id) AS cnt FROM customers c JOIN orders o ON c.id=o.customer_id JOIN order_items oi ON o.id=oi.order_id JOIN products p ON oi.product_id=p.id JOIN categories cat ON p.category_id=cat.id GROUP BY c.id,cat.id) sub JOIN customers c ON sub.id=c.id JOIN categories cat ON sub.cat_id=cat.id GROUP BY cat.name ORDER BY repeat_rate DESC"):
    print(f"  {r[0]:<15} {r[1]} buyers | {r[2]} repeat ({r[3]}%)")""",
                "challenge_variations": [
                    "Package all 8 queries as Python functions that accept a connection and return lists of results.",
                    "Export all query results to a pandas DataFrame and generate a combined Excel report.",
                    "Add a PRODUCTS_WITHOUT_SALES query using LEFT JOIN + WHERE IS NULL.",
                    "Create views for Q2 and Q5 and add indexes to speed the underlying JOINs.",
                    "Modify Q5 to show weekly growth using strftime('%Y-%W', date) instead of monthly.",
                    "Build a repeat purchase rate metric across all categories, not just the top one.",
                    "Add cohort analysis: group customers by their first-order month and track 3-month retention.",
                    "Run the capstone against a real CSV file loaded into SQLite instead of generated data.",
                    "Add error handling: wrap each query in try/except and log failures to an errors table.",
                    "Time each of the 8 queries and identify which benefits most from an additional index."
                ]
            }
        }
    ]
}
