MODULE_1 = {
    "id": "module1",
    "title": "Python Foundations",
    "description": "Start your coding journey. Learn the building blocks of Python — the same language you'll use throughout your entire program.",
    "course": "MSBC 5070 · Python Bootcamp",
    "order": 1,
    "locked": False,
    "lessons": [
        {
            "id": "m1-l1",
            "title": "What is Python? Your First Line of Code",
            "order": 1,
            "duration_min": 15,
            "concept": """Python is a programming language — a way to give instructions to a computer. It's one of the most popular languages in the world, especially for data science and AI.

When you write Python, you're writing a recipe for the computer to follow. The computer reads your code from top to bottom and does exactly what you tell it.

Your very first Python instruction is `print()`. It tells the computer to display something on the screen.

```python
print("Hello, world!")
```

This prints: `Hello, world!`

The text inside the quotes is called a **string** — any sequence of letters, numbers, or symbols wrapped in quotes.

You can print anything:
```python
print("I'm going to be a data scientist!")
print(42)
print(3.14)
```

**Why Python?**
- Clear, readable syntax (it almost reads like English)
- Industry standard for data analytics, machine learning, and AI
- What your MS program is built on""",
            "reference": {
                "key_syntax": ["print(value)", "print('text')", "print(42)"],
                "notes": "Strings use single or double quotes — both work."
            },
            "questions": [
                {
                    "type": "true_false",
                    "question": "Python reads your code from top to bottom.",
                    "answer": True,
                    "explanation": "Correct! Python executes code sequentially, line by line, from top to bottom."
                },
                {
                    "type": "multiple_choice",
                    "question": "What does print() do?",
                    "options": [
                        "Saves your code to a file",
                        "Displays something on the screen",
                        "Deletes a variable",
                        "Sends an email"
                    ],
                    "answer": 1,
                    "explanation": "print() outputs whatever is inside the parentheses to the screen."
                },
                {
                    "type": "fill_blank",
                    "question": 'Complete the code to display "Hello, Orion!"',
                    "template": '___("Hello, Orion!")',
                    "answer": "print",
                    "explanation": "print() is the function for displaying output in Python."
                }
            ],
            "challenge": {
                "instructions": 'Write code that prints your name on one line, then prints "Future Data Scientist" on the next line.',
                "starter_code": "# Write your code below\n",
                "tests": [
                    {"type": "output_contains", "value": "Future Data Scientist"}
                ],
                "solution": 'print("Your Name")\nprint("Future Data Scientist")'
            }
        },
        {
            "id": "m1-l2",
            "title": "Variables — Giving Names to Data",
            "order": 2,
            "duration_min": 15,
            "concept": """A **variable** is a named container that stores data. Think of it like a labeled box — you put something in, give the box a name, and retrieve it later.

```python
name = "Alex"
age = 28
gpa = 3.8
is_student = True
```

The `=` sign is the **assignment operator** — it stores the value on the right into the variable on the left.

**Rules for variable names:**
- Must start with a letter or underscore (`_`)
- Can contain letters, numbers, underscores
- Case-sensitive (`Name` and `name` are different!)
- No spaces — use `_` instead: `first_name = "Alex"`

**Python's main data types:**
| Type | Example | What it is |
|------|---------|------------|
| `str` | `"hello"` | Text (string) |
| `int` | `42` | Whole number |
| `float` | `3.14` | Decimal number |
| `bool` | `True` / `False` | Yes or no |

You can use `type()` to check a variable's type:
```python
print(type(name))   # <class 'str'>
print(type(age))    # <class 'int'>
```""",
            "reference": {
                "key_syntax": [
                    "variable_name = value",
                    "type(variable)",
                    "str, int, float, bool"
                ],
                "notes": "Variable names are case-sensitive. Use snake_case (underscores) for multi-word names."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which variable name is valid in Python?",
                    "options": ["2name", "first name", "first_name", "first-name"],
                    "answer": 2,
                    "explanation": "first_name is valid. Variable names can't start with a number, can't have spaces, and can't use hyphens."
                },
                {
                    "type": "true_false",
                    "question": "In Python, `Name` and `name` refer to the same variable.",
                    "answer": False,
                    "explanation": "Python is case-sensitive, so Name and name are two different variables."
                },
                {
                    "type": "fill_blank",
                    "question": "Store the number 25 in a variable called age.",
                    "template": "age ___ 25",
                    "answer": "=",
                    "explanation": "The = sign assigns a value to a variable."
                }
            ],
            "challenge": {
                "instructions": "Create variables for: your first name (string), your target GPA (float), the year you'll graduate (int), and whether you're excited to start (bool). Then print all four values.",
                "starter_code": "# Create your variables below\n\n# Print them all\n",
                "tests": [
                    {"type": "runs_without_error"},
                    {"type": "variable_count_min", "value": 4}
                ],
                "solution": 'first_name = "Alex"\ntarget_gpa = 3.9\ngrad_year = 2027\nexcited = True\nprint(first_name)\nprint(target_gpa)\nprint(grad_year)\nprint(excited)'
            }
        },
        {
            "id": "m1-l3",
            "title": "Strings — Working with Text",
            "order": 3,
            "duration_min": 20,
            "concept": """Strings are text — any characters inside quotes. Since data analytics deals with lots of text (names, categories, descriptions), strings are critical.

**Combining strings (concatenation):**
```python
first = "Business"
second = "Analytics"
full = first + " " + second
print(full)  # Business Analytics
```

**f-strings — the modern way to format text:**
```python
name = "Alex"
score = 95
print(f"Student: {name}, Score: {score}")
# Student: Alex, Score: 95
```
The `f` before the quote makes it an f-string. Variables inside `{}` get inserted automatically.

**Useful string methods:**
```python
text = "  hello world  "
print(text.upper())      # HELLO WORLD
print(text.lower())      # hello world
print(text.strip())      # hello world (removes spaces)
print(text.replace("world", "Python"))  # hello Python
print(len("hello"))      # 5
```

**Accessing characters:**
```python
word = "Python"
print(word[0])   # P  (first character, index 0)
print(word[-1])  # n  (last character)
print(word[0:3]) # Pyt (slice from index 0 to 2)
```""",
            "reference": {
                "key_syntax": [
                    'f"text {variable}"',
                    "str.upper() / .lower()",
                    "str.strip() / .replace(a, b)",
                    "len(str)",
                    "str[index] / str[start:end]"
                ],
                "notes": "String indices start at 0. Negative indices count from the end."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": 'What does "hello".upper() return?',
                    "options": ["hello", "Hello", "HELLO", "Error"],
                    "answer": 2,
                    "explanation": ".upper() converts all characters in a string to uppercase."
                },
                {
                    "type": "fill_blank",
                    "question": 'Use an f-string to print "My score is 98"',
                    "template": 'score = 98\nprint(___"My score is {score}")',
                    "answer": "f",
                    "explanation": "The f prefix before a quote creates an f-string, allowing {variable} interpolation."
                },
                {
                    "type": "true_false",
                    "question": 'word = "Python"; word[0] gives "P"',
                    "answer": True,
                    "explanation": "String indexing starts at 0, so word[0] is the first character."
                }
            ],
            "challenge": {
                "instructions": 'Given the variables below, use an f-string to print: "Hi, I\'m [name] and I\'m [age] years old. My program is [program]."',
                "starter_code": 'name = "Alex"\nage = 28\nprogram = "Business Analytics"\n\n# Write your f-string print below\n',
                "tests": [
                    {"type": "output_contains", "value": "Business Analytics"},
                    {"type": "code_contains", "value": "f\""}
                ],
                "solution": 'name = "Alex"\nage = 28\nprogram = "Business Analytics"\nprint(f"Hi, I\'m {name} and I\'m {age} years old. My program is {program}.")'
            }
        },
        {
            "id": "m1-l4",
            "title": "Numbers and Math",
            "order": 4,
            "duration_min": 15,
            "concept": """Python is excellent at math — from simple arithmetic to complex statistical calculations.

**Arithmetic operators:**
```python
print(10 + 3)   # 13  (addition)
print(10 - 3)   # 7   (subtraction)
print(10 * 3)   # 30  (multiplication)
print(10 / 3)   # 3.333... (division — always float)
print(10 // 3)  # 3   (floor division — drops decimal)
print(10 % 3)   # 1   (modulo — remainder)
print(10 ** 3)  # 1000 (exponent — 10 to the power of 3)
```

**Order of operations:** Python follows PEMDAS — parentheses first, then exponents, multiplication/division, then addition/subtraction.

```python
result = (5 + 3) * 2 ** 2  # = 8 * 4 = 32
```

**Updating variables:**
```python
score = 100
score += 10   # Same as: score = score + 10
score -= 5    # Now 105
score *= 2    # Now 210
```

**Useful built-in math:**
```python
print(abs(-42))      # 42 (absolute value)
print(round(3.7))    # 4  (rounds to nearest int)
print(max(3, 7, 2))  # 7  (maximum)
print(min(3, 7, 2))  # 2  (minimum)
```""",
            "reference": {
                "key_syntax": [
                    "+ - * / // % **",
                    "+= -= *= /=",
                    "abs() round() max() min()"
                ],
                "notes": "/ always returns a float. Use // for integer division."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does 17 % 5 equal?",
                    "options": ["3", "2", "1", "0"],
                    "answer": 1,
                    "explanation": "% is modulo (remainder). 17 divided by 5 = 3 remainder 2."
                },
                {
                    "type": "true_false",
                    "question": "10 / 2 returns an integer (5) in Python.",
                    "answer": False,
                    "explanation": "/ always returns a float in Python 3, so 10 / 2 returns 5.0, not 5."
                },
                {
                    "type": "fill_blank",
                    "question": "What operator raises a number to a power? (e.g., 2 to the power of 8)",
                    "template": "print(2 ___ 8)",
                    "answer": "**",
                    "explanation": "** is the exponentiation operator. 2 ** 8 = 256."
                }
            ],
            "challenge": {
                "instructions": "You scored 87, 92, and 78 on three exams. Calculate and print your average score. Then print whether your average is above 80 (use a comparison like avg > 80).",
                "starter_code": "score1 = 87\nscore2 = 92\nscore3 = 78\n\n# Calculate average\n\n# Print average and whether it's above 80\n",
                "tests": [
                    {"type": "output_contains", "value": "85."},
                    {"type": "runs_without_error"}
                ],
                "solution": "score1 = 87\nscore2 = 92\nscore3 = 78\navg = (score1 + score2 + score3) / 3\nprint(avg)\nprint(avg > 80)"
            }
        },
        {
            "id": "m1-l5",
            "title": "If/Else — Making Decisions",
            "order": 5,
            "duration_min": 20,
            "concept": """Programs need to make decisions based on conditions. `if/elif/else` lets your code take different paths.

```python
grade = 88

if grade >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
else:
    print("Below C")
```

**Important:** Python uses **indentation** (4 spaces) to define code blocks. Code indented under `if` only runs when that condition is True.

**Comparison operators:**
```python
x == y   # Equal to
x != y   # Not equal to
x > y    # Greater than
x < y    # Less than
x >= y   # Greater than or equal
x <= y   # Less than or equal
```

**Logical operators:**
```python
if age >= 18 and has_id:
    print("Welcome!")

if is_weekend or is_holiday:
    print("Day off!")

if not is_raining:
    print("Go outside!")
```""",
            "reference": {
                "key_syntax": [
                    "if condition:",
                    "elif condition:",
                    "else:",
                    "== != > < >= <=",
                    "and / or / not"
                ],
                "notes": "Indentation (4 spaces) is required — it defines the code block."
            },
            "questions": [
                {
                    "type": "code_ordering",
                    "question": "Put these lines in the correct order for a grade checker:",
                    "lines": [
                        'print("Pass")',
                        "else:",
                        "if score >= 60:",
                        'print("Fail")'
                    ],
                    "answer": [2, 0, 1, 3],
                    "explanation": "The if statement comes first, then the indented code for True, then else, then the indented code for False."
                },
                {
                    "type": "true_false",
                    "question": "In Python, you use == to check if two values are equal (not =).",
                    "answer": True,
                    "explanation": "= assigns a value. == compares two values. This is one of the most common beginner mistakes!"
                },
                {
                    "type": "multiple_choice",
                    "question": "What does `and` do in a condition?",
                    "options": [
                        "Both conditions must be True",
                        "At least one condition must be True",
                        "The condition must be False",
                        "It adds two numbers"
                    ],
                    "answer": 0,
                    "explanation": "and requires BOTH conditions to be True. or requires at least one to be True."
                }
            ],
            "challenge": {
                "instructions": "Write a program that checks a student's GPA. If it's 3.7 or above, print 'Honors'. If it's between 3.0 and 3.69, print 'Good Standing'. Otherwise, print 'Academic Probation'.",
                "starter_code": "gpa = 3.5\n\n# Write your if/elif/else below\n",
                "tests": [
                    {"type": "output_contains", "value": "Good Standing"},
                    {"type": "code_contains", "value": "elif"}
                ],
                "solution": "gpa = 3.5\nif gpa >= 3.7:\n    print('Honors')\nelif gpa >= 3.0:\n    print('Good Standing')\nelse:\n    print('Academic Probation')"
            }
        },
        {
            "id": "m1-l6",
            "title": "Loops — Repeating Actions",
            "order": 6,
            "duration_min": 20,
            "concept": """Loops let you repeat code without copy-pasting it. This is essential for processing datasets with thousands of rows.

**for loop — iterate over a sequence:**
```python
grades = [85, 92, 78, 96, 88]

for grade in grades:
    print(grade)
```

**range() — loop a specific number of times:**
```python
for i in range(5):
    print(i)   # prints 0, 1, 2, 3, 4

for i in range(1, 6):
    print(i)   # prints 1, 2, 3, 4, 5
```

**while loop — keep going until condition is False:**
```python
count = 0
while count < 5:
    print(count)
    count += 1   # IMPORTANT: must update the condition or it loops forever!
```

**Loop control:**
```python
for i in range(10):
    if i == 5:
        break      # Stop the loop entirely
    if i % 2 == 0:
        continue   # Skip this iteration, go to next
    print(i)
```

**Accumulating with loops:**
```python
grades = [85, 92, 78, 96, 88]
total = 0
for grade in grades:
    total += grade
average = total / len(grades)
print(average)  # 87.8
```""",
            "reference": {
                "key_syntax": [
                    "for item in list:",
                    "for i in range(n):",
                    "while condition:",
                    "break  # exit loop",
                    "continue  # skip to next"
                ],
                "notes": "Always make sure a while loop's condition eventually becomes False, or it runs forever."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "How many times does range(3) iterate?",
                    "options": ["2", "3", "4", "1"],
                    "answer": 1,
                    "explanation": "range(3) produces 0, 1, 2 — three values. range(n) always starts at 0 and goes up to (but not including) n."
                },
                {
                    "type": "true_false",
                    "question": "`break` skips the current iteration and continues to the next one.",
                    "answer": False,
                    "explanation": "break exits the loop entirely. continue skips the current iteration and moves to the next."
                },
                {
                    "type": "fill_blank",
                    "question": "Complete the code to loop through a list called 'scores'",
                    "template": "___ score in scores:\n    print(score)",
                    "answer": "for",
                    "explanation": "for is used to iterate over a sequence like a list."
                }
            ],
            "challenge": {
                "instructions": "Given a list of exam scores, write a loop that counts how many scores are 90 or above (an 'A'). Print the count at the end.",
                "starter_code": "scores = [72, 95, 88, 91, 63, 99, 85, 90, 77, 94]\ncount = 0\n\n# Loop through scores and count A grades\n\nprint(f'A grades: {count}')\n",
                "tests": [
                    {"type": "output_contains", "value": "A grades: 5"}
                ],
                "solution": "scores = [72, 95, 88, 91, 63, 99, 85, 90, 77, 94]\ncount = 0\nfor score in scores:\n    if score >= 90:\n        count += 1\nprint(f'A grades: {count}')"
            }
        },
        {
            "id": "m1-l7",
            "title": "Functions — Reusable Code Blocks",
            "order": 7,
            "duration_min": 20,
            "concept": """A **function** is a named block of code you can call multiple times. Functions are the foundation of organized, reusable code.

**Defining a function:**
```python
def greet(name):
    message = f"Hello, {name}!"
    return message

result = greet("Alex")
print(result)  # Hello, Alex!
```

**Key parts:**
- `def` — keyword to define a function
- `greet` — the function name
- `(name)` — parameters (inputs)
- `return` — sends a value back to the caller

**Multiple parameters and default values:**
```python
def calculate_grade(score, total=100):
    percentage = (score / total) * 100
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    else:
        return "C"

print(calculate_grade(85))        # B (total defaults to 100)
print(calculate_grade(17, 20))    # A (85%)
```

**Functions can call other functions:**
```python
def average(numbers):
    return sum(numbers) / len(numbers)

def letter_grade(numbers):
    avg = average(numbers)
    return calculate_grade(avg)
```""",
            "reference": {
                "key_syntax": [
                    "def function_name(param):",
                    "    return value",
                    "result = function_name(arg)",
                    "def func(param=default_value):"
                ],
                "notes": "A function without a return statement returns None."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What keyword defines a function in Python?",
                    "options": ["function", "func", "def", "define"],
                    "answer": 2,
                    "explanation": "def is the keyword used to define a function in Python."
                },
                {
                    "type": "true_false",
                    "question": "A function must always have a return statement.",
                    "answer": False,
                    "explanation": "Functions don't need to return a value. Without return, they return None automatically."
                },
                {
                    "type": "code_ordering",
                    "question": "Arrange these lines to create a working function that doubles a number:",
                    "lines": [
                        "def double(n):",
                        "print(double(5))",
                        "    return n * 2"
                    ],
                    "answer": [0, 2, 1],
                    "explanation": "First define the function, then the indented body with return, then call the function."
                }
            ],
            "challenge": {
                "instructions": "Write a function called `bmi_category` that takes weight_kg and height_m as parameters, calculates BMI (weight / height²), and returns: 'Underweight' if BMI < 18.5, 'Normal' if 18.5-24.9, 'Overweight' if 25+. Test it by printing the result for weight=70, height=1.75.",
                "starter_code": "def bmi_category(weight_kg, height_m):\n    # Calculate BMI\n    \n    # Return the category\n    pass\n\nprint(bmi_category(70, 1.75))\n",
                "tests": [
                    {"type": "output_contains", "value": "Normal"}
                ],
                "solution": "def bmi_category(weight_kg, height_m):\n    bmi = weight_kg / (height_m ** 2)\n    if bmi < 18.5:\n        return 'Underweight'\n    elif bmi < 25:\n        return 'Normal'\n    else:\n        return 'Overweight'\n\nprint(bmi_category(70, 1.75))"
            }
        },
        {
            "id": "m1-l8",
            "title": "Lists — Collections of Data",
            "order": 8,
            "duration_min": 20,
            "concept": """A **list** is an ordered collection of items. In data analytics, you'll constantly work with lists of numbers, names, and records.

```python
scores = [85, 92, 78, 96, 88]
names = ["Alice", "Bob", "Carol"]
mixed = [42, "hello", True, 3.14]
```

**Accessing items (indexing):**
```python
print(scores[0])    # 85 (first item)
print(scores[-1])   # 88 (last item)
print(scores[1:3])  # [92, 78] (slice)
```

**Modifying lists:**
```python
scores.append(100)         # Add to end
scores.insert(0, 70)       # Insert at index 0
scores.remove(78)          # Remove first occurrence of 78
popped = scores.pop()      # Remove and return last item
scores[0] = 99             # Change item at index 0
```

**Useful list operations:**
```python
print(len(scores))         # Number of items
print(sum(scores))         # Sum of all numbers
print(max(scores))         # Highest value
print(min(scores))         # Lowest value
print(sorted(scores))      # New sorted list
print(85 in scores)        # True if 85 is in list
```

**List comprehensions — concise list creation:**
```python
squares = [x**2 for x in range(1, 6)]
# [1, 4, 9, 16, 25]

passing = [s for s in scores if s >= 60]
# Only scores >= 60
```""",
            "reference": {
                "key_syntax": [
                    "list[index]  # access",
                    "list.append(item)",
                    "list.remove(item)",
                    "len() sum() max() min() sorted()",
                    "[expr for item in list if condition]"
                ],
                "notes": "Lists are mutable — you can change them after creation. Indices start at 0."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": 'data = ["a", "b", "c"]; what is data[-1]?',
                    "options": ['"a"', '"b"', '"c"', "Error"],
                    "answer": 2,
                    "explanation": "Negative indices count from the end. -1 is the last item, which is 'c'."
                },
                {
                    "type": "fill_blank",
                    "question": "Add the value 100 to the end of the list called 'scores'",
                    "template": "scores.___(100)",
                    "answer": "append",
                    "explanation": ".append() adds an item to the end of a list."
                },
                {
                    "type": "true_false",
                    "question": "[x*2 for x in [1,2,3]] creates [2, 4, 6]",
                    "answer": True,
                    "explanation": "This is a list comprehension — it applies x*2 to each element, producing [2, 4, 6]."
                }
            ],
            "challenge": {
                "instructions": "Given a list of student scores, use a list comprehension to create a new list called 'curved' where each score is increased by 5 points. Then print the average of the curved scores (rounded to 2 decimal places).",
                "starter_code": "scores = [67, 82, 75, 91, 58, 88, 70, 95]\n\n# Create curved list (each score + 5)\n\n# Print the average of curved scores\n",
                "tests": [
                    {"type": "output_contains", "value": "82."},
                    {"type": "code_contains", "value": "for"}
                ],
                "solution": "scores = [67, 82, 75, 91, 58, 88, 70, 95]\ncurved = [s + 5 for s in scores]\naverage = round(sum(curved) / len(curved), 2)\nprint(average)"
            }
        },
        {
            "id": "m1-l9",
            "title": "Dictionaries — Key-Value Data",
            "order": 9,
            "duration_min": 20,
            "concept": """A **dictionary** stores data as **key-value pairs** — like a real dictionary where each word (key) has a definition (value). Dictionaries are essential for structured data.

```python
student = {
    "name": "Alex",
    "gpa": 3.8,
    "enrolled": True,
    "courses": ["Python", "Statistics"]
}
```

**Accessing values:**
```python
print(student["name"])        # Alex
print(student.get("gpa"))     # 3.8 (safer — won't crash if key missing)
print(student.get("age", 0))  # 0 (default if key missing)
```

**Modifying dictionaries:**
```python
student["age"] = 28           # Add new key or update existing
student["gpa"] = 3.9          # Update existing key
del student["enrolled"]       # Remove a key
```

**Iterating over dictionaries:**
```python
for key in student:
    print(key)

for key, value in student.items():
    print(f"{key}: {value}")

print(student.keys())    # All keys
print(student.values())  # All values
```

**Checking for keys:**
```python
if "name" in student:
    print("Name exists!")
```""",
            "reference": {
                "key_syntax": [
                    'dict["key"]  # access',
                    'dict.get("key", default)',
                    'dict["key"] = value  # set',
                    "dict.items() / .keys() / .values()",
                    '"key" in dict  # check'
                ],
                "notes": "Use .get() instead of [] when you're not sure a key exists — it won't throw an error."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": 'data = {"x": 10, "y": 20}; what is data["y"]?',
                    "options": ["10", "20", '"y"', "Error"],
                    "answer": 1,
                    "explanation": 'data["y"] looks up the key "y" and returns its value, which is 20.'
                },
                {
                    "type": "true_false",
                    "question": "Dictionaries maintain insertion order in Python 3.7+.",
                    "answer": True,
                    "explanation": "As of Python 3.7, dictionaries remember the order in which keys were inserted."
                },
                {
                    "type": "fill_blank",
                    "question": "Loop through key-value pairs in a dict called 'data'",
                    "template": "for key, value in data.___():\n    print(key, value)",
                    "answer": "items",
                    "explanation": ".items() returns each key-value pair as a tuple, which you can unpack into key and value."
                }
            ],
            "challenge": {
                "instructions": "Create a dictionary representing a course with keys: 'name', 'credits', 'grade' (a letter), and 'passed' (True if grade is not F). Then write a function called `course_summary` that takes a course dict and prints a formatted summary line.",
                "starter_code": "course = {\n    # Fill in the dictionary\n}\n\ndef course_summary(c):\n    # Print formatted summary\n    pass\n\ncourse_summary(course)\n",
                "tests": [
                    {"type": "runs_without_error"},
                    {"type": "code_contains", "value": "def course_summary"}
                ],
                "solution": 'course = {\n    "name": "Python Foundations",\n    "credits": 3,\n    "grade": "A",\n    "passed": True\n}\n\ndef course_summary(c):\n    print(f"{c[\'name\']} ({c[\'credits\']} credits) - Grade: {c[\'grade\']} - Passed: {c[\'passed\']}")\n\ncourse_summary(course)'
            }
        },
        {
            "id": "m1-l10",
            "title": "Putting It All Together — Mini Project",
            "order": 10,
            "duration_min": 30,
            "concept": """You've learned the building blocks of Python. Now let's combine everything into a real mini-project: a **Student Grade Calculator**.

This project uses:
- Variables and data types
- Dictionaries to store student data
- Lists to store grades
- Loops to process data
- Functions to organize code
- f-strings to format output
- If/else for grade classification

```python
def calculate_average(grades):
    return sum(grades) / len(grades)

def letter_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

students = [
    {"name": "Alice", "grades": [92, 88, 95, 91]},
    {"name": "Bob",   "grades": [74, 68, 81, 73]},
    {"name": "Carol", "grades": [85, 90, 88, 92]},
]

for student in students:
    avg = calculate_average(student["grades"])
    grade = letter_grade(avg)
    print(f"{student['name']:10} | Avg: {avg:.1f} | Grade: {grade}")
```

Output:
```
Alice      | Avg: 91.5 | Grade: A
Bob        | Avg: 74.0 | Grade: C
Carol      | Avg: 88.8 | Grade: B
```

Notice `{avg:.1f}` — this formats the float to 1 decimal place. And `{student['name']:10}` pads the name to 10 characters for alignment.""",
            "reference": {
                "key_syntax": [
                    "sum(list) / len(list)  # average",
                    "f'{value:.2f}'  # 2 decimal places",
                    "f'{value:10}'   # pad to 10 chars"
                ],
                "notes": "This mini-project combines all Module 1 concepts. Take your time!"
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "In f'{value:.2f}', what does .2f mean?",
                    "options": [
                        "2 significant figures",
                        "Float rounded to 2 decimal places",
                        "Multiply by 2",
                        "Format as integer"
                    ],
                    "answer": 1,
                    "explanation": ".2f formats the number as a float with 2 decimal places. .1f = 1 decimal, .3f = 3 decimals."
                },
                {
                    "type": "true_false",
                    "question": "You can access a list stored inside a dictionary with dict['key'][index].",
                    "answer": True,
                    "explanation": "You can chain access: dict['grades'] gives the list, then [0] gives the first item."
                }
            ],
            "challenge": {
                "instructions": "Build a grade report system. Given the list of students below, write code that: (1) calculates each student's average, (2) assigns a letter grade, (3) prints a formatted report, and (4) at the end prints the class average.",
                "starter_code": 'students = [\n    {"name": "Jordan", "grades": [88, 92, 79, 95, 84]},\n    {"name": "Taylor", "grades": [71, 65, 78, 69, 73]},\n    {"name": "Morgan", "grades": [95, 98, 92, 97, 96]},\n    {"name": "Casey",  "grades": [55, 62, 58, 70, 60]},\n]\n\n# Your code here\n',
                "tests": [
                    {"type": "output_contains", "value": "Jordan"},
                    {"type": "output_contains", "value": "Morgan"},
                    {"type": "code_contains", "value": "def"}
                ],
                "solution": 'students = [\n    {"name": "Jordan", "grades": [88, 92, 79, 95, 84]},\n    {"name": "Taylor", "grades": [71, 65, 78, 69, 73]},\n    {"name": "Morgan", "grades": [95, 98, 92, 97, 96]},\n    {"name": "Casey",  "grades": [55, 62, 58, 70, 60]},\n]\n\ndef avg(grades):\n    return sum(grades) / len(grades)\n\ndef letter(a):\n    if a >= 90: return "A"\n    elif a >= 80: return "B"\n    elif a >= 70: return "C"\n    elif a >= 60: return "D"\n    else: return "F"\n\nall_avgs = []\nfor s in students:\n    a = avg(s["grades"])\n    all_avgs.append(a)\n    print(f"{s[\'name\']:10} | {a:.1f} | {letter(a)}")\n\nprint(f"\\nClass average: {avg(all_avgs):.1f}")'
            }
        },
        {
            "id": "m1-l11",
            "title": "Tuples — Immutable Sequences",
            "order": 11,
            "duration_min": 20,
            "real_world_context": "As a business analyst, you'll use tuples to store fixed data like geographic coordinates, RGB color codes, or database records that should never be accidentally changed.",
            "concept": """A **tuple** is like a list, but it is **immutable** — once created, you cannot change it. This is a feature, not a limitation. When data should stay fixed (like a student's ID and name, or the (latitude, longitude) of an office location), a tuple communicates that intent to anyone reading your code.

```python
# Creating tuples
coordinates = (40.7128, -74.0060)   # New York City lat/lon
rgb_red     = (255, 0, 0)
student_id  = (10042, "Alice Chen")

# Tuples can also be created without parentheses (tuple packing)
point = 3, 7
print(point)        # (3, 7)
print(type(point))  # <class 'tuple'>
```

**Accessing tuple items** works exactly like lists — with indices:
```python
city = ("New York", "NY", 10001)
print(city[0])   # New York
print(city[-1])  # 10001
print(city[1:])  # ('NY', 10001)
```

**Tuple unpacking** is one of Python's most elegant features — assign each element to its own variable in a single line:
```python
name, state, zip_code = city
print(name)     # New York
print(zip_code) # 10001

# Swap two variables (classic Python trick using tuple unpacking)
a, b = 10, 20
a, b = b, a
print(a, b)   # 20 10
```

**Tuples vs Lists — when to use which:**
| Use a **tuple** when... | Use a **list** when... |
|-------------------------|------------------------|
| Data won't change       | Data will grow/shrink  |
| Fixed structure (x, y)  | Collection of similar items |
| Dictionary key needed   | Need .append()/.remove() |

Tuples are also slightly faster than lists and can be used as dictionary keys (lists cannot). In data pipelines you'll often receive database rows as tuples.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Store quarterly revenue as a tuple and unpack it

quarterly_revenue = (125_000, 148_000, 132_000, 170_000)

q1, q2, q3, q4 = quarterly_revenue

total   = sum(quarterly_revenue)
average = total / len(quarterly_revenue)
best_q  = quarterly_revenue.index(max(quarterly_revenue)) + 1  # +1 because index is 0-based

print(f"Total revenue:   ${total:,}")
print(f"Average quarter: ${average:,.0f}")
print(f"Best quarter:    Q{best_q}")
""",
                "explanation": "We create a tuple of four revenue figures. Tuple unpacking assigns each quarter to its own variable. sum() and len() work on tuples just like lists. .index() finds the position of the maximum value; we add 1 to convert from 0-based index to human quarter number."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "t = (a, b, c)  # create tuple",
                    "a, b, c = t   # unpack tuple",
                    "t[0]          # access by index",
                    "len(t), sum(t), max(t), min(t)",
                    "t.count(x)    # how many times x appears",
                    "t.index(x)    # index of first x"
                ],
                "notes": "Tuples are immutable — t[0] = 99 raises TypeError. A single-element tuple needs a trailing comma: t = (42,)"
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which of the following creates a valid single-element tuple?",
                    "options": ["A. t = (42)", "B. t = (42,)", "C. t = [42]", "D. t = {42}"],
                    "answer": 1,
                    "explanation": "(42) is just parentheses around an integer — Python sees it as the number 42. You need a trailing comma: (42,) to make it a tuple."
                },
                {
                    "type": "true_false",
                    "question": "You can use a tuple as a dictionary key, but you cannot use a list as a dictionary key.",
                    "answer": True,
                    "explanation": "Dictionary keys must be immutable (hashable). Tuples are immutable so they can be keys; lists are mutable so they cannot."
                },
                {
                    "type": "fill_blank",
                    "question": "Unpack the tuple point = (10, 20) into variables x and y in one line.",
                    "template": "___, ___ = point",
                    "answer": "x, y",
                    "explanation": "Tuple unpacking assigns each element to a variable in the same positional order."
                }
            ],
            "challenge": {
                "instructions": "You have a tuple of monthly sales figures for the first half of the year. Unpack it into six individual month variables, calculate the total and average, and print a summary showing total sales, average monthly sales (rounded to 2 decimal places), and which month number had the highest sales.",
                "starter_code": "monthly_sales = (42000, 38500, 51000, 47200, 53800, 49600)\n\n# Unpack into jan, feb, mar, apr, may, jun\n\n# Calculate total and average\n\n# Find the month number with highest sales (1-6)\n\n# Print summary\n",
                "tests": [
                    {"type": "output_contains", "value": "282100"},
                    {"type": "output_contains", "value": "47016.67"}
                ],
                "solution": """monthly_sales = (42000, 38500, 51000, 47200, 53800, 49600)

jan, feb, mar, apr, may, jun = monthly_sales

total   = sum(monthly_sales)
average = round(total / len(monthly_sales), 2)
best_month = monthly_sales.index(max(monthly_sales)) + 1

print(f"Total sales:   ${total:,}")
print(f"Average month: ${average:,}")
print(f"Best month:    Month {best_month}")
"""
            },
            "challenge_variations": [
                "Variation 1: Store a product's (name, price, stock_qty) as a tuple and print a formatted inventory line.",
                "Variation 2: Given a tuple of temperatures for 7 days, find the highest, lowest, and daily average.",
                "Variation 3: Use tuple unpacking to swap the values of two variables without a temporary variable.",
                "Variation 4: Create a list of (student_name, gpa) tuples and sort them by GPA.",
                "Variation 5: Store an address as a (street, city, state, zip) tuple and format it as a mailing label.",
                "Variation 6: Given a tuple of exam scores, count how many are above the class average.",
                "Variation 7: Use a tuple as a dictionary key to map (row, column) grid positions to cell values.",
                "Variation 8: Unpack a tuple of (first_name, last_name, age) returned from a function.",
                "Variation 9: Compare two (year, month, day) date tuples to find the earlier one without importing datetime.",
                "Variation 10: Given a tuple of quarterly budgets, compute the percentage each quarter represents of the annual total."
            ]
        },
        {
            "id": "m1-l12",
            "title": "Sets — Unique Collections",
            "order": 12,
            "duration_min": 20,
            "real_world_context": "Business analysts use sets constantly for data cleaning — finding unique customers, removing duplicate entries, checking which items appear in two different datasets (like which products are in both this year's and last year's catalog).",
            "concept": """A **set** is an unordered collection of **unique** items. If you add the same value twice, the set keeps only one copy. This makes sets perfect for deduplication and membership testing.

```python
# Creating a set
tags = {"python", "data", "analytics", "python"}  # duplicate ignored
print(tags)   # {'analytics', 'data', 'python'}  (order not guaranteed)

# Convert a list to a set to remove duplicates
responses = ["yes", "no", "yes", "maybe", "no", "yes"]
unique_responses = set(responses)
print(unique_responses)  # {'maybe', 'no', 'yes'}
print(len(unique_responses))  # 3
```

**Adding and removing items:**
```python
skills = {"python", "sql", "excel"}
skills.add("tableau")       # add one item
skills.discard("excel")     # remove if present (no error if missing)
skills.remove("sql")        # remove — raises KeyError if missing
print(skills)  # {'python', 'tableau'}
```

**Set operations — the real power:**
```python
team_a = {"Alice", "Bob", "Carol"}
team_b = {"Bob", "Carol", "Dave"}

# Union — everyone in either team
print(team_a | team_b)          # {'Alice', 'Bob', 'Carol', 'Dave'}

# Intersection — only in BOTH teams
print(team_a & team_b)          # {'Bob', 'Carol'}

# Difference — in team_a but NOT in team_b
print(team_a - team_b)          # {'Alice'}

# Symmetric difference — in one but not both
print(team_a ^ team_b)          # {'Alice', 'Dave'}
```

**Real data-analytics use case:** You have last month's customer IDs and this month's. Who is new? Who churned?
```python
last_month = {101, 102, 103, 104, 105}
this_month = {102, 103, 105, 106, 107}

new_customers     = this_month - last_month   # {106, 107}
churned_customers = last_month - this_month   # {101, 104}
retained          = last_month & this_month   # {102, 103, 105}
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Analyze course enrollment overlap

spring_courses = {"Python", "Statistics", "SQL", "Marketing"}
fall_courses   = {"Python", "SQL", "Finance", "Machine Learning"}

# Courses offered in both semesters
both_semesters = spring_courses & fall_courses
print(f"Offered both semesters: {both_semesters}")

# All unique courses across both semesters
all_courses = spring_courses | fall_courses
print(f"Total unique courses: {len(all_courses)}")

# Courses only in spring (not repeated in fall)
spring_only = spring_courses - fall_courses
print(f"Spring-only courses: {spring_only}")
""",
                "explanation": "& finds the intersection (courses in both), | finds the union (all courses combined with no duplicates), and - finds the difference (spring courses that don't appear in fall)."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    "s = {a, b, c}       # create set",
                    "s = set(list)       # from list",
                    "s.add(x)            # add item",
                    "s.discard(x)        # safe remove",
                    "A | B  # union",
                    "A & B  # intersection",
                    "A - B  # difference",
                    "x in s # membership test (very fast)"
                ],
                "notes": "Sets are unordered — you cannot index them with s[0]. Use a list if order matters. Sets cannot contain mutable items like lists."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What is the result of {1, 2, 3} & {2, 3, 4}?",
                    "options": ["A. {1, 2, 3, 4}", "B. {2, 3}", "C. {1, 4}", "D. {1, 2, 3, 2, 3, 4}"],
                    "answer": 1,
                    "explanation": "& is intersection — elements that appear in BOTH sets. 2 and 3 appear in both, so the result is {2, 3}."
                },
                {
                    "type": "true_false",
                    "question": "s = {1, 2, 2, 3, 3, 3}; len(s) equals 3.",
                    "answer": True,
                    "explanation": "Sets only store unique values. Duplicates are automatically removed, leaving {1, 2, 3} with length 3."
                },
                {
                    "type": "fill_blank",
                    "question": "Get all items that are in set A OR set B (union).",
                    "template": "result = A ___ B",
                    "answer": "|",
                    "explanation": "The | operator computes the union of two sets — all unique elements from both."
                }
            ],
            "challenge": {
                "instructions": "You have two lists of student IDs — those who submitted Assignment 1 and those who submitted Assignment 2. Using sets, find: (1) students who submitted BOTH assignments, (2) students who submitted ONLY Assignment 1, (3) students who submitted ONLY Assignment 2, and (4) students who submitted AT LEAST ONE assignment. Print each result with a descriptive label.",
                "starter_code": "assignment1 = [101, 102, 103, 105, 107, 108, 110]\nassignment2 = [101, 103, 104, 106, 107, 109, 110]\n\n# Convert to sets\n\n# Find each group\n\n# Print results\n",
                "tests": [
                    {"type": "output_contains", "value": "101"},
                    {"type": "output_contains", "value": "102"}
                ],
                "solution": """assignment1 = [101, 102, 103, 105, 107, 108, 110]
assignment2 = [101, 103, 104, 106, 107, 109, 110]

s1 = set(assignment1)
s2 = set(assignment2)

both        = s1 & s2
only_a1     = s1 - s2
only_a2     = s2 - s1
at_least_one = s1 | s2

print(f"Submitted both:        {sorted(both)}")
print(f"Only Assignment 1:     {sorted(only_a1)}")
print(f"Only Assignment 2:     {sorted(only_a2)}")
print(f"At least one:          {sorted(at_least_one)}")
"""
            },
            "challenge_variations": [
                "Variation 1: Given a list of survey answers, count how many unique responses there are.",
                "Variation 2: Find which products appear in both a supplier catalog and your store's inventory.",
                "Variation 3: Given two email lists, find contacts who appear in both (duplicates to avoid re-emailing).",
                "Variation 4: Remove all duplicate entries from a list of transaction IDs using a set.",
                "Variation 5: Check if every required field name is present in a dataset's column set.",
                "Variation 6: Find all unique words in a paragraph of text.",
                "Variation 7: Given attendee lists for two events, find people who went to neither event.",
                "Variation 8: Determine which cities appear in a sales dataset but not in a shipping-zone dataset.",
                "Variation 9: Use a set to track which student IDs you have already processed in a loop.",
                "Variation 10: Find the symmetric difference between this quarter's and last quarter's top-10 product SKUs."
            ]
        },
        {
            "id": "m1-l13",
            "title": "File I/O — Reading and Writing Files",
            "order": 13,
            "duration_min": 25,
            "real_world_context": "Almost every real data analytics task starts with reading a file — CSVs from accounting, logs from web servers, reports from databases. Knowing how to read and write files in Python is a fundamental job skill.",
            "concept": """Python can read and write files on your computer. The built-in `open()` function is the gateway.

**Opening and reading a text file:**
```python
# The with statement automatically closes the file when done — always use it
with open("students.txt", "r") as f:   # "r" = read mode
    content = f.read()                  # entire file as one string
    print(content)
```

The `"r"` is the **mode**:
| Mode | Meaning |
|------|---------|
| `"r"` | Read (file must exist) |
| `"w"` | Write (creates file; overwrites if it exists) |
| `"a"` | Append (adds to end of existing file) |
| `"x"` | Create (fails if file already exists) |

**Reading line by line** (memory-efficient for large files):
```python
with open("students.txt", "r") as f:
    for line in f:
        print(line.strip())   # .strip() removes the newline character
```

**Writing to a file:**
```python
lines = ["Alice,92", "Bob,78", "Carol,85"]

with open("grades.txt", "w") as f:
    for line in lines:
        f.write(line + "\\n")   # \\n is the newline character
```

**Working with CSV files** using the built-in `csv` module:
```python
import csv

# Writing a CSV
students = [
    ["Name", "Score", "Grade"],
    ["Alice", 92, "A"],
    ["Bob", 78, "C"],
]
with open("report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)

# Reading a CSV
with open("report.csv", "r") as f:
    reader = csv.DictReader(f)   # each row becomes a dict
    for row in reader:
        print(row["Name"], row["Score"])
```

In your MS program, you'll mostly use pandas to read CSVs (one line: `pd.read_csv("file.csv")`), but understanding the underlying file operations helps you debug and handle edge cases.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import csv

# Worked example: Write a sales report CSV then read it back

sales_data = [
    {"product": "Laptop",  "units": 12, "revenue": 14400},
    {"product": "Monitor", "units": 25, "revenue":  7500},
    {"product": "Keyboard","units": 50, "revenue":  2500},
]

# Write the CSV
with open("sales_report.csv", "w", newline="") as f:
    fieldnames = ["product", "units", "revenue"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sales_data)

print("File written.")

# Read it back and compute totals
total_revenue = 0
with open("sales_report.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_revenue += int(row["revenue"])
        print(f"  {row['product']:10} — ${int(row['revenue']):,}")

print(f"Total revenue: ${total_revenue:,}")
""",
                "explanation": "csv.DictWriter writes each dict as a row using the field names as column headers. csv.DictReader reads each row back as a dict, so you access values by column name. We cast row['revenue'] to int because CSV values are always read as strings."
            },
            "difficulty": "beginner",
            "reference": {
                "key_syntax": [
                    'open("path", "r/w/a") as f',
                    "f.read()         # whole file",
                    "f.readlines()    # list of lines",
                    "f.write(string)",
                    "import csv",
                    "csv.reader(f) / csv.DictReader(f)",
                    "csv.writer(f) / csv.DictWriter(f, fieldnames)"
                ],
                "notes": "Always use 'with open(...)' — it guarantees the file is closed even if an error occurs. CSV values are always read as strings; convert with int() or float() as needed."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which file mode would you use to ADD new lines to an existing log file without deleting what's already there?",
                    "options": ["A. 'r'", "B. 'w'", "C. 'a'", "D. 'x'"],
                    "answer": 2,
                    "explanation": "'a' (append) mode adds content to the end of an existing file. 'w' would overwrite and erase the existing content."
                },
                {
                    "type": "true_false",
                    "question": "When you read a CSV file with csv.DictReader, each row is returned as a Python dictionary.",
                    "answer": True,
                    "explanation": "DictReader uses the header row as keys and each subsequent row's values as dict values, so every row comes back as a dict."
                },
                {
                    "type": "fill_blank",
                    "question": "Complete the with-statement to open 'data.txt' for reading.",
                    "template": "with open('data.txt', ___) as f:",
                    "answer": "'r'",
                    "explanation": "'r' is the read mode. You can also omit the mode entirely since 'r' is the default, but being explicit is good practice."
                }
            ],
            "challenge": {
                "instructions": "Write a program that: (1) creates a list of at least 3 student dicts with 'name', 'score', and 'grade' keys, (2) writes them to a CSV file called 'class_grades.csv', (3) reads the file back, and (4) prints each student's name and score, plus the class average score at the end.",
                "starter_code": "import csv\n\nstudents = [\n    # Add at least 3 students\n]\n\n# Write to CSV\n\n# Read back and compute average\n",
                "tests": [
                    {"type": "code_contains", "value": "csv"},
                    {"type": "code_contains", "value": "with open"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import csv

students = [
    {"name": "Alice",  "score": 92, "grade": "A"},
    {"name": "Bob",    "score": 78, "grade": "C"},
    {"name": "Carol",  "score": 85, "grade": "B"},
    {"name": "David",  "score": 91, "grade": "A"},
]

with open("class_grades.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "score", "grade"])
    writer.writeheader()
    writer.writerows(students)

total = 0
count = 0
with open("class_grades.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']}: {row['score']}")
        total += int(row["score"])
        count += 1

print(f"Class average: {total / count:.1f}")
"""
            },
            "challenge_variations": [
                "Variation 1: Read a text file of product names (one per line) and print them numbered.",
                "Variation 2: Write a program that appends a new log entry (timestamp + message) to a log file each time it runs.",
                "Variation 3: Count how many lines are in a text file without loading the whole file into memory at once.",
                "Variation 4: Read a CSV of transactions and sum the 'amount' column.",
                "Variation 5: Write a CSV of the multiplication table (rows 1–10, columns 1–10).",
                "Variation 6: Read a file, convert all text to uppercase, and write it to a new file.",
                "Variation 7: Given a CSV with a 'category' column, group rows by category and count each.",
                "Variation 8: Find and print all lines in a text file that contain the word 'error'.",
                "Variation 9: Read a CSV, filter rows where a numeric column exceeds a threshold, and write filtered rows to a new CSV.",
                "Variation 10: Write each student's report card to a separate text file named after the student."
            ]
        },
        {
            "id": "m1-l14",
            "title": "Error Handling — try/except/finally",
            "order": 14,
            "duration_min": 20,
            "real_world_context": "Production data is messy — files go missing, users enter bad values, API calls fail. Error handling is what separates a fragile script from a professional tool that keeps running and tells you clearly what went wrong.",
            "concept": """When Python hits an error it raises an **exception** and stops. The `try/except` block lets you **catch** that exception and decide what to do instead.

```python
# Without error handling — crashes on bad input
number = int("abc")   # ValueError: invalid literal for int()

# With error handling — graceful fallback
try:
    number = int("abc")
except ValueError:
    print("That's not a valid number!")
    number = 0
```

**Common exception types:**
| Exception | When it happens |
|-----------|----------------|
| `ValueError` | Wrong value type (`int("abc")`) |
| `TypeError` | Wrong data type (`"hi" + 5`) |
| `KeyError` | Dict key doesn't exist (`d["missing"]`) |
| `IndexError` | List index out of range (`lst[99]`) |
| `FileNotFoundError` | File doesn't exist |
| `ZeroDivisionError` | Dividing by zero |

**Catching multiple exceptions:**
```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Both arguments must be numbers!")
        return None
    else:
        return result   # runs only if no exception occurred
```

**The finally block** — always runs, regardless of errors:
```python
def read_config(filename):
    f = None
    try:
        f = open(filename, "r")
        return f.read()
    except FileNotFoundError:
        print(f"Config file '{filename}' not found — using defaults.")
        return ""
    finally:
        if f:
            f.close()   # always close the file, even if an error occurred
```

**Raising your own exceptions:**
```python
def set_age(age):
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is not realistic.")
    return age
```

Think of try/except like a safety net — you try the risky thing, and if it fails you land softly instead of crashing.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Safe grade input processor

def parse_grade(raw_input):
    \"\"\"Convert a string input to a valid grade 0-100, or return None.\"\"\"
    try:
        grade = float(raw_input)
    except ValueError:
        print(f"  ERROR: '{raw_input}' is not a number — skipping.")
        return None

    if grade < 0 or grade > 100:
        print(f"  ERROR: {grade} is out of range 0-100 — skipping.")
        return None

    return grade

raw_grades = ["85", "92.5", "abc", "110", "78", "-5", "95"]
valid_grades = []

for raw in raw_grades:
    result = parse_grade(raw)
    if result is not None:
        valid_grades.append(result)

print(f"Valid grades: {valid_grades}")
print(f"Average: {sum(valid_grades) / len(valid_grades):.1f}")
""",
                "explanation": "parse_grade wraps float() in a try/except to catch non-numeric strings. A second check handles numbers that are out of the valid range. The main loop collects only valid grades. This pattern — validate input, collect results, compute — is standard in data cleaning."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "try: ... except ExceptionType: ...",
                    "except (TypeError, ValueError): ...",
                    "else: ...   # runs if no exception",
                    "finally: ... # always runs",
                    "raise ValueError('message')",
                    "except Exception as e: print(e)"
                ],
                "notes": "Avoid bare 'except:' with no type — it catches everything including keyboard interrupts. Always name the specific exception type you expect."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Which exception is raised when you try to access a dictionary key that doesn't exist?",
                    "options": ["A. IndexError", "B. ValueError", "C. KeyError", "D. TypeError"],
                    "answer": 2,
                    "explanation": "KeyError is raised when you use dict['key'] and the key is not in the dictionary. Use .get() to avoid this."
                },
                {
                    "type": "true_false",
                    "question": "The finally block runs only when an exception occurs.",
                    "answer": False,
                    "explanation": "finally ALWAYS runs — whether an exception occurred or not. It's used for cleanup code like closing files or database connections."
                },
                {
                    "type": "fill_blank",
                    "question": "Complete the code to catch a ZeroDivisionError.",
                    "template": "try:\n    result = 10 / 0\n___ ZeroDivisionError:\n    print('Cannot divide by zero')",
                    "answer": "except",
                    "explanation": "The 'except' keyword followed by the exception type catches that specific error."
                }
            ],
            "challenge": {
                "instructions": "Write a function called `safe_stats(data)` that takes a list of raw values (which may contain non-numeric strings), converts each to a float using try/except to skip invalid entries, and returns a dict with keys 'count', 'mean', 'minimum', and 'maximum'. If no valid numbers exist, return None. Test it with the provided data list.",
                "starter_code": "def safe_stats(data):\n    valid = []\n    for item in data:\n        # Try to convert each item to float\n        pass\n    \n    # If no valid numbers, return None\n    \n    # Return stats dict\n    pass\n\nraw_data = [\"12.5\", \"error\", \"8.0\", \"N/A\", \"15.2\", \"9.8\", \"bad\", \"11.1\"]\nresult = safe_stats(raw_data)\nprint(result)\n",
                "tests": [
                    {"type": "output_contains", "value": "count"},
                    {"type": "output_contains", "value": "mean"},
                    {"type": "runs_without_error"}
                ],
                "solution": """def safe_stats(data):
    valid = []
    for item in data:
        try:
            valid.append(float(item))
        except (ValueError, TypeError):
            pass  # skip invalid entries

    if not valid:
        return None

    return {
        "count":   len(valid),
        "mean":    round(sum(valid) / len(valid), 2),
        "minimum": min(valid),
        "maximum": max(valid),
    }

raw_data = ["12.5", "error", "8.0", "N/A", "15.2", "9.8", "bad", "11.1"]
result = safe_stats(raw_data)
print(result)
"""
            },
            "challenge_variations": [
                "Variation 1: Wrap a file-open operation so it prints a friendly message if the file is missing.",
                "Variation 2: Write a function that safely looks up a key in a dict and returns a default value if the key is absent.",
                "Variation 3: Handle a ZeroDivisionError when computing a percentage if the total is 0.",
                "Variation 4: Validate that a user-supplied date string matches YYYY-MM-DD format using try/except.",
                "Variation 5: Write a loop that retries an operation up to 3 times before giving up.",
                "Variation 6: Use raise to enforce that a function argument is a positive number.",
                "Variation 7: Parse a CSV row and skip any row where a required column is missing or empty.",
                "Variation 8: Catch a TypeError when someone accidentally passes a string to a math function.",
                "Variation 9: Use finally to print 'Processing complete' whether or not an error occurred.",
                "Variation 10: Write a safe int-conversion function that returns 0 for any non-integer input."
            ]
        },
        {
            "id": "m1-l15",
            "title": "Classes Part 1 — Objects and Attributes",
            "order": 15,
            "duration_min": 25,
            "real_world_context": "In a business analytics program, you'll model real-world entities — students, transactions, products, customers — as objects. Classes are the template; objects are the individual instances. This is how pandas DataFrames, scikit-learn models, and every major Python library is built.",
            "concept": """**Object-Oriented Programming (OOP)** is a way of organizing code around *things* (objects) instead of just *actions*. A **class** is a blueprint; an **object** is a specific instance of that blueprint.

Think of it like this: "Student" is a class (the blueprint). "Alice with GPA 3.8 enrolled in Python" is an object (a specific student).

```python
class Student:
    def __init__(self, name, gpa, major):
        self.name  = name    # instance attribute
        self.gpa   = gpa
        self.major = major

# Create instances (objects)
alice = Student("Alice", 3.8, "Business Analytics")
bob   = Student("Bob",   3.2, "Finance")

print(alice.name)   # Alice
print(bob.gpa)      # 3.2
```

**Breaking down `__init__`:**
- `__init__` is the **constructor** — it runs automatically when you create a new object
- `self` refers to the specific instance being created (like saying "this particular student")
- `self.name = name` stores the value as an **instance attribute** on the object

**You can set attributes after creation too:**
```python
alice.email = "alice@university.edu"   # add new attribute
alice.gpa   = 3.9                       # update existing attribute
print(alice.email)   # alice@university.edu
```

**Class attributes** are shared by ALL instances (vs instance attributes which are unique per object):
```python
class Student:
    school = "State University"    # class attribute — same for all

    def __init__(self, name, gpa):
        self.name = name           # instance attribute — unique per student
        self.gpa  = gpa

s = Student("Alice", 3.8)
print(s.school)          # State University  (from class)
print(Student.school)    # State University  (same thing)
```

**Why use classes?** Instead of keeping a student's data in three separate variables (`name`, `gpa`, `major`), a class bundles it all into one object that you can pass around, store in lists, and operate on consistently. This is exactly how pandas keeps a DataFrame's data, index, and methods together.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Product class for an inventory system

class Product:
    category_tax_rate = 0.08   # class attribute: 8% tax for all products

    def __init__(self, name, price, stock):
        self.name  = name
        self.price = price
        self.stock = stock

    def total_value(self):
        \"\"\"Return the total inventory value (price × stock).\"\"\"
        return self.price * self.stock

    def price_with_tax(self):
        \"\"\"Return price including tax.\"\"\"
        return round(self.price * (1 + self.category_tax_rate), 2)


laptop  = Product("Laptop", 1200.00, 15)
monitor = Product("Monitor", 350.00, 40)

print(f"{laptop.name}: ${laptop.price_with_tax()} (tax included)")
print(f"Inventory value: ${laptop.total_value():,.2f}")
print(f"{monitor.name} stock: {monitor.stock} units")
""",
                "explanation": "__init__ stores name, price, and stock on each instance via self. total_value() and price_with_tax() are methods that operate on the instance's own data using self. category_tax_rate is a class attribute accessed via self inside the method."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "class ClassName:",
                    "    def __init__(self, param):",
                    "        self.attr = param",
                    "obj = ClassName(arg)",
                    "obj.attribute      # read attribute",
                    "obj.attribute = v  # set attribute",
                    "ClassName.class_attr  # class-level attribute"
                ],
                "notes": "self is always the first parameter of any method but you never pass it when calling — Python passes it automatically. __init__ is called the constructor."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What is the purpose of __init__ in a class?",
                    "options": [
                        "A. It deletes the object when it's no longer needed",
                        "B. It runs automatically when a new object is created and sets up its attributes",
                        "C. It prints the object's data",
                        "D. It is called only once when the program starts"
                    ],
                    "answer": 1,
                    "explanation": "__init__ is the constructor — it runs the moment you create a new instance (e.g., Student('Alice', 3.8)) and initializes that object's attributes."
                },
                {
                    "type": "true_false",
                    "question": "Two instances of the same class always share the same attribute values.",
                    "answer": False,
                    "explanation": "Each instance has its own copy of instance attributes. alice.gpa and bob.gpa can be completely different values even though both are Student objects."
                },
                {
                    "type": "fill_blank",
                    "question": "Inside __init__, how do you store the parameter 'name' as an instance attribute?",
                    "template": "def __init__(self, name):\n    ___.___ = name",
                    "answer": "self.name",
                    "explanation": "self.name = name creates an instance attribute called 'name' on this specific object."
                }
            ],
            "challenge": {
                "instructions": "Create a class called `Course` with instance attributes: `title` (string), `credits` (int), `instructor` (string), and `enrolled_students` (int, default 0). Add a class attribute `max_capacity = 30`. Create at least two Course instances and print their details. Bonus: add an `is_full` method that returns True if enrolled_students >= max_capacity.",
                "starter_code": "class Course:\n    max_capacity = 30\n\n    def __init__(self, title, credits, instructor):\n        # Set instance attributes\n        pass\n\n    def is_full(self):\n        # Return True if at capacity\n        pass\n\n# Create two courses and print their info\n",
                "tests": [
                    {"type": "code_contains", "value": "class Course"},
                    {"type": "code_contains", "value": "__init__"},
                    {"type": "runs_without_error"}
                ],
                "solution": """class Course:
    max_capacity = 30

    def __init__(self, title, credits, instructor, enrolled_students=0):
        self.title             = title
        self.credits           = credits
        self.instructor        = instructor
        self.enrolled_students = enrolled_students

    def is_full(self):
        return self.enrolled_students >= self.max_capacity


python_course = Course("Python Foundations", 3, "Dr. Smith", 25)
stats_course  = Course("Applied Statistics", 4, "Dr. Jones", 30)

print(f"{python_course.title} — {python_course.enrolled_students}/{python_course.max_capacity} students — Full: {python_course.is_full()}")
print(f"{stats_course.title}  — {stats_course.enrolled_students}/{stats_course.max_capacity} students — Full: {stats_course.is_full()}")
"""
            },
            "challenge_variations": [
                "Variation 1: Create a BankAccount class with owner and balance attributes and a deposit() method.",
                "Variation 2: Model a Product with name, price, and quantity; add a total_value() method.",
                "Variation 3: Build an Employee class that stores name, department, and salary.",
                "Variation 4: Create a Rectangle class with width and height; add area() and perimeter() methods.",
                "Variation 5: Model a survey Response with respondent_id, answers (list), and a score() method.",
                "Variation 6: Create a simple Inventory item with SKU, description, and reorder_threshold.",
                "Variation 7: Build a Meeting class with title, date, and attendees (list); add an add_attendee() method.",
                "Variation 8: Model a Student with a grades list and compute their GPA inside the class.",
                "Variation 9: Create a SalesRep class that tracks name, region, and a list of sales amounts.",
                "Variation 10: Build a simple Timer class that stores a start_time and has an elapsed() method."
            ]
        },
        {
            "id": "m1-l16",
            "title": "Classes Part 2 — Methods and Inheritance",
            "order": 16,
            "duration_min": 25,
            "real_world_context": "Every pandas DataFrame is an object with methods like .describe() and .groupby(). Every scikit-learn model has .fit() and .predict(). Understanding how methods and inheritance work helps you use these tools confidently and build your own reusable components.",
            "concept": """In Part 1 you learned how to create objects with attributes. Now let's give them **behavior** through methods, and learn how classes can **inherit** from each other.

**Instance methods** are functions that belong to a class and always receive `self` as their first argument:
```python
class Student:
    def __init__(self, name, grades):
        self.name   = name
        self.grades = grades

    def average(self):
        return sum(self.grades) / len(self.grades)

    def letter_grade(self):
        avg = self.average()     # a method can call another method
        if avg >= 90: return "A"
        elif avg >= 80: return "B"
        elif avg >= 70: return "C"
        else: return "F"

alice = Student("Alice", [88, 95, 92, 90])
print(alice.average())       # 91.25
print(alice.letter_grade())  # A
```

**__str__ — the string representation method:**
```python
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa  = gpa

    def __str__(self):
        return f"Student({self.name}, GPA: {self.gpa})"

s = Student("Alice", 3.8)
print(s)   # Student(Alice, GPA: 3.8)
```
Without `__str__`, `print(s)` shows something like `<__main__.Student object at 0x10f3a>`. Defining `__str__` makes your object human-readable.

**Inheritance** — one class extending another:
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def greet(self):
        return f"Hi, I'm {self.name}."

class GraduateStudent(Person):   # inherits from Person
    def __init__(self, name, age, thesis_topic):
        super().__init__(name, age)   # call parent's __init__
        self.thesis_topic = thesis_topic

    def introduce(self):
        return f"{self.greet()} I'm researching {self.thesis_topic}."

gs = GraduateStudent("Alice", 26, "NLP in Finance")
print(gs.greet())      # Hi, I'm Alice.  (inherited from Person)
print(gs.introduce())  # Hi, I'm Alice. I'm researching NLP in Finance.
```

**Why this matters for data analytics:** You'll extend base classes constantly — e.g., building a custom transformer that inherits from scikit-learn's `BaseEstimator`. The pattern is always the same: call `super().__init__()`, then add your own attributes and methods.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Employee hierarchy with inheritance

class Employee:
    company = "Orion Analytics Inc."

    def __init__(self, name, salary):
        self.name   = name
        self.salary = salary

    def annual_cost(self):
        return self.salary * 12

    def __str__(self):
        return f"{self.name} (${self.salary:,}/mo)"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def budget_responsibility(self):
        # Manager's total cost includes their team (assume avg $5k/mo per report)
        return self.annual_cost() + self.team_size * 5000 * 12

    def __str__(self):
        base = super().__str__()
        return f"{base} — Manager of {self.team_size}"


emp  = Employee("Bob Smith", 6000)
mgr  = Manager("Carol Jones", 9000, 5)

print(emp)
print(mgr)
print(f"Carol's budget responsibility: ${mgr.budget_responsibility():,}")
""",
                "explanation": "Employee defines the base behavior. Manager calls super().__init__() to reuse the parent setup, then adds team_size. It also overrides __str__ using super().__str__() to get the base string and extend it. This avoids repeating code."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "def method_name(self): ...",
                    "def __str__(self): return '...'",
                    "class Child(Parent):",
                    "super().__init__(args)",
                    "super().method_name()"
                ],
                "notes": "Always call super().__init__() in a child class __init__ unless you have a specific reason not to. __str__ should return a string, not print one."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does super().__init__() do inside a child class?",
                    "options": [
                        "A. Creates a new parent class",
                        "B. Calls the parent class's __init__ to set up inherited attributes",
                        "C. Deletes the parent class",
                        "D. Returns the parent object"
                    ],
                    "answer": 1,
                    "explanation": "super().__init__() runs the parent class's constructor so that all the parent's attributes are properly initialized on the child object."
                },
                {
                    "type": "true_false",
                    "question": "A child class can call methods defined in the parent class without redefining them.",
                    "answer": True,
                    "explanation": "Inheritance means the child automatically has access to all the parent's methods and attributes. This is the whole point — code reuse."
                },
                {
                    "type": "fill_blank",
                    "question": "Which special method should you define to control what print(obj) displays?",
                    "template": "def ___(self):\n    return f'My object: {self.name}'",
                    "answer": "__str__",
                    "explanation": "__str__ is called by print() and str() to get a human-readable string representation of an object."
                }
            ],
            "challenge": {
                "instructions": "Create a base class `Animal` with attributes `name` and `sound`, and a `speak()` method that returns '{name} says {sound}'. Then create a subclass `Pet` that inherits from Animal and adds an `owner` attribute. Override `speak()` in Pet to return '{name} (owned by {owner}) says {sound}'. Add `__str__` to both classes. Create one Animal and one Pet instance and print them.",
                "starter_code": "class Animal:\n    def __init__(self, name, sound):\n        pass\n\n    def speak(self):\n        pass\n\n    def __str__(self):\n        pass\n\n\nclass Pet(Animal):\n    def __init__(self, name, sound, owner):\n        pass\n\n    def speak(self):\n        pass\n\n    def __str__(self):\n        pass\n\n\n# Create instances and print them\n",
                "tests": [
                    {"type": "code_contains", "value": "class Pet(Animal)"},
                    {"type": "code_contains", "value": "super()"},
                    {"type": "runs_without_error"}
                ],
                "solution": """class Animal:
    def __init__(self, name, sound):
        self.name  = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __str__(self):
        return f"Animal: {self.name}"


class Pet(Animal):
    def __init__(self, name, sound, owner):
        super().__init__(name, sound)
        self.owner = owner

    def speak(self):
        return f"{self.name} (owned by {self.owner}) says {self.sound}"

    def __str__(self):
        return f"Pet: {self.name}, Owner: {self.owner}"


lion = Animal("Lion", "ROAR")
dog  = Pet("Rex", "Woof", "Alice")

print(lion)
print(dog)
print(lion.speak())
print(dog.speak())
"""
            },
            "challenge_variations": [
                "Variation 1: Create a Vehicle base class and Car/Truck subclasses with type-specific attributes.",
                "Variation 2: Build a Shape base class with area() and a Circle and Rectangle subclass.",
                "Variation 3: Create an Account base class and SavingsAccount/CheckingAccount subclasses.",
                "Variation 4: Model a Person with a full_name() method and a Professor subclass with a teach() method.",
                "Variation 5: Build a Notification base class and EmailNotification/SMSNotification subclasses.",
                "Variation 6: Create a Report base class with generate() and a SalesReport subclass that adds a chart_data attribute.",
                "Variation 7: Extend your Student class from l15 with a GraduateStudent subclass that adds thesis_advisor.",
                "Variation 8: Build a DataSource base class and CSVDataSource/APIDataSource subclasses.",
                "Variation 9: Create an Offer base class and DiscountOffer/BundleOffer subclasses for an e-commerce system.",
                "Variation 10: Model a Task base class and RecurringTask subclass that adds a frequency attribute."
            ]
        },
        {
            "id": "m1-l17",
            "title": "Modules and Imports",
            "order": 17,
            "duration_min": 20,
            "real_world_context": "Python's standard library and the broader ecosystem (numpy, pandas, scikit-learn) are all modules. Knowing how to import and use them efficiently is how you leverage thousands of hours of other engineers' work in your own analyses.",
            "concept": """A **module** is just a Python file that contains functions, classes, and variables you can reuse. Python ships with a large **standard library** of built-in modules — no installation required.

**The import statement:**
```python
import math

print(math.pi)            # 3.141592653589793
print(math.sqrt(16))      # 4.0
print(math.ceil(3.2))     # 4  (round up)
print(math.floor(3.8))    # 3  (round down)
print(math.log(100, 10))  # 2.0  (log base 10)
```

**from ... import** — bring specific names into your namespace:
```python
from math import sqrt, pi

print(sqrt(25))   # 5.0  (no need for math.sqrt)
print(pi)         # 3.14...
```

**import ... as** — give a module an alias (very common in data science):
```python
import math as m
print(m.sqrt(9))   # 3.0

# The data-science convention you'll see everywhere:
import numpy as np           # by convention
import pandas as pd          # by convention
```

**Commonly used standard library modules:**
```python
import os
print(os.getcwd())            # current working directory
print(os.listdir("."))        # files in current directory
os.makedirs("output", exist_ok=True)  # create folder

import random
print(random.randint(1, 100)) # random integer 1–100
print(random.choice(["A","B","C"]))   # random item from list
random.shuffle(my_list)               # shuffle in place

import datetime
today = datetime.date.today()
print(today)                   # 2026-03-18

import json
data = {"name": "Alice", "score": 95}
text = json.dumps(data)        # dict → JSON string
back = json.loads(text)        # JSON string → dict
```

**Writing your own module:** Any `.py` file is a module. If you save functions in `helpers.py`, you can do `from helpers import my_function` in another file. This is how large projects stay organized.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """import random
import math
import os

# Worked example: Generate a random sample and compute stats

random.seed(42)   # set seed for reproducibility

sample = [random.gauss(75, 10) for _ in range(20)]   # 20 random exam scores
sample = [round(s, 1) for s in sample]

n    = len(sample)
mean = sum(sample) / n
variance = sum((x - mean) ** 2 for x in sample) / n
std_dev  = math.sqrt(variance)

print(f"Sample size: {n}")
print(f"Mean:        {mean:.2f}")
print(f"Std Dev:     {std_dev:.2f}")
print(f"Min / Max:   {min(sample)} / {max(sample)}")

# Save to a text file in current directory
output_path = os.path.join(os.getcwd(), "sample_stats.txt")
with open(output_path, "w") as f:
    f.write(f"mean={mean:.2f}, std={std_dev:.2f}\\n")
print(f"Stats saved to {output_path}")
""",
                "explanation": "random.seed(42) makes the random numbers reproducible. random.gauss generates normally-distributed values. math.sqrt computes the standard deviation. os.path.join safely builds a file path that works on any OS."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "import module_name",
                    "from module import name",
                    "import module as alias",
                    "math: sqrt, pi, ceil, floor, log",
                    "random: randint, choice, shuffle, seed",
                    "os: getcwd, listdir, makedirs, path.join",
                    "json: dumps, loads"
                ],
                "notes": "Standard library modules are built-in — no pip install needed. Third-party modules (numpy, pandas) must be installed first."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does 'import numpy as np' accomplish?",
                    "options": [
                        "A. Installs numpy on your computer",
                        "B. Imports numpy and lets you refer to it as np throughout your code",
                        "C. Creates a new module called np",
                        "D. Imports only the numpy.np submodule"
                    ],
                    "answer": 1,
                    "explanation": "'as np' creates an alias. Instead of typing numpy.array() every time, you type np.array(). This is a very common convention in data science."
                },
                {
                    "type": "true_false",
                    "question": "You can write your own module by simply saving Python code in a .py file and importing it.",
                    "answer": True,
                    "explanation": "Any .py file is a module. If utils.py has a function called clean_data, you can do 'from utils import clean_data' in another file in the same directory."
                },
                {
                    "type": "fill_blank",
                    "question": "Import only the sqrt function from the math module.",
                    "template": "___ math ___ sqrt",
                    "answer": "from ... import",
                    "explanation": "'from math import sqrt' brings only sqrt into your namespace, so you can call sqrt(16) directly."
                }
            ],
            "challenge": {
                "instructions": "Using the random and math modules: (1) set a seed of 99 for reproducibility, (2) generate a list of 15 random integers between 50 and 100, (3) compute the mean and standard deviation manually using math.sqrt, (4) use random.choice to pick a 'winner' from the list, and (5) print all results with clear labels.",
                "starter_code": "import random\nimport math\n\n# 1. Set seed\n\n# 2. Generate 15 random integers between 50 and 100\n\n# 3. Compute mean and std deviation\n\n# 4. Pick a random winner\n\n# 5. Print results\n",
                "tests": [
                    {"type": "code_contains", "value": "import random"},
                    {"type": "code_contains", "value": "import math"},
                    {"type": "code_contains", "value": "random.seed"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import random
import math

random.seed(99)

scores = [random.randint(50, 100) for _ in range(15)]

mean = sum(scores) / len(scores)
variance = sum((x - mean) ** 2 for x in scores) / len(scores)
std_dev = math.sqrt(variance)

winner = random.choice(scores)

print(f"Scores:    {scores}")
print(f"Mean:      {mean:.2f}")
print(f"Std Dev:   {std_dev:.2f}")
print(f"Winner:    {winner}")
"""
            },
            "challenge_variations": [
                "Variation 1: Use os to list all .py files in the current directory.",
                "Variation 2: Use json.dumps to convert a student record dict to a JSON string and print it.",
                "Variation 3: Use random.shuffle to randomize a list of team names for a tournament bracket.",
                "Variation 4: Use math.log to compute compound interest growth over 10 years.",
                "Variation 5: Use os.makedirs to create a project folder structure programmatically.",
                "Variation 6: Use random.sample to pick 5 unique prize winners from a list of entrants.",
                "Variation 7: Use json.loads to parse a JSON string and extract a nested value.",
                "Variation 8: Use math.ceil to calculate how many pages are needed to fit N items at K per page.",
                "Variation 9: Combine os and datetime to generate a timestamped output filename.",
                "Variation 10: Write your own utilities.py module with two helper functions and import it in a main script."
            ]
        },
        {
            "id": "m1-l18",
            "title": "Advanced List Comprehensions",
            "order": 18,
            "duration_min": 20,
            "real_world_context": "Data transformation is the core of analytics work — cleaning a column, reformatting records, filtering rows. Comprehensions let you express these transformations in one concise, readable line instead of five lines of boilerplate.",
            "concept": """You already know basic list comprehensions from Lesson 8. Now let's unlock their full power: dict comprehensions, set comprehensions, nested comprehensions, and conditional logic.

**Dict comprehensions — build a dict from a sequence:**
```python
names  = ["Alice", "Bob", "Carol"]
scores = [92, 78, 85]

# Map each name to their score
grade_map = {name: score for name, score in zip(names, scores)}
print(grade_map)  # {'Alice': 92, 'Bob': 78, 'Carol': 85}

# Square of each number as a dict
squares = {n: n**2 for n in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

**Set comprehensions:**
```python
words = ["hello", "world", "hello", "python", "world"]
unique_words = {word.lower() for word in words}
print(unique_words)  # {'hello', 'world', 'python'}
```

**Conditional comprehensions — filter inline:**
```python
scores = [88, 72, 95, 61, 90, 55, 83]

# Only passing scores
passing  = [s for s in scores if s >= 60]

# Letter grade for each passing score
graded   = {s: "A" if s >= 90 else "B" if s >= 80 else "C" for s in passing}
print(graded)  # {88: 'B', 72: 'C', 95: 'A', 61: 'C', 90: 'A', 83: 'B'}
```

**Nested comprehensions — flatten a 2D structure:**
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten to a 1D list
flat = [val for row in matrix for val in row]
print(flat)   # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# All cells above 5
above_five = [val for row in matrix for val in row if val > 5]
print(above_five)  # [6, 7, 8, 9]
```

**Readability rule:** If a comprehension needs more than one condition or two levels of nesting, a regular loop is often clearer. Comprehensions are a tool for conciseness, not a mandate.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Transform a product catalog

products = [
    {"name": "Laptop",   "price": 1200, "in_stock": True},
    {"name": "Monitor",  "price": 350,  "in_stock": False},
    {"name": "Keyboard", "price": 80,   "in_stock": True},
    {"name": "Mouse",    "price": 45,   "in_stock": True},
    {"name": "Webcam",   "price": 95,   "in_stock": False},
]

# Dict: name → discounted price (10% off) for in-stock items only
discounted = {
    p["name"]: round(p["price"] * 0.90, 2)
    for p in products
    if p["in_stock"]
}
print("In-stock discounted prices:")
for name, price in discounted.items():
    print(f"  {name}: ${price}")

# Set of unique price tiers (budget <100, mid 100-500, premium >500)
def tier(price):
    if price < 100:   return "budget"
    elif price <= 500: return "mid"
    else:              return "premium"

price_tiers = {tier(p["price"]) for p in products}
print(f"Price tiers represented: {price_tiers}")
""",
                "explanation": "The dict comprehension filters with 'if p[in_stock]' and transforms the price inline. The set comprehension calls a helper function inside the expression — comprehensions can call any function. Both are far more concise than equivalent for-loops."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "[expr for x in iterable]",
                    "[expr for x in iterable if condition]",
                    "{key: val for x in iterable}",
                    "{expr for x in iterable}  # set",
                    "[expr for row in matrix for val in row]  # nested",
                    "zip(list1, list2)  # pair up two lists"
                ],
                "notes": "Comprehensions create new collections — they never modify the original. zip() stops at the shorter list if they have unequal lengths."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does {k: v for k, v in pairs} create?",
                    "options": ["A. A list of tuples", "B. A set", "C. A dictionary", "D. A generator"],
                    "answer": 2,
                    "explanation": "Curly braces with key: value syntax inside a comprehension creates a dictionary. Plain curly braces with just a value create a set."
                },
                {
                    "type": "true_false",
                    "question": "[x for x in range(10) if x % 2 == 0] produces [0, 2, 4, 6, 8].",
                    "answer": True,
                    "explanation": "The 'if x % 2 == 0' filter keeps only even numbers. range(10) is 0–9, so the result is [0, 2, 4, 6, 8]."
                },
                {
                    "type": "fill_blank",
                    "question": "Use zip to pair names and scores into a dict in one line.",
                    "template": "result = {name: score for name, score in ___(names, scores)}",
                    "answer": "zip",
                    "explanation": "zip(names, scores) pairs up corresponding elements from both lists as tuples, which you then unpack into name and score."
                }
            ],
            "challenge": {
                "instructions": "You have a list of employee dicts with 'name', 'department', and 'salary'. Using comprehensions: (1) create a dict mapping name → salary for all employees earning above $70,000, (2) create a set of all unique departments, (3) create a list of names (uppercased) sorted alphabetically. Print all three results.",
                "starter_code": "employees = [\n    {\"name\": \"Alice\",   \"department\": \"Engineering\", \"salary\": 95000},\n    {\"name\": \"Bob\",     \"department\": \"Marketing\",   \"salary\": 68000},\n    {\"name\": \"Carol\",   \"department\": \"Engineering\", \"salary\": 88000},\n    {\"name\": \"David\",   \"department\": \"Finance\",     \"salary\": 72000},\n    {\"name\": \"Eve\",     \"department\": \"Marketing\",   \"salary\": 75000},\n    {\"name\": \"Frank\",   \"department\": \"Finance\",     \"salary\": 61000},\n]\n\n# 1. Dict: name → salary for salary > 70000\n\n# 2. Set of unique departments\n\n# 3. Sorted list of uppercased names\n\n# Print all three\n",
                "tests": [
                    {"type": "output_contains", "value": "Alice"},
                    {"type": "output_contains", "value": "Engineering"},
                    {"type": "runs_without_error"}
                ],
                "solution": """employees = [
    {"name": "Alice",   "department": "Engineering", "salary": 95000},
    {"name": "Bob",     "department": "Marketing",   "salary": 68000},
    {"name": "Carol",   "department": "Engineering", "salary": 88000},
    {"name": "David",   "department": "Finance",     "salary": 72000},
    {"name": "Eve",     "department": "Marketing",   "salary": 75000},
    {"name": "Frank",   "department": "Finance",     "salary": 61000},
]

high_earners = {e["name"]: e["salary"] for e in employees if e["salary"] > 70000}
departments  = {e["department"] for e in employees}
names_upper  = sorted([e["name"].upper() for e in employees])

print("High earners:", high_earners)
print("Departments:", departments)
print("Names:", names_upper)
"""
            },
            "challenge_variations": [
                "Variation 1: Create a dict of word → word_length for all words in a sentence.",
                "Variation 2: Filter a list of dicts to only those where a boolean flag is True using a list comprehension.",
                "Variation 3: Flatten a list of lists of student names into one sorted list.",
                "Variation 4: Use a dict comprehension to invert a dictionary (swap keys and values).",
                "Variation 5: Build a set of all unique first letters from a list of company names.",
                "Variation 6: Create a list of (name, score) tuples only for students who passed.",
                "Variation 7: Use a nested comprehension to generate a multiplication table as a list of lists.",
                "Variation 8: Build a dict mapping each category to the count of items in that category.",
                "Variation 9: Normalize a list of scores to 0–1 range using a list comprehension.",
                "Variation 10: Create a dict of product SKUs mapped to their discounted price using a comprehension."
            ]
        },
        {
            "id": "m1-l19",
            "title": "Lambda Functions",
            "order": 19,
            "duration_min": 18,
            "real_world_context": "You'll use lambda functions constantly with pandas: df.sort_values(key=lambda x: x.str.len()), df.apply(lambda row: ...), or with sorted() to sort complex data structures by a specific field.",
            "concept": """A **lambda function** is an anonymous (nameless) function defined in one line. It's used when you need a small throwaway function — usually as an argument to another function.

**Syntax:**
```python
# Regular function
def square(x):
    return x ** 2

# Equivalent lambda
square = lambda x: x ** 2

print(square(5))   # 25
```

The syntax is: `lambda parameters: expression`
- No `def`, no `return` keyword — the expression IS the return value
- Can take multiple parameters: `lambda x, y: x + y`

**The real use case — as an argument:**
```python
students = [
    {"name": "Alice", "gpa": 3.8},
    {"name": "Bob",   "gpa": 3.2},
    {"name": "Carol", "gpa": 3.9},
]

# Sort by GPA (descending)
ranked = sorted(students, key=lambda s: s["gpa"], reverse=True)
for s in ranked:
    print(s["name"], s["gpa"])
# Carol 3.9
# Alice 3.8
# Bob   3.2
```

**map() — apply a function to every item:**
```python
prices   = [10.0, 25.5, 8.0, 42.0]
with_tax = list(map(lambda p: round(p * 1.08, 2), prices))
print(with_tax)  # [10.8, 27.54, 8.64, 45.36]
```

**filter() — keep items where the function returns True:**
```python
scores   = [88, 72, 95, 61, 90, 55, 83]
passing  = list(filter(lambda s: s >= 60, scores))
print(passing)  # [88, 72, 95, 61, 90, 83]
```

**Lambda vs def — when to use which:**
| Use **lambda** | Use **def** |
|----------------|-------------|
| Simple one-liner | Multi-line logic |
| Passed as argument | Reused in multiple places |
| Sorting key | Needs a docstring |

In pandas you'll almost always use lambda with `.apply()`, `.sort_values(key=...)`, and `.groupby()`. Recognizing the pattern is more important than memorizing the syntax.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Rank and filter a product catalog

products = [
    {"name": "Laptop",   "price": 1200, "rating": 4.5},
    {"name": "Monitor",  "price": 350,  "rating": 4.7},
    {"name": "Keyboard", "price": 80,   "rating": 4.2},
    {"name": "Mouse",    "price": 45,   "rating": 4.8},
    {"name": "Webcam",   "price": 95,   "rating": 3.9},
]

# Filter: only products rated 4.5 or above
top_rated = list(filter(lambda p: p["rating"] >= 4.5, products))

# Sort top-rated by price (cheapest first)
top_rated_sorted = sorted(top_rated, key=lambda p: p["price"])

# Map: add a 'value_score' = rating / (price / 100)
for p in top_rated_sorted:
    p["value_score"] = round(p["rating"] / (p["price"] / 100), 3)

for p in top_rated_sorted:
    print(f"{p['name']:10} ${p['price']:>6} rating {p['rating']} value_score {p['value_score']}")
""",
                "explanation": "filter() keeps only items where the lambda returns True. sorted() uses a lambda as the key to extract the field to sort by. The final loop adds a computed field to each dict using inline arithmetic. No named functions needed — all logic is concise and inline."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "lambda x: expression",
                    "lambda x, y: expression",
                    "sorted(iterable, key=lambda x: x['field'])",
                    "list(map(lambda x: expr, iterable))",
                    "list(filter(lambda x: condition, iterable))"
                ],
                "notes": "Lambda functions can only contain a single expression — no if/else blocks, no loops, no assignments. For anything complex, use def."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does list(filter(lambda x: x > 0, [-1, 2, -3, 4])) return?",
                    "options": ["A. [-1, -3]", "B. [2, 4]", "C. [1, 3]", "D. [-1, 2, -3, 4]"],
                    "answer": 1,
                    "explanation": "filter keeps items where the lambda returns True. x > 0 is True for 2 and 4, so the result is [2, 4]."
                },
                {
                    "type": "true_false",
                    "question": "A lambda function can contain multiple lines of code.",
                    "answer": False,
                    "explanation": "Lambda functions are limited to a single expression. For multi-line logic you must use a regular def function."
                },
                {
                    "type": "fill_blank",
                    "question": "Sort a list of dicts by the 'score' key using a lambda.",
                    "template": "sorted(data, ___ = lambda x: x['score'])",
                    "answer": "key",
                    "explanation": "The key parameter of sorted() accepts a callable that extracts the sort value from each element."
                }
            ],
            "challenge": {
                "instructions": "Given a list of sales records (dicts with 'rep', 'region', and 'amount'), use lambda with: (1) filter to keep only records above $10,000, (2) map to add a 'commission' field (7% of amount, rounded to 2 decimal places) to each kept record, (3) sorted to rank them by commission descending. Print each rep and their commission.",
                "starter_code": "sales = [\n    {\"rep\": \"Alice\", \"region\": \"North\", \"amount\": 15000},\n    {\"rep\": \"Bob\",   \"region\": \"South\", \"amount\": 8500},\n    {\"rep\": \"Carol\", \"region\": \"East\",  \"amount\": 22000},\n    {\"rep\": \"Dave\",  \"region\": \"West\",  \"amount\": 9800},\n    {\"rep\": \"Eve\",   \"region\": \"North\", \"amount\": 18500},\n]\n\n# 1. Filter: amount > 10000\n\n# 2. Map: add commission (7% of amount)\n\n# 3. Sort by commission descending\n\n# Print results\n",
                "tests": [
                    {"type": "code_contains", "value": "lambda"},
                    {"type": "output_contains", "value": "Carol"},
                    {"type": "runs_without_error"}
                ],
                "solution": """sales = [
    {"rep": "Alice", "region": "North", "amount": 15000},
    {"rep": "Bob",   "region": "South", "amount": 8500},
    {"rep": "Carol", "region": "East",  "amount": 22000},
    {"rep": "Dave",  "region": "West",  "amount": 9800},
    {"rep": "Eve",   "region": "North", "amount": 18500},
]

big_sales = list(filter(lambda s: s["amount"] > 10000, sales))

with_commission = list(map(
    lambda s: {**s, "commission": round(s["amount"] * 0.07, 2)},
    big_sales
))

ranked = sorted(with_commission, key=lambda s: s["commission"], reverse=True)

for s in ranked:
    print(f"{s['rep']:8} commission: ${s['commission']:,.2f}")
"""
            },
            "challenge_variations": [
                "Variation 1: Use sorted with a lambda to rank students by last name (split on space).",
                "Variation 2: Use map to convert a list of temperatures from Celsius to Fahrenheit.",
                "Variation 3: Use filter to keep only email addresses that contain '@company.com'.",
                "Variation 4: Sort a list of files by their extension using a lambda.",
                "Variation 5: Use map to apply a discount percentage to every price in a list.",
                "Variation 6: Chain filter and map to extract and transform data in one pipeline.",
                "Variation 7: Use a lambda as a default-value function in a dict.get() call.",
                "Variation 8: Sort a list of (date_string, amount) tuples by amount descending.",
                "Variation 9: Use filter to remove None values from a list with a lambda.",
                "Variation 10: Use map to capitalize only the first letter of each word in a list of tags."
            ]
        },
        {
            "id": "m1-l20",
            "title": "String Methods Deep Dive",
            "order": 20,
            "duration_min": 20,
            "real_world_context": "Data rarely arrives clean. Column headers have trailing spaces, categories are inconsistently capitalized, dates are in odd formats, and names have extra whitespace. String methods are your first line of defense in data cleaning.",
            "concept": """Python strings come with a rich set of built-in methods. You've seen a few — now let's go deep on the ones that matter most for data work.

**Splitting and joining:**
```python
# split() — break a string into a list
csv_row = "Alice,92,Business Analytics"
parts   = csv_row.split(",")
print(parts)    # ['Alice', '92', 'Business Analytics']

# split with maxsplit
text = "first last email extra"
first, rest = text.split(" ", 1)   # split at most once
print(first)  # first
print(rest)   # last email extra

# join() — the inverse of split()
words = ["Business", "Analytics", "and", "AI"]
print(" ".join(words))     # Business Analytics and AI
print("-".join(words))     # Business-Analytics-and-AI
```

**Cleaning whitespace:**
```python
raw = "   hello world   "
print(raw.strip())    # 'hello world'   (both ends)
print(raw.lstrip())   # 'hello world   ' (left only)
print(raw.rstrip())   # '   hello world' (right only)
```

**Finding and replacing:**
```python
text = "Data Science is great. Data Analytics is also great."
print(text.replace("great", "excellent"))
print(text.count("Data"))       # 2  — how many times it appears
print(text.find("Analytics"))   # 20 — index of first match (-1 if not found)
```

**Checking content:**
```python
email = "user@university.edu"
print(email.startswith("user"))          # True
print(email.endswith(".edu"))            # True
print("@" in email)                      # True  (fastest membership check)
print(email.isdigit())                   # False
print("  ".strip() == "")               # True  (check if blank after strip)

category = "  Business Analytics  "
print(category.strip().lower() == "business analytics")  # True
```

**String formatting review — all three ways:**
```python
name = "Alice"
score = 92.5

# %-style (old, avoid in new code)
print("Name: %s, Score: %.1f" % (name, score))

# .format() (still common)
print("Name: {}, Score: {:.1f}".format(name, score))

# f-strings (modern, preferred)
print(f"Name: {name}, Score: {score:.1f}")
```

**Real cleaning pattern:**
```python
def clean_header(raw):
    return raw.strip().lower().replace(" ", "_")

headers = ["  First Name ", "Last  Name", "GPA ", " Department"]
clean   = [clean_header(h) for h in headers]
print(clean)  # ['first_name', 'last__name', 'gpa', 'department']
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Parse and clean messy student data

raw_records = [
    "  alice chen  | 92 | business analytics ",
    "BOB SMITH|78|Finance",
    "  Carol  Jones|85 | Data Science  ",
]

students = []
for record in raw_records:
    parts = record.split("|")
    name  = parts[0].strip().title()   # normalize to Title Case
    score = int(parts[1].strip())
    major = parts[2].strip().title()
    students.append({"name": name, "score": score, "major": major})

for s in students:
    status = "Pass" if s["score"] >= 60 else "Fail"
    print(f"{s['name']:15} | {s['major']:20} | {s['score']} | {status}")
""",
                "explanation": ".split('|') breaks each record on the pipe character. .strip() removes surrounding whitespace. .title() converts to Title Case regardless of input casing. int() converts the score string to a number. This clean-parse-transform pattern is fundamental data preprocessing."
            },
            "difficulty": "intermediate",
            "reference": {
                "key_syntax": [
                    "s.split(sep)     # list of substrings",
                    "sep.join(list)   # join list into string",
                    "s.strip()        # remove whitespace",
                    "s.replace(a, b)  # substitute",
                    "s.startswith(x) / s.endswith(x)",
                    "s.find(x)        # index or -1",
                    "s.count(x)       # occurrences",
                    "x in s           # membership test",
                    "s.upper() / s.lower() / s.title()"
                ],
                "notes": "String methods never modify the original string — they return a new one. Chain them: s.strip().lower().replace(' ', '_')"
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does 'a,b,c'.split(',') return?",
                    "options": ["A. 'abc'", "B. ('a','b','c')", "C. ['a', 'b', 'c']", "D. {'a','b','c'}"],
                    "answer": 2,
                    "explanation": ".split() always returns a list. Splitting 'a,b,c' on ',' gives the list ['a', 'b', 'c']."
                },
                {
                    "type": "true_false",
                    "question": "'-'.join(['a', 'b', 'c']) returns 'a-b-c'.",
                    "answer": True,
                    "explanation": "join() inserts the separator between each element: 'a' + '-' + 'b' + '-' + 'c' = 'a-b-c'."
                },
                {
                    "type": "fill_blank",
                    "question": "Remove leading and trailing whitespace from a string called 'raw'.",
                    "template": "clean = raw._____()",
                    "answer": "strip",
                    "explanation": ".strip() removes all leading and trailing whitespace (spaces, tabs, newlines)."
                }
            ],
            "challenge": {
                "instructions": "You receive a list of messy product entries in the format 'ProductName | Price | Category'. Clean and parse each entry: strip whitespace, normalize the product name to Title Case, convert price to float, lowercase the category. Store results as a list of dicts. Then print only the products in the 'electronics' category with their price.",
                "starter_code": "raw_products = [\n    \"  laptop PRO  | 1299.99 | Electronics \",\n    \"wireless MOUSE | 49.99 |  Electronics\",\n    \"desk organizer |  24.99 | Office \",\n    \"USB HUB  | 35.00 | electronics\",\n    \"  Standing DESK | 450.00 | Office\",\n]\n\n# Parse and clean each entry\n\n# Print only electronics\n",
                "tests": [
                    {"type": "output_contains", "value": "Laptop Pro"},
                    {"type": "output_contains", "value": "1299.99"},
                    {"type": "runs_without_error"}
                ],
                "solution": """raw_products = [
    "  laptop PRO  | 1299.99 | Electronics ",
    "wireless MOUSE | 49.99 |  Electronics",
    "desk organizer |  24.99 | Office ",
    "USB HUB  | 35.00 | electronics",
    "  Standing DESK | 450.00 | Office",
]

products = []
for entry in raw_products:
    parts    = entry.split("|")
    name     = parts[0].strip().title()
    price    = float(parts[1].strip())
    category = parts[2].strip().lower()
    products.append({"name": name, "price": price, "category": category})

for p in products:
    if p["category"] == "electronics":
        print(f"{p['name']}: ${p['price']:.2f}")
"""
            },
            "challenge_variations": [
                "Variation 1: Parse a full name string 'Last, First' into separate first and last name variables.",
                "Variation 2: Count how many times the word 'error' appears in a multi-line log string.",
                "Variation 3: Clean a list of column headers by stripping whitespace, lowercasing, and replacing spaces with underscores.",
                "Variation 4: Check if a list of email addresses all end with the same domain.",
                "Variation 5: Extract the domain from a list of email addresses using split('@').",
                "Variation 6: Use join to convert a list of tags to a comma-separated string for a CSV.",
                "Variation 7: Validate that a product code starts with 'SKU-' and is exactly 10 characters long.",
                "Variation 8: Replace all occurrences of a placeholder like '{STUDENT}' in a template string.",
                "Variation 9: Parse a 'key=value' config file line into a key and value using split('=', 1).",
                "Variation 10: Find the longest word in a sentence using split and max with a lambda key."
            ]
        },
        {
            "id": "m1-l21",
            "title": "Working with Dates and Times",
            "order": 21,
            "duration_min": 22,
            "real_world_context": "Business analytics is full of time-based data: order dates, project deadlines, employee start dates, fiscal quarters. Being comfortable with Python's datetime module lets you calculate days until a deadline, compare timestamps, and format dates for reports.",
            "concept": """Python's `datetime` module handles dates and times. You'll use it constantly in data work.

**The key classes:**
- `date` — just a calendar date (year, month, day)
- `datetime` — a date AND a time
- `timedelta` — a duration (difference between two dates/times)

```python
from datetime import date, datetime, timedelta

# Today's date
today = date.today()
print(today)          # 2026-03-18
print(today.year)     # 2026
print(today.month)    # 3
print(today.day)      # 18

# A specific date
start_date = date(2026, 6, 1)   # June 1, 2026
print(start_date)     # 2026-06-01
```

**Date arithmetic with timedelta:**
```python
today      = date.today()
deadline   = date(2026, 4, 30)
days_left  = (deadline - today).days
print(f"Days until deadline: {days_left}")

one_week_later = today + timedelta(weeks=1)
print(one_week_later)

# timedelta supports: days, seconds, weeks
two_weeks = timedelta(weeks=2)
ninety_days = timedelta(days=90)
```

**Formatting dates — strftime (date → string):**
```python
today = date.today()
print(today.strftime("%Y-%m-%d"))    # 2026-03-18
print(today.strftime("%B %d, %Y"))  # March 18, 2026
print(today.strftime("%m/%d/%y"))   # 03/18/26
```

Common format codes: `%Y` = 4-digit year, `%m` = month number, `%d` = day, `%B` = full month name, `%A` = full weekday name.

**Parsing strings — strptime (string → date):**
```python
raw = "2026-06-15"
parsed = datetime.strptime(raw, "%Y-%m-%d").date()
print(parsed)           # 2026-06-15
print(type(parsed))     # <class 'datetime.date'>

# Parse a messy format
messy = "June 15, 2026"
clean = datetime.strptime(messy, "%B %d, %Y").date()
```

**Real business use case:**
```python
projects = [
    {"name": "Q2 Report",    "deadline": date(2026, 6, 30)},
    {"name": "Model Review", "deadline": date(2026, 4, 15)},
    {"name": "Presentation", "deadline": date(2026, 5, 1)},
]

today = date.today()
for p in sorted(projects, key=lambda x: x["deadline"]):
    days = (p["deadline"] - today).days
    status = "OVERDUE" if days < 0 else f"due in {days} days"
    print(f"{p['name']:15} — {p['deadline']} ({status})")
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """from datetime import date, timedelta

# Worked example: Employee anniversary tracker

employees = [
    {"name": "Alice",  "start_date": date(2021, 3, 10)},
    {"name": "Bob",    "start_date": date(2019, 8, 22)},
    {"name": "Carol",  "start_date": date(2023, 11, 5)},
    {"name": "David",  "start_date": date(2020, 6, 1)},
]

today = date.today()

print("Employee Tenure Report")
print("-" * 40)
for e in employees:
    tenure_days  = (today - e["start_date"]).days
    tenure_years = tenure_days // 365
    tenure_months = (tenure_days % 365) // 30
    print(f"{e['name']:8} started {e['start_date'].strftime('%B %d, %Y')} "
          f"— {tenure_years}y {tenure_months}m")
""",
                "explanation": "We subtract dates to get a timedelta; .days gives the integer number of days. Integer division by 365 gives years, and the remainder divided by 30 approximates months. strftime formats the date for the report."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "from datetime import date, datetime, timedelta",
                    "date.today()  /  date(y, m, d)",
                    "(date2 - date1).days",
                    "date + timedelta(days=n)",
                    "date.strftime('%Y-%m-%d')  # date → string",
                    "datetime.strptime(s, fmt).date()  # string → date",
                    "%Y %m %d %B %A  # format codes"
                ],
                "notes": "strftime = 'format' (date to string). strptime = 'parse' (string to date). The 'p' in strptime stands for parse."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "How do you find the number of days between two date objects d1 and d2?",
                    "options": [
                        "A. d2 - d1",
                        "B. (d2 - d1).days",
                        "C. timedelta(d2, d1)",
                        "D. date.diff(d1, d2)"
                    ],
                    "answer": 1,
                    "explanation": "Subtracting two date objects returns a timedelta object. You then access the .days attribute to get the integer number of days."
                },
                {
                    "type": "true_false",
                    "question": "strftime converts a date object to a formatted string.",
                    "answer": True,
                    "explanation": "strftime (string format time) takes a format string and returns the date as a formatted string. strptime does the reverse — parses a string into a date."
                },
                {
                    "type": "fill_blank",
                    "question": "Format today's date as 'March 18, 2026' style.",
                    "template": "today.strftime('___ %d, %Y')",
                    "answer": "%B",
                    "explanation": "%B is the full month name (January, February, ...). %m would give the number (01, 02, ...)."
                }
            ],
            "challenge": {
                "instructions": "You have a list of project dicts with 'name', 'start_date' (a string in 'YYYY-MM-DD' format), and 'deadline' (also a string). Parse both strings into date objects, compute: (1) project duration in days, (2) days remaining from today until the deadline (negative if overdue). Print a formatted table sorted by deadline. Mark any project as 'OVERDUE' if the deadline has passed.",
                "starter_code": "from datetime import date, datetime\n\nprojects = [\n    {\"name\": \"Market Analysis\",  \"start_date\": \"2026-01-15\", \"deadline\": \"2026-04-01\"},\n    {\"name\": \"Revenue Forecast\", \"start_date\": \"2026-02-01\", \"deadline\": \"2026-03-15\"},\n    {\"name\": \"Customer Survey\",  \"start_date\": \"2026-03-01\", \"deadline\": \"2026-05-30\"},\n]\n\ntoday = date.today()\n\n# Parse dates, compute stats, print table\n",
                "tests": [
                    {"type": "code_contains", "value": "strptime"},
                    {"type": "code_contains", "value": "timedelta"},
                    {"type": "runs_without_error"}
                ],
                "solution": """from datetime import date, datetime, timedelta

projects = [
    {"name": "Market Analysis",  "start_date": "2026-01-15", "deadline": "2026-04-01"},
    {"name": "Revenue Forecast", "start_date": "2026-02-01", "deadline": "2026-03-15"},
    {"name": "Customer Survey",  "start_date": "2026-03-01", "deadline": "2026-05-30"},
]

today = date.today()

parsed = []
for p in projects:
    start    = datetime.strptime(p["start_date"], "%Y-%m-%d").date()
    deadline = datetime.strptime(p["deadline"],   "%Y-%m-%d").date()
    duration = (deadline - start).days
    remaining = (deadline - today).days
    parsed.append({**p, "start": start, "deadline_date": deadline,
                   "duration": duration, "remaining": remaining})

for p in sorted(parsed, key=lambda x: x["deadline_date"]):
    status = "OVERDUE" if p["remaining"] < 0 else f"{p['remaining']} days left"
    print(f"{p['name']:20} | {p['duration']} day project | {status}")
"""
            },
            "challenge_variations": [
                "Variation 1: Calculate how many days remain until a student's program start date.",
                "Variation 2: Given a list of invoice dates as strings, find the oldest and newest invoice.",
                "Variation 3: Generate a list of the next 5 Mondays from today using timedelta.",
                "Variation 4: Parse a log file's timestamp strings and find the total duration of a process.",
                "Variation 5: Calculate each employee's age from their date of birth.",
                "Variation 6: Find all projects that are due within the next 30 days.",
                "Variation 7: Group a list of sales dates by month and count sales per month.",
                "Variation 8: Convert a list of dates from 'MM/DD/YYYY' format to 'YYYY-MM-DD'.",
                "Variation 9: Determine which quarter (Q1-Q4) each date falls in.",
                "Variation 10: Calculate the average number of days between consecutive events in a sorted date list."
            ]
        },
        {
            "id": "m1-l22",
            "title": "Type Hints and Clean Code",
            "order": 22,
            "duration_min": 20,
            "real_world_context": "In your MS program and on any professional data team, you'll read and write code collaboratively. Clean code — with type hints and docstrings — is not just good style; it's a professional expectation and makes debugging ten times faster.",
            "concept": """**Type hints** tell Python (and your team) what data types a function expects and returns. Python doesn't enforce them at runtime, but tools and IDEs use them to catch bugs before you run your code.

```python
# Without type hints — what does this function expect?
def calculate_grade(score, total):
    return (score / total) * 100

# With type hints — crystal clear
def calculate_grade(score: float, total: float) -> float:
    return (score / total) * 100
```

**Syntax:** `param: type` for parameters, `-> type` after the closing parenthesis for the return type.

**Common types to annotate:**
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def count_passing(scores: list, threshold: int = 60) -> int:
    return sum(1 for s in scores if s >= threshold)

def get_student(students: dict, student_id: int) -> dict | None:
    return students.get(student_id)  # might return None
```

**Docstrings — document what your function does:**
```python
def calculate_average(grades: list[float]) -> float:
    \"\"\"
    Calculate the arithmetic mean of a list of grades.

    Args:
        grades: A list of numeric grade values (0-100).

    Returns:
        The arithmetic mean as a float.

    Raises:
        ValueError: If the grades list is empty.
    \"\"\"
    if not grades:
        raise ValueError("Cannot average an empty list.")
    return sum(grades) / len(grades)
```

**Meaningful names — the most impactful clean-code habit:**
```python
# BAD — what does x, y, z mean?
def f(x, y, z):
    return (x / y) * z

# GOOD — self-documenting
def calculate_weighted_score(raw_score: float, max_score: float, weight: float) -> float:
    return (raw_score / max_score) * weight
```

**Constants — use uppercase names for fixed values:**
```python
MAX_GRADE     = 100
PASSING_SCORE = 60
TAX_RATE      = 0.08
```

Clean code is not about aesthetics — it's about reducing the mental effort required to understand, debug, and extend your work. A function with a good name and docstring is self-explanatory in a code review.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Refactor messy code into clean, documented functions

# BEFORE: hard to understand
def proc(d, t=0.6):
    r = []
    for x in d:
        if x["s"] >= t * 100:
            r.append(x)
    return r

# AFTER: clean, typed, documented
PASSING_THRESHOLD = 0.60  # 60%

def filter_passing_students(
    student_records: list[dict],
    passing_threshold: float = PASSING_THRESHOLD
) -> list[dict]:
    \"\"\"
    Return only students who met the passing threshold.

    Args:
        student_records: List of dicts with at least a 'score' key (0-100).
        passing_threshold: Minimum fraction to pass (default 0.60 = 60%).

    Returns:
        Filtered list of student dicts.
    \"\"\"
    min_score = passing_threshold * 100
    return [s for s in student_records if s["score"] >= min_score]


students = [
    {"name": "Alice", "score": 88},
    {"name": "Bob",   "score": 55},
    {"name": "Carol", "score": 72},
    {"name": "Dave",  "score": 45},
]

passing = filter_passing_students(students)
print(f"Passing students: {[s['name'] for s in passing]}")
""",
                "explanation": "The refactored version uses a constant for the threshold, type hints to document expected types, a docstring that explains args and return value, and a meaningful function name. The logic is identical to the original but anyone reading it immediately understands the intent."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "def func(param: type) -> return_type:",
                    "param: list[str]  # list of strings",
                    "param: dict[str, int]  # dict with str keys and int values",
                    "param: type | None  # optional (may be None)",
                    '\"\"\"Docstring here.\"\"\"',
                    "CONSTANT_NAME = value  # uppercase for constants"
                ],
                "notes": "Type hints are not enforced at runtime — Python won't crash if you pass the wrong type. Use tools like mypy or your IDE's type checker to catch errors statically."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does the -> in 'def func(x: int) -> str:' mean?",
                    "options": [
                        "A. The function takes a string and returns an int",
                        "B. The function returns a string",
                        "C. The function is asynchronous",
                        "D. The function can only be called once"
                    ],
                    "answer": 1,
                    "explanation": "-> str after the closing parenthesis is the return type hint — it tells you (and your IDE) that this function returns a string."
                },
                {
                    "type": "true_false",
                    "question": "Python will raise a TypeError at runtime if you pass the wrong type to a type-hinted function.",
                    "answer": False,
                    "explanation": "Type hints are for documentation and static analysis tools only — Python itself does NOT enforce them at runtime. The function will run regardless."
                },
                {
                    "type": "fill_blank",
                    "question": "Complete the docstring opening for a function.",
                    "template": "def my_func():\n    ___\n    This function does something.\n    ___",
                    "answer": '\"\"\"',
                    "explanation": 'Docstrings use triple quotes (\"\"\"). They appear immediately after the def line and are accessible via help(my_func).'
                }
            ],
            "challenge": {
                "instructions": "Take the following messy function and rewrite it cleanly: it should have (1) a descriptive name, (2) type hints on all parameters and return value, (3) a proper docstring with Args and Returns sections, (4) a named constant instead of a magic number, and (5) a meaningful variable name inside the function.\n\nOriginal: def calc(d, r=0.07): return d + d * r",
                "starter_code": "# Original messy function:\n# def calc(d, r=0.07): return d + d * r\n\n# Rewrite it below with: good name, type hints, docstring, constant\n\n# Test your function\nprint(calc(1000))      # should print 1070.0\nprint(calc(1000, 0.05))  # should print 1050.0\n",
                "tests": [
                    {"type": "code_contains", "value": '\"\"\"'},
                    {"type": "code_contains", "value": "->"},
                    {"type": "output_contains", "value": "1070"},
                    {"type": "runs_without_error"}
                ],
                "solution": '''DEFAULT_INTEREST_RATE = 0.07  # 7% annual rate

def calculate_total_with_interest(
    principal: float,
    interest_rate: float = DEFAULT_INTEREST_RATE
) -> float:
    """
    Calculate total amount after applying an interest rate.

    Args:
        principal: The original amount before interest.
        interest_rate: The decimal interest rate (default 0.07 = 7%).

    Returns:
        The total amount including interest.
    """
    return principal + principal * interest_rate

print(calculate_total_with_interest(1000))
print(calculate_total_with_interest(1000, 0.05))
'''
            },
            "challenge_variations": [
                "Variation 1: Add type hints and a docstring to your Student class from Lesson 15.",
                "Variation 2: Refactor a function with single-letter variable names to use descriptive names.",
                "Variation 3: Write a fully documented function that validates an email address.",
                "Variation 4: Replace all magic numbers in a tax-calculation script with named constants.",
                "Variation 5: Add type hints to a function that returns a list of dicts.",
                "Variation 6: Write a docstring for a complex function using Google or NumPy docstring style.",
                "Variation 7: Annotate a function that accepts an optional parameter (str | None).",
                "Variation 8: Refactor a 50-line procedural script into three well-named functions.",
                "Variation 9: Add type hints to a function that uses *args and **kwargs.",
                "Variation 10: Create a clean, documented module with three utility functions for data cleaning."
            ]
        },
        {
            "id": "m1-l23",
            "title": "Debugging Python Code",
            "order": 23,
            "duration_min": 20,
            "real_world_context": "Every programmer spends a significant portion of their time debugging. Learning to read tracebacks, understand common errors, and debug systematically is what separates someone who gives up after the first error from someone who solves problems efficiently.",
            "concept": """When Python hits an error, it prints a **traceback** — a detailed message showing exactly where and why things went wrong. Learning to read it is your most important debugging skill.

**Anatomy of a traceback:**
```
Traceback (most recent call last):
  File "script.py", line 12, in <module>
    result = calculate_avg(scores)
  File "script.py", line 5, in calculate_avg
    return sum(grades) / len(grades)
ZeroDivisionError: division by zero
```

Read it **bottom-up**: the last line is the error type and message. Work your way up through the call stack to find where YOUR code triggered it.

**The most common errors and how to fix them:**

```python
# NameError — variable doesn't exist (typo or not defined yet)
print(scroe)   # NameError: name 'scroe' is not defined
# Fix: check spelling, make sure variable is defined before use

# TypeError — wrong type
"5" + 5        # TypeError: can only concatenate str (not "int") to str
# Fix: int("5") + 5  or  "5" + str(5)

# IndexError — list index out of range
lst = [1, 2, 3]
print(lst[5])  # IndexError: list index out of range
# Fix: check len(lst) before accessing

# KeyError — dict key missing
d = {"a": 1}
print(d["b"])  # KeyError: 'b'
# Fix: use d.get("b") or check "b" in d first

# ValueError — right type, wrong value
int("hello")   # ValueError: invalid literal for int() with base 10: 'hello'
# Fix: use try/except or validate input first

# IndentationError — wrong indentation
def func():
print("hi")  # IndentationError: expected an indented block
# Fix: indent the body
```

**Print-debugging strategy — the simplest and most effective tool:**
```python
def process_data(records):
    print(f"DEBUG: received {len(records)} records")   # add debug prints
    total = 0
    for i, record in enumerate(records):
        print(f"DEBUG: record[{i}] = {record}")        # see each record
        total += record["value"]
    print(f"DEBUG: total = {total}")                    # check accumulation
    return total / len(records)
```

Remove or comment out debug prints once you've fixed the issue.

**Systematic debugging checklist:**
1. Read the traceback bottom-up — what is the error type?
2. Go to the line number mentioned — what does that line do?
3. Print the variables involved right before the error
4. Check types: `print(type(variable))`
5. Simplify — comment out code until the error disappears, then add back""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Find and fix 4 bugs in this grade calculator

# BUGGY VERSION (do not run as-is)
# def compute_report(studens):
#     results = []
#     for student in students:
#         avg = sum(student["grade"]) / len(student["grade"])
#         results.append({
#             "name": student["name"],
#             "average": avg,
#             "passed": avg > 60
#         })
#     return result

# BUG ANALYSIS:
# 1. Line 1: parameter name 'studens' (typo) but loop uses 'students' -> NameError
# 2. Line 4: key "grade" should be "grades" (based on data structure) -> KeyError
# 3. Line 10: returns 'result' instead of 'results' -> NameError
# (The logic avg > 60 should be >= 60 -- a logic bug, not a syntax error)

# FIXED VERSION:
def compute_report(students):
    results = []
    for student in students:
        avg = sum(student["grades"]) / len(student["grades"])
        results.append({
            "name": student["name"],
            "average": round(avg, 1),
            "passed": avg >= 60
        })
    return results

data = [
    {"name": "Alice", "grades": [88, 92, 85]},
    {"name": "Bob",   "grades": [55, 60, 58]},
]
for r in compute_report(data):
    print(r)
""",
                "explanation": "Bug 1 was a NameError from a typo in the parameter name. Bug 2 was a KeyError from a wrong dictionary key. Bug 3 was a NameError from a typo in the return variable name. The pattern: read the error type, go to the line, check names and keys carefully."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "Read traceback bottom-up: error type + line number",
                    "print(type(var))  # check data type",
                    "print(len(var))   # check size",
                    "print(var)        # inspect value",
                    "Common: NameError, TypeError, IndexError, KeyError, ValueError, IndentationError",
                    "try/except to handle expected errors"
                ],
                "notes": "The line number in a traceback is where Python detected the problem, not always where you wrote the bug. Look one or two steps up the call stack too."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "You see 'KeyError: \"score\"' — what most likely caused it?",
                    "options": [
                        "A. A list index out of range",
                        "B. You tried to access d['score'] but the dict doesn't have that key",
                        "C. The variable 'score' was not defined",
                        "D. You divided by zero"
                    ],
                    "answer": 1,
                    "explanation": "KeyError occurs when you access a dictionary key that doesn't exist. Check that the key name is spelled correctly and that the data actually has that key."
                },
                {
                    "type": "true_false",
                    "question": "In a Python traceback, you should read from the bottom up to understand the error.",
                    "answer": True,
                    "explanation": "The most specific error information is at the bottom — the exception type and message. The lines above show the call stack leading to the error. Start at the bottom."
                },
                {
                    "type": "fill_blank",
                    "question": "What is the quickest way to inspect the type of a variable x while debugging?",
                    "template": "print(___(x))",
                    "answer": "type",
                    "explanation": "type(x) returns the type of any variable — print(type(x)) is the fastest way to confirm whether x is a str, int, list, dict, etc."
                }
            ],
            "challenge": {
                "instructions": "The code below has 4 bugs. Your task: (1) identify each bug and what type of error it causes, (2) fix all 4 bugs so the code runs correctly and prints each student's name and average score. Write a comment above each fix explaining what was wrong.",
                "starter_code": "students = [\n    {\"name\": \"Alice\", \"scores\": [88, 92, 79]},\n    {\"name\": \"Bob\",   \"scores\": [72, 68, 75]},\n]\n\ndef compute_averages(student_list):\n    averages = {}\n    for student in student_list:\n        name = student[\"names\"]            # Bug 1\n        total = sum(student[\"scores\"])\n        avg = total / len(student[scores]) # Bug 2\n        averages[name] = avg\n    return averagess                       # Bug 3\n\nresults = compute_averages(students)\nfor name, avg in result.items():          # Bug 4\n    print(f\"{name}: {avg:.1f}\")\n",
                "tests": [
                    {"type": "output_contains", "value": "Alice"},
                    {"type": "output_contains", "value": "86."},
                    {"type": "runs_without_error"}
                ],
                "solution": '''students = [
    {"name": "Alice", "scores": [88, 92, 79]},
    {"name": "Bob",   "scores": [72, 68, 75]},
]

def compute_averages(student_list):
    averages = {}
    for student in student_list:
        # Fix 1: "names" -> "name" (KeyError: wrong key name)
        name = student["name"]
        total = sum(student["scores"])
        # Fix 2: scores -> "scores" (NameError: missing quotes around dict key)
        avg = total / len(student["scores"])
        averages[name] = avg
    # Fix 3: averagess -> averages (NameError: typo in variable name)
    return averages

results = compute_averages(students)
# Fix 4: result -> results (NameError: typo in variable name)
for name, avg in results.items():
    print(f"{name}: {avg:.1f}")
'''
            },
            "challenge_variations": [
                "Variation 1: Find and fix an off-by-one IndexError in a loop that processes a list.",
                "Variation 2: Debug a function that returns None instead of a value (missing return statement).",
                "Variation 3: Fix a TypeError caused by trying to add a string and an integer.",
                "Variation 4: Identify why a while loop runs forever and add the correct stopping condition.",
                "Variation 5: Debug a function that gives wrong results due to a logic error (wrong operator).",
                "Variation 6: Fix an IndentationError in a class definition.",
                "Variation 7: A CSV parser crashes on one row — add error handling to skip bad rows and log them.",
                "Variation 8: A dict lookup crashes — rewrite using .get() with a default value.",
                "Variation 9: Debug a function where the variable is updated in the wrong scope.",
                "Variation 10: Use print-debugging to find which iteration of a loop produces an incorrect result."
            ]
        },
        {
            "id": "m1-l24",
            "title": "Nested Data Structures",
            "order": 24,
            "duration_min": 25,
            "real_world_context": "JSON data from APIs, database query results, and configuration files are almost always nested — lists of dicts, dicts of lists, and multiple levels deep. This is the exact data shape you'll manipulate in every data analytics project.",
            "concept": """Real-world data is rarely flat. You'll constantly work with structures like: a list of student records (each a dict), a dict of department data (each value a list), or deeply nested JSON from an API.

**Lists of dicts — the most common data shape:**
```python
students = [
    {"name": "Alice", "gpa": 3.8, "courses": ["Python", "Stats"]},
    {"name": "Bob",   "gpa": 3.2, "courses": ["SQL", "Excel"]},
    {"name": "Carol", "gpa": 3.9, "courses": ["Python", "ML", "Stats"]},
]

# Access a specific student's name
print(students[0]["name"])          # Alice

# Access a course inside a nested list
print(students[0]["courses"][1])    # Stats

# Loop through all students
for s in students:
    print(s["name"], "—", ", ".join(s["courses"]))
```

**Dicts of lists:**
```python
department_sales = {
    "North": [15000, 18000, 12000],
    "South": [22000, 19000, 25000],
    "East":  [9000,  11000, 14000],
}

for region, sales in department_sales.items():
    avg = sum(sales) / len(sales)
    print(f"{region}: avg ${avg:,.0f}")
```

**Deeply nested JSON-like structures:**
```python
company = {
    "name": "Orion Corp",
    "departments": {
        "engineering": {
            "head": "Alice",
            "employees": ["Bob", "Carol", "Dave"],
            "budget": 500000
        },
        "marketing": {
            "head": "Eve",
            "employees": ["Frank", "Grace"],
            "budget": 200000
        }
    }
}

# Access nested values
eng_head   = company["departments"]["engineering"]["head"]
mkt_team   = company["departments"]["marketing"]["employees"]
print(eng_head)      # Alice
print(mkt_team[0])   # Frank

# Safe nested access with .get()
budget = company.get("departments", {}).get("finance", {}).get("budget", 0)
print(budget)   # 0 (finance dept doesn't exist)
```

**Building nested structures programmatically:**
```python
# Group students by grade
students = [
    {"name": "Alice", "grade": "A"},
    {"name": "Bob",   "grade": "B"},
    {"name": "Carol", "grade": "A"},
    {"name": "Dave",  "grade": "C"},
]

by_grade = {}
for s in students:
    grade = s["grade"]
    if grade not in by_grade:
        by_grade[grade] = []        # initialize list
    by_grade[grade].append(s["name"])

print(by_grade)
# {'A': ['Alice', 'Carol'], 'B': ['Bob'], 'C': ['Dave']}
```""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Analyze a nested course enrollment dataset

enrollments = {
    "Python Foundations": {
        "instructor": "Dr. Smith",
        "students": [
            {"name": "Alice",  "score": 92},
            {"name": "Bob",    "score": 78},
            {"name": "Carol",  "score": 85},
        ]
    },
    "Applied Statistics": {
        "instructor": "Dr. Jones",
        "students": [
            {"name": "Dave",   "score": 88},
            {"name": "Alice",  "score": 95},
            {"name": "Eve",    "score": 71},
        ]
    }
}

print("Course Summary Report")
print("=" * 45)
for course_name, data in enrollments.items():
    scores = [s["score"] for s in data["students"]]
    avg    = sum(scores) / len(scores)
    top    = max(data["students"], key=lambda s: s["score"])
    print(f"{course_name}")
    print(f"  Instructor: {data['instructor']}")
    print(f"  Students:   {len(scores)}")
    print(f"  Avg Score:  {avg:.1f}")
    print(f"  Top Scorer: {top['name']} ({top['score']})")
""",
                "explanation": "We navigate two levels deep: enrollments[course_name] gets the course dict, then ['students'] gets the list, then a comprehension extracts the scores. max() with a lambda key finds the highest-scoring student. This pattern — traverse, extract, aggregate — is how you'll process almost all analytics data."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "data[0]['key']           # list of dicts",
                    "data['key'][0]           # dict of lists",
                    "data['a']['b']['c']      # deep nesting",
                    "d.get('k', {}).get('k2') # safe nested access",
                    "[item['field'] for item in list]  # extract a column",
                    "max(list, key=lambda x: x['field'])"
                ],
                "notes": "When accessing deeply nested keys you're not sure exist, chain .get() calls with empty dict defaults. Accessing a missing key with [] raises KeyError; .get() returns None or your default."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "Given data = [{'x': 1}, {'x': 2}], how do you access the x value of the second dict?",
                    "options": ["A. data['x'][1]", "B. data[1]['x']", "C. data[1, 'x']", "D. data.x[1]"],
                    "answer": 1,
                    "explanation": "data[1] gets the second dict (index 1), then ['x'] gets the value of key 'x'. You chain index then key access."
                },
                {
                    "type": "true_false",
                    "question": "A Python dict can contain a list as a value, and that list can contain dicts.",
                    "answer": True,
                    "explanation": "Python data structures can be nested arbitrarily. A dict's values can be any type — including lists, which can contain other dicts. This is how JSON data is represented in Python."
                },
                {
                    "type": "fill_blank",
                    "question": "Extract all 'name' values from a list of dicts called 'records' into a new list.",
                    "template": "names = [r[___] for r in records]",
                    "answer": "'name'",
                    "explanation": "r['name'] accesses the 'name' key from each dict r in the list. The comprehension collects all of them into a new list."
                }
            ],
            "challenge": {
                "instructions": "You have a nested dataset of regional sales records. Each region has a list of monthly sales dicts with 'month' and 'revenue' keys. Write code that: (1) computes total and average revenue for each region, (2) finds the best month (highest revenue) across ALL regions, (3) prints a formatted summary table sorted by total revenue descending.",
                "starter_code": "sales_data = {\n    \"North\": [\n        {\"month\": \"Jan\", \"revenue\": 42000},\n        {\"month\": \"Feb\", \"revenue\": 38000},\n        {\"month\": \"Mar\", \"revenue\": 51000},\n    ],\n    \"South\": [\n        {\"month\": \"Jan\", \"revenue\": 65000},\n        {\"month\": \"Feb\", \"revenue\": 71000},\n        {\"month\": \"Mar\", \"revenue\": 59000},\n    ],\n    \"East\": [\n        {\"month\": \"Jan\", \"revenue\": 28000},\n        {\"month\": \"Feb\", \"revenue\": 33000},\n        {\"month\": \"Mar\", \"revenue\": 30000},\n    ],\n}\n\n# Compute stats and print summary\n",
                "tests": [
                    {"type": "output_contains", "value": "South"},
                    {"type": "output_contains", "value": "195000"},
                    {"type": "runs_without_error"}
                ],
                "solution": """sales_data = {
    "North": [
        {"month": "Jan", "revenue": 42000},
        {"month": "Feb", "revenue": 38000},
        {"month": "Mar", "revenue": 51000},
    ],
    "South": [
        {"month": "Jan", "revenue": 65000},
        {"month": "Feb", "revenue": 71000},
        {"month": "Mar", "revenue": 59000},
    ],
    "East": [
        {"month": "Jan", "revenue": 28000},
        {"month": "Feb", "revenue": 33000},
        {"month": "Mar", "revenue": 30000},
    ],
}

summaries = []
all_months = []

for region, months in sales_data.items():
    revenues = [m["revenue"] for m in months]
    total    = sum(revenues)
    avg      = total / len(revenues)
    summaries.append({"region": region, "total": total, "avg": avg})
    all_months.extend([(region, m["month"], m["revenue"]) for m in months])

summaries.sort(key=lambda x: x["total"], reverse=True)
best = max(all_months, key=lambda x: x[2])

print(f"{'Region':10} {'Total':>12} {'Monthly Avg':>14}")
print("-" * 38)
for s in summaries:
    print(f"{s['region']:10} ${s['total']:>11,} ${s['avg']:>13,.0f}")

print(f"\\nBest month overall: {best[0]} {best[1]} (${best[2]:,})")
"""
            },
            "challenge_variations": [
                "Variation 1: Flatten a list of lists of product names into one deduplicated sorted list.",
                "Variation 2: Given a list of order dicts each containing a 'items' list, count total items across all orders.",
                "Variation 3: Group a flat list of transactions into a dict keyed by customer ID.",
                "Variation 4: Navigate three levels of nesting to extract all employee names from a company org-chart dict.",
                "Variation 5: Find the student with the highest score across all courses in a course-enrollment dataset.",
                "Variation 6: Convert a list of dicts into a dict-of-lists (pivot the structure).",
                "Variation 7: Given a JSON-like API response, extract all values for a specific key at any nesting level.",
                "Variation 8: Build a nested dict from a flat CSV-like list of (department, team, employee) tuples.",
                "Variation 9: Compute the total budget from a multi-level department hierarchy dict.",
                "Variation 10: Merge two lists of dicts on a shared key (like a simple JOIN operation)."
            ]
        },
        {
            "id": "m1-l25",
            "title": "Virtual Environments and Packages",
            "order": 25,
            "duration_min": 20,
            "real_world_context": "Every professional Python project uses a virtual environment. It's how you avoid the 'it works on my machine' problem, share your project with teammates, and install packages like numpy and pandas without them conflicting across projects.",
            "concept": """**The problem virtual environments solve:** Imagine Project A needs pandas version 1.3 and Project B needs pandas version 2.0. If you install both globally, they conflict. A virtual environment is an isolated Python installation per project — each project gets its own packages, its own versions, no conflicts.

**Creating and activating a virtual environment:**
```bash
# Create a virtual environment named 'venv' in your project folder
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\\Scripts\\activate

# Your terminal prompt changes: (venv) $
# Now any pip install goes into THIS project only

# Deactivate when done
deactivate
```

**Installing packages with pip:**
```bash
# Install a single package
pip install numpy

# Install a specific version
pip install pandas==2.1.0

# Install multiple packages
pip install numpy pandas matplotlib scikit-learn

# See what's installed
pip list

# Uninstall
pip uninstall numpy
```

**requirements.txt — sharing your environment:**
```bash
# Save all your project's dependencies to a file
pip freeze > requirements.txt

# Someone else (or you on a new machine) can recreate the environment:
pip install -r requirements.txt
```

A typical `requirements.txt` looks like:
```
numpy==1.26.0
pandas==2.1.4
scikit-learn==1.3.2
matplotlib==3.8.0
```

**Using installed packages in Python:**
```python
import numpy as np
import pandas as pd

# numpy: fast math on arrays
arr = np.array([1, 2, 3, 4, 5])
print(np.mean(arr))    # 3.0
print(np.std(arr))     # 1.4142...

# pandas: DataFrames — like Excel tables in Python
data = {"name": ["Alice", "Bob"], "score": [92, 78]}
df = pd.DataFrame(data)
print(df)
#     name  score
# 0  Alice     92
# 1    Bob     78
print(df["score"].mean())  # 85.0
```

You'll use numpy and pandas in virtually every analytics project. The standard workflow: create venv → pip install → import → build.""",
            "worked_example": {
                "description": "Let's solve a similar problem together before you try yours.",
                "code": """# Worked example: Use numpy for grade statistics (run after: pip install numpy)

import numpy as np

grades = [88, 72, 95, 61, 90, 55, 83, 77, 91, 68]

grades_array = np.array(grades)

print("Grade Statistics (numpy)")
print(f"Mean:       {np.mean(grades_array):.2f}")
print(f"Median:     {np.median(grades_array):.2f}")
print(f"Std Dev:    {np.std(grades_array):.2f}")
print(f"Min / Max:  {np.min(grades_array)} / {np.max(grades_array)}")
print(f"25th pct:   {np.percentile(grades_array, 25):.1f}")
print(f"75th pct:   {np.percentile(grades_array, 75):.1f}")

# Boolean indexing — a numpy superpower
passing = grades_array[grades_array >= 60]
print(f"\\nPassing grades: {passing}")
print(f"Pass rate: {len(passing)/len(grades_array)*100:.0f}%")
""",
                "explanation": "numpy arrays support mathematical operations on the whole array at once — no loops needed. np.mean(), np.std(), np.percentile() give you statistics in one line. Boolean indexing (grades_array >= 60) creates a mask and filters the array. This is the foundation of all numerical computing in Python."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "python -m venv venv          # create",
                    "source venv/bin/activate      # activate (Mac/Linux)",
                    "venv\\\\Scripts\\\\activate       # activate (Windows)",
                    "pip install package_name",
                    "pip freeze > requirements.txt",
                    "pip install -r requirements.txt",
                    "import numpy as np",
                    "import pandas as pd"
                ],
                "notes": "Always create a venv before starting a new project. Never install packages globally for project work. Add 'venv/' to your .gitignore — never commit the venv folder itself, only requirements.txt."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does 'pip freeze > requirements.txt' do?",
                    "options": [
                        "A. Uninstalls all packages",
                        "B. Saves a list of all installed packages and their versions to requirements.txt",
                        "C. Installs packages from a file",
                        "D. Activates the virtual environment"
                    ],
                    "answer": 1,
                    "explanation": "pip freeze lists all installed packages with versions. > redirects that output to a file. The result is requirements.txt — a snapshot of your environment that others can replicate."
                },
                {
                    "type": "true_false",
                    "question": "You should commit your entire venv/ folder to Git so teammates can use the same environment.",
                    "answer": False,
                    "explanation": "Never commit the venv folder — it's large, platform-specific, and unnecessary. Instead commit requirements.txt, which teammates use to recreate their own venv with pip install -r requirements.txt."
                },
                {
                    "type": "fill_blank",
                    "question": "Install the pandas library using pip.",
                    "template": "___ install pandas",
                    "answer": "pip",
                    "explanation": "pip is Python's package installer. 'pip install pandas' downloads pandas and all its dependencies into your current (virtual) environment."
                }
            ],
            "challenge": {
                "instructions": "Write a Python script that demonstrates your understanding of numpy (or simulates it using only the standard library if numpy is not installed). Create a list of 10 numeric scores, compute the mean, median (sort and pick middle), standard deviation, and the percentage of scores above the mean. Print all results with clear labels. Bonus: if numpy is available, use np.array() and numpy functions instead.",
                "starter_code": "import math\n\n# Try to import numpy; fall back to manual calculation if not available\ntry:\n    import numpy as np\n    HAS_NUMPY = True\nexcept ImportError:\n    HAS_NUMPY = False\n\nscores = [88, 72, 95, 61, 90, 55, 83, 77, 91, 68]\n\n# Compute and print: mean, median, std dev, % above mean\n",
                "tests": [
                    {"type": "output_contains", "value": "mean"},
                    {"type": "output_contains", "value": "78"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import math

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

scores = [88, 72, 95, 61, 90, 55, 83, 77, 91, 68]

if HAS_NUMPY:
    arr    = np.array(scores)
    mean   = np.mean(arr)
    median = np.median(arr)
    std    = np.std(arr)
else:
    n      = len(scores)
    mean   = sum(scores) / n
    sorted_s = sorted(scores)
    mid    = n // 2
    median = sorted_s[mid] if n % 2 else (sorted_s[mid-1] + sorted_s[mid]) / 2
    variance = sum((x - mean) ** 2 for x in scores) / n
    std    = math.sqrt(variance)

above_mean = [s for s in scores if s > mean]
pct_above  = len(above_mean) / len(scores) * 100

print(f"Scores:      {scores}")
print(f"Mean:        {mean:.2f}")
print(f"Median:      {median:.1f}")
print(f"Std Dev:     {std:.2f}")
print(f"Above mean:  {pct_above:.0f}%")
"""
            },
            "challenge_variations": [
                "Variation 1: Create a requirements.txt for a project that needs numpy, pandas, and requests.",
                "Variation 2: Write a script that checks whether numpy is installed and prints a helpful message if not.",
                "Variation 3: Use pandas to create a DataFrame from a list of dicts and print df.describe().",
                "Variation 4: Demonstrate the difference between global and venv installs by listing site-packages.",
                "Variation 5: Use numpy to compute the dot product of two sales vectors.",
                "Variation 6: Create a pandas DataFrame from a CSV file and filter rows by a condition.",
                "Variation 7: Use numpy boolean indexing to find all scores in the top quartile.",
                "Variation 8: Build a simple requirements.txt parser that prints each package name and version.",
                "Variation 9: Use pandas groupby to summarize sales by region from a DataFrame.",
                "Variation 10: Write a setup script that creates a venv, installs requirements, and runs a test."
            ]
        },
        {
            "id": "m1-capstone",
            "title": "Capstone — Student Data Management System",
            "order": 26,
            "duration_min": 35,
            "is_capstone": True,
            "real_world_context": "You're building a real mini-application. Every concept from this module — classes, file I/O, error handling, dicts, lists, functions, string methods, type hints — comes together here. This is the kind of project you'll show in a portfolio or describe in an interview.",
            "concept": """You've completed all 25 lessons of Module 1. Now it's time to build something real.

In this capstone you'll build a **Student Data Management System** — a command-driven application that manages a roster of students with their grades.

**What you'll apply from each lesson:**
- **Variables & types (l1-l4):** Student attributes
- **if/elif/else (l5):** Grade classification
- **Loops (l6):** Processing all students
- **Functions (l7):** Modular, reusable operations
- **Lists (l8):** Storing student records and grades
- **Dicts (l9):** Student data structure
- **Classes (l15-l16):** Student and Gradebook objects
- **File I/O (l13):** Save and load roster from CSV
- **Error handling (l14):** Validate input, handle missing files
- **String methods (l20):** Clean and format data
- **Type hints (l22):** Document your code professionally
- **Nested data (l24):** Gradebook with multiple students

**System requirements:**
1. A `Student` class with name, student_id, and a grades list
2. A `Gradebook` class that manages a collection of Students
3. Methods: add_student, record_grade, get_report, class_average
4. Save/load the roster to/from a CSV file
5. Error handling for invalid grades, missing students, and file errors

Here's a skeleton to get you started:

```python
import csv
from datetime import date

class Student:
    def __init__(self, name: str, student_id: int):
        self.name       = name
        self.student_id = student_id
        self.grades: list[float] = []

    def add_grade(self, grade: float) -> None:
        if not 0 <= grade <= 100:
            raise ValueError(f"Grade {grade} must be between 0 and 100.")
        self.grades.append(grade)

    def average(self) -> float | None:
        if not self.grades:
            return None
        return round(sum(self.grades) / len(self.grades), 2)

    def letter_grade(self) -> str:
        avg = self.average()
        if avg is None: return "N/A"
        if avg >= 90:   return "A"
        elif avg >= 80: return "B"
        elif avg >= 70: return "C"
        elif avg >= 60: return "D"
        else:           return "F"

    def __str__(self) -> str:
        return f"[{self.student_id}] {self.name} — Avg: {self.average()} ({self.letter_grade()})"


class Gradebook:
    def __init__(self):
        self.students: dict[int, Student] = {}   # id → Student

    def add_student(self, name: str, student_id: int) -> None:
        if student_id in self.students:
            raise ValueError(f"Student ID {student_id} already exists.")
        self.students[student_id] = Student(name, student_id)

    def record_grade(self, student_id: int, grade: float) -> None:
        if student_id not in self.students:
            raise KeyError(f"No student with ID {student_id}.")
        self.students[student_id].add_grade(grade)

    def class_average(self) -> float | None:
        avgs = [s.average() for s in self.students.values() if s.average() is not None]
        return round(sum(avgs) / len(avgs), 2) if avgs else None

    def get_report(self) -> str:
        lines = ["Student Report", "=" * 40]
        for s in sorted(self.students.values(), key=lambda x: x.name):
            lines.append(str(s))
        lines.append(f"Class Average: {self.class_average()}")
        return "\\n".join(lines)

    def save_to_csv(self, filepath: str) -> None:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "grades"])
            for s in self.students.values():
                grades_str = ";".join(str(g) for g in s.grades)
                writer.writerow([s.student_id, s.name, grades_str])

    def load_from_csv(self, filepath: str) -> None:
        try:
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sid = int(row["student_id"])
                    self.add_student(row["name"], sid)
                    if row["grades"]:
                        for g in row["grades"].split(";"):
                            self.students[sid].add_grade(float(g))
        except FileNotFoundError:
            print(f"No saved file found at '{filepath}' — starting fresh.")
```

Your challenge is to complete the application below.""",
            "worked_example": {
                "description": "Here is a complete working demo of the system in action.",
                "code": """# This demonstrates how the completed system works:

gb = Gradebook()

# Add students
gb.add_student("Alice Chen", 1001)
gb.add_student("Bob Smith",  1002)
gb.add_student("Carol Diaz", 1003)

# Record grades
for grade in [92, 88, 95, 90]:
    gb.record_grade(1001, grade)
for grade in [72, 68, 75, 71]:
    gb.record_grade(1002, grade)
for grade in [85, 88, 91, 87]:
    gb.record_grade(1003, grade)

# Print report
print(gb.get_report())

# Save and reload
gb.save_to_csv("gradebook.csv")
gb2 = Gradebook()
gb2.load_from_csv("gradebook.csv")
print("\\nAfter save/load:")
print(gb2.get_report())
""",
                "explanation": "This demo shows the full workflow: create a Gradebook, add students, record grades, generate a report, save to CSV, and load back. The system handles all the complexity internally — the code that uses it is clean and readable."
            },
            "difficulty": "advanced",
            "reference": {
                "key_syntax": [
                    "All Module 1 concepts combined",
                    "class Student / class Gradebook",
                    "csv.reader / csv.DictWriter",
                    "try/except for file and validation errors",
                    "type hints on all methods",
                    "sorted(iterable, key=lambda ...)",
                    "dict[int, Student]  # typed dict"
                ],
                "notes": "Break the problem into small steps. Get the Student class working first, then Gradebook, then CSV I/O, then put it all together. Test each piece independently."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "In the Gradebook class, why store students as a dict keyed by student_id rather than a list?",
                    "options": [
                        "A. Dicts use less memory than lists",
                        "B. Looking up a student by ID is O(1) in a dict vs O(n) in a list",
                        "C. Lists cannot store Student objects",
                        "D. Dict keys must be integers"
                    ],
                    "answer": 1,
                    "explanation": "When you frequently look up items by a unique identifier (like student_id), a dict gives instant O(1) access. With a list you'd have to loop through all students to find one — O(n), which is slow for large rosters."
                },
                {
                    "type": "true_false",
                    "question": "Saving grades as '92;88;95' in a CSV cell and splitting on ';' when reading is a valid approach for storing a list of numbers.",
                    "answer": True,
                    "explanation": "CSV cells are strings, so you can't store a list directly. Joining with a delimiter and splitting on load is a common, practical workaround for simple cases."
                },
                {
                    "type": "fill_blank",
                    "question": "Complete the method signature for add_student with proper type hints and no return value.",
                    "template": "def add_student(self, name: ___, student_id: ___) -> ___:",
                    "answer": "str, int, None",
                    "explanation": "name is a str, student_id is an int, and the method returns nothing so the return type is None."
                }
            ],
            "challenge": {
                "instructions": "Build the complete Student Data Management System using the skeleton provided in the concept section. Your implementation must: (1) implement the full Student class with add_grade, average, letter_grade, and __str__, (2) implement the full Gradebook class with add_student, record_grade, class_average, get_report, save_to_csv, and load_from_csv, (3) add at least 4 students with at least 3 grades each, (4) print the full report, (5) save to 'gradebook.csv', (6) load into a new Gradebook instance and print the report again to verify the save/load works, (7) demonstrate error handling by catching a ValueError when adding an invalid grade (e.g., 105).",
                "starter_code": """import csv
from datetime import date

# ── Student class ─────────────────────────────────────────
class Student:
    def __init__(self, name: str, student_id: int):
        # Initialize name, student_id, and an empty grades list
        pass

    def add_grade(self, grade: float) -> None:
        # Validate 0-100, then append; raise ValueError if invalid
        pass

    def average(self) -> float | None:
        # Return rounded average or None if no grades
        pass

    def letter_grade(self) -> str:
        # Return A/B/C/D/F/N/A based on average
        pass

    def __str__(self) -> str:
        # Return formatted string representation
        pass


# ── Gradebook class ───────────────────────────────────────
class Gradebook:
    def __init__(self):
        self.students: dict = {}   # student_id → Student

    def add_student(self, name: str, student_id: int) -> None:
        # Add student; raise ValueError if ID already exists
        pass

    def record_grade(self, student_id: int, grade: float) -> None:
        # Look up student by ID; raise KeyError if not found
        pass

    def class_average(self) -> float | None:
        # Average of all students' averages
        pass

    def get_report(self) -> str:
        # Build and return a formatted report string
        pass

    def save_to_csv(self, filepath: str) -> None:
        # Write gradebook to CSV (id, name, grades as semicolon-joined string)
        pass

    def load_from_csv(self, filepath: str) -> None:
        # Load from CSV; handle FileNotFoundError gracefully
        pass


# ── Demo ──────────────────────────────────────────────────
gb = Gradebook()

# Add 4+ students and record 3+ grades each

# Print report

# Save to CSV

# Load into new Gradebook and print report

# Demonstrate error handling for invalid grade

""",
                "tests": [
                    {"type": "code_contains", "value": "class Student"},
                    {"type": "code_contains", "value": "class Gradebook"},
                    {"type": "code_contains", "value": "save_to_csv"},
                    {"type": "code_contains", "value": "load_from_csv"},
                    {"type": "code_contains", "value": "try"},
                    {"type": "output_contains", "value": "Class Average"},
                    {"type": "runs_without_error"}
                ],
                "solution": """import csv
from datetime import date

class Student:
    def __init__(self, name: str, student_id: int):
        self.name       = name
        self.student_id = student_id
        self.grades: list = []

    def add_grade(self, grade: float) -> None:
        if not 0 <= grade <= 100:
            raise ValueError(f"Grade {grade} must be between 0 and 100.")
        self.grades.append(grade)

    def average(self):
        if not self.grades:
            return None
        return round(sum(self.grades) / len(self.grades), 2)

    def letter_grade(self) -> str:
        avg = self.average()
        if avg is None: return "N/A"
        if avg >= 90:   return "A"
        elif avg >= 80: return "B"
        elif avg >= 70: return "C"
        elif avg >= 60: return "D"
        else:           return "F"

    def __str__(self) -> str:
        return f"[{self.student_id}] {self.name:15} Avg: {self.average()} ({self.letter_grade()})"


class Gradebook:
    def __init__(self):
        self.students = {}

    def add_student(self, name: str, student_id: int) -> None:
        if student_id in self.students:
            raise ValueError(f"Student ID {student_id} already exists.")
        self.students[student_id] = Student(name, student_id)

    def record_grade(self, student_id: int, grade: float) -> None:
        if student_id not in self.students:
            raise KeyError(f"No student with ID {student_id}.")
        self.students[student_id].add_grade(grade)

    def class_average(self):
        avgs = [s.average() for s in self.students.values() if s.average() is not None]
        return round(sum(avgs) / len(avgs), 2) if avgs else None

    def get_report(self) -> str:
        lines = ["\\nStudent Report", "=" * 45]
        for s in sorted(self.students.values(), key=lambda x: x.name):
            lines.append(str(s))
        lines.append(f"{'Class Average:':20} {self.class_average()}")
        return "\\n".join(lines)

    def save_to_csv(self, filepath: str) -> None:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "grades"])
            for s in self.students.values():
                grades_str = ";".join(str(g) for g in s.grades)
                writer.writerow([s.student_id, s.name, grades_str])
        print(f"Gradebook saved to '{filepath}'.")

    def load_from_csv(self, filepath: str) -> None:
        try:
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sid = int(row["student_id"])
                    self.add_student(row["name"], sid)
                    if row["grades"]:
                        for g in row["grades"].split(";"):
                            self.students[sid].add_grade(float(g))
            print(f"Gradebook loaded from '{filepath}'.")
        except FileNotFoundError:
            print(f"No file found at '{filepath}' — starting fresh.")


# ── Demo ─────────────────────────────────────────────────
gb = Gradebook()

gb.add_student("Alice Chen",  1001)
gb.add_student("Bob Smith",   1002)
gb.add_student("Carol Diaz",  1003)
gb.add_student("David Park",  1004)

for g in [92, 88, 95, 90]: gb.record_grade(1001, g)
for g in [72, 68, 75, 71]: gb.record_grade(1002, g)
for g in [85, 88, 91, 87]: gb.record_grade(1003, g)
for g in [55, 60, 58, 62]: gb.record_grade(1004, g)

print(gb.get_report())

gb.save_to_csv("gradebook.csv")

gb2 = Gradebook()
gb2.load_from_csv("gradebook.csv")
print("\\nVerification after save/load:")
print(gb2.get_report())

# Error handling demo
try:
    gb.record_grade(1001, 105)
except ValueError as e:
    print(f"\\nCaught expected error: {e}")
"""
            },
            "challenge_variations": [
                "Variation 1: Add a remove_student method that deletes a student and their grades.",
                "Variation 2: Add a top_student property that returns the Student with the highest average.",
                "Variation 3: Extend Student to track assignment name alongside each grade (store as list of tuples).",
                "Variation 4: Add a grade_distribution method that returns counts of A, B, C, D, F grades.",
                "Variation 5: Add a search_student(name) method that finds students by partial name match.",
                "Variation 6: Save the gradebook as JSON instead of CSV using the json module.",
                "Variation 7: Add a command-line interface so users can type 'add', 'grade', 'report', 'save', 'quit'.",
                "Variation 8: Add email validation when creating a Student with an email attribute.",
                "Variation 9: Add an attendance tracker to Student that records present/absent by date.",
                "Variation 10: Extend Gradebook to support multiple courses, each with its own roster and grades."
            ]
        }
    ]
}
