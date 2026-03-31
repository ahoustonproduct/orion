MODULE_5 = {
    "id": "module5",
    "title": "Build It Yourself — Systems & Tools",
    "description": "Understand how technology works by building it from scratch. You'll recreate web servers, databases, search engines, and more — using only Python.",
    "course": "Self-Directed · Build Your Own X",
    "order": 5,
    "locked": True,
    "lessons": [
        {
            "id": "m5-l1",
            "title": "Build Your Own Web Server",
            "order": 1,
            "duration_min": 20,
            "concept": """**What is a web server?**

A web server is a program that listens for incoming HTTP requests and sends back HTTP responses. Every website you visit goes through a web server.

When you type `http://example.com` in your browser, your browser:
1. Connects to the server at `example.com` on port 80
2. Sends an HTTP request: `GET / HTTP/1.1`
3. The server processes the request
4. The server sends back an HTTP response with HTML content

Let's build a minimal web server using Python's `socket` module:

```python
import socket

HOST = "127.0.0.1"
PORT = 8080

# Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
print(f"Server running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()
    print(f"Request from {addr}: {request[:50]}")
    
    response = "HTTP/1.1 200 OK\\r\\n"
    response += "Content-Type: text/html\\r\\n"
    response += "\\r\\n"
    response += "<h1>Hello, World!</h1>"
    
    conn.sendall(response.encode())
    conn.close()
```

**Key concepts:**
- **Socket** — An endpoint for network communication
- **TCP** — Reliable, ordered delivery of data
- **HTTP Request** — What the browser sends (method, path, headers)
- **HTTP Response** — What the server sends back (status code, headers, body)
- **Port** — A number that identifies which service to connect to""",
            "reference": {
                "key_syntax": [
                    "socket.socket(AF_INET, SOCK_STREAM)",
                    "server.bind((HOST, PORT))",
                    "server.listen(1)",
                    "conn, addr = server.accept()",
                    "conn.recv(1024)",
                    "conn.sendall(data.encode())",
                ],
                "notes": "Port 8080 is commonly used for development. Ports below 1024 require admin privileges."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does a web server listen for?",
                    "options": ["SQL queries", "HTTP requests", "Email messages", "File downloads"],
                    "answer": 1,
                    "explanation": "A web server listens for HTTP requests from clients (browsers) and sends back HTTP responses."
                },
                {
                    "type": "true_false",
                    "question": "A socket is an endpoint for network communication.",
                    "answer": True,
                    "explanation": "Correct! A socket is a communication endpoint that allows two programs to exchange data over a network."
                },
                {
                    "type": "multiple_choice",
                    "question": "What does server.accept() return?",
                    "options": [
                        "Just the request data",
                        "A connection object and the client address",
                        "The HTTP status code",
                        "The server's IP address"
                    ],
                    "answer": 1,
                    "explanation": "accept() returns a tuple of (connection_socket, client_address). The connection socket is used to communicate with that specific client."
                },
                {
                    "type": "true_false",
                    "question": "HTTP responses must include headers before the body.",
                    "answer": True,
                    "explanation": "Correct! HTTP responses start with a status line, then headers, then a blank line (\\r\\n\\r\\n), then the body."
                },
            ],
            "challenge": {
                "instructions": "Build a simple web server that responds with different messages based on the URL path. If the path is '/', return 'Home Page'. If the path is '/about', return 'About Page'. For any other path, return '404 Not Found'.",
                "starter_code": """import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
print(f"Server running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()
    
    # Parse the path from the request
    # Request looks like: GET /path HTTP/1.1
    lines = request.split("\\r\\n")
    if lines:
        parts = lines[0].split(" ")
        path = parts[1] if len(parts) > 1 else "/"
    
    # TODO: Set body based on path
    # If path is "/", body = "Home Page"
    # If path is "/about", body = "About Page"
    # Otherwise, body = "404 Not Found"
    
    body = "Home Page"  # Replace with your logic
    
    response = "HTTP/1.1 200 OK\\r\\n"
    response += "Content-Type: text/plain\\r\\n"
    response += "\\r\\n"
    response += body
    
    conn.sendall(response.encode())
    conn.close()
""",
                "solution": """import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
print(f"Server running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()
    lines = request.split("\\r\\n")
    if lines:
        parts = lines[0].split(" ")
        path = parts[1] if len(parts) > 1 else "/"
    
    if path == "/":
        body = "Home Page"
    elif path == "/about":
        body = "About Page"
    else:
        body = "404 Not Found"
    
    response = "HTTP/1.1 200 OK\\r\\n"
    response += "Content-Type: text/plain\\r\\n"
    response += "\\r\\n"
    response += body
    
    conn.sendall(response.encode())
    conn.close()
""",
            },
        },
        {
            "id": "m5-l2",
            "title": "Build Your Own Key-Value Database",
            "order": 2,
            "duration_min": 20,
            "concept": """**What is a key-value database?**

A key-value database is the simplest type of NoSQL database. You store data as pairs: a unique key and its associated value. Think of it like a Python dictionary that persists after your program ends.

Examples: Redis, DynamoDB, etcd

Let's build a simple key-value store that saves data to a file:

```python
import json
import os

class KVStore:
    def __init__(self, filepath="store.json"):
        self.filepath = filepath
        self.data = {}
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.data = json.load(f)
    
    def set(self, key, value):
        self.data[key] = value
        self._save()
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False
    
    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)

# Usage
db = KVStore()
db.set("name", "Alice")
db.set("age", 30)
print(db.get("name"))  # Alice
```

**Key concepts:**
- **Persistence** — Data survives after the program ends
- **Serialization** — Converting data to a storable format (JSON)
- **CRUD** — Create, Read, Update, Delete operations
- **Key-Value Store** — Simplest database model: unique keys map to values""",
            "reference": {
                "key_syntax": [
                    "json.dump(data, file)",
                    "json.load(file)",
                    "db.set(key, value)",
                    "db.get(key, default)",
                    "db.delete(key)",
                ],
                "notes": "This is a simple implementation. Real databases use B-trees, write-ahead logs, and memory-mapped files for performance."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does CRUD stand for?",
                    "options": [
                        "Create, Read, Update, Delete",
                        "Copy, Run, Upload, Download",
                        "Connect, Request, Update, Disconnect",
                        "Create, Retrieve, Upload, Delete"
                    ],
                    "answer": 0,
                    "explanation": "CRUD stands for Create, Read, Update, Delete — the four basic operations of persistent storage."
                },
                {
                    "type": "true_false",
                    "question": "A key-value store is the simplest type of database.",
                    "answer": True,
                    "explanation": "Correct! Key-value stores simply map unique keys to values, making them the simplest database model."
                },
                {
                    "type": "multiple_choice",
                    "question": "What is serialization?",
                    "options": [
                        "Encrypting data for security",
                        "Converting data to a storable/transmittable format",
                        "Sorting data in alphabetical order",
                        "Compressing data to save space"
                    ],
                    "answer": 1,
                    "explanation": "Serialization converts data structures into a format that can be stored (like JSON) or transmitted over a network."
                },
            ],
            "challenge": {
                "instructions": "Extend the KVStore class to add a `keys()` method that returns all keys, and a `has()` method that checks if a key exists. Then use them to count how many keys are in the database.",
                "starter_code": """import json
import os

class KVStore:
    def __init__(self, filepath="store.json"):
        self.filepath = filepath
        self.data = {}
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.data = json.load(f)
    
    def set(self, key, value):
        self.data[key] = value
        self._save()
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False
    
    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)
    
    # TODO: Add keys() method - return list of all keys
    # TODO: Add has(key) method - return True if key exists
    
    def count(self):
        # Use keys() to count entries
        pass

db = KVStore("test_store.json")
db.set("name", "Alice")
db.set("age", 30)
db.set("city", "NYC")
print(db.keys())
print(db.has("name"))
print(db.count())
""",
                "solution": """import json
import os

class KVStore:
    def __init__(self, filepath="store.json"):
        self.filepath = filepath
        self.data = {}
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.data = json.load(f)
    
    def set(self, key, value):
        self.data[key] = value
        self._save()
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False
    
    def keys(self):
        return list(self.data.keys())
    
    def has(self, key):
        return key in self.data
    
    def count(self):
        return len(self.keys())
    
    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)

db = KVStore("test_store.json")
db.set("name", "Alice")
db.set("age", 30)
db.set("city", "NYC")
print(db.keys())
print(db.has("name"))
print(db.count())
""",
            },
        },
        {
            "id": "m5-l3",
            "title": "Build Your Own Search Engine",
            "order": 3,
            "duration_min": 25,
            "concept": """**What is a search engine?**

A search engine indexes text content and lets you find relevant documents by keyword. Google, Elasticsearch, and SQLite's full-text search all work on similar principles.

The basic approach:
1. **Tokenize** — Split text into individual words (tokens)
2. **Index** — Build an inverted index: word → list of documents containing it
3. **Query** — Look up words in the index and return matching documents

```python
class SearchEngine:
    def __init__(self):
        self.index = {}  # word -> set of doc_ids
        self.docs = {}   # doc_id -> text
    
    def add_document(self, doc_id, text):
        self.docs[doc_id] = text
        tokens = text.lower().split()
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)
    
    def search(self, query):
        tokens = query.lower().split()
        if not tokens:
            return []
        # Start with documents matching the first word
        results = self.index.get(tokens[0], set()).copy()
        # Intersect with documents matching subsequent words
        for token in tokens[1:]:
            results &= self.index.get(token, set())
        return [self.docs[doc_id] for doc_id in results]

# Usage
engine = SearchEngine()
engine.add_document(1, "Python is great for data science")
engine.add_document(2, "Python is also great for web development")
engine.add_document(3, "Data science uses statistics and math")

print(engine.search("Python data"))
# ['Python is great for data science']
```

**Key concepts:**
- **Inverted Index** — Maps words to the documents that contain them
- **Tokenization** — Splitting text into individual words
- **Intersection** — Finding documents that contain ALL query words
- **TF-IDF** — Term Frequency-Inverse Document Frequency (advanced ranking)""",
            "reference": {
                "key_syntax": [
                    "text.lower().split()",
                    "index[word].add(doc_id)",
                    "results &= other_set",
                    "engine.search(query)",
                ],
                "notes": "This is a basic Boolean search. Real search engines use ranking (relevance scores), stemming, and fuzzy matching."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What is an inverted index?",
                    "options": [
                        "A list of documents sorted by date",
                        "A mapping from words to the documents that contain them",
                        "A reverse-ordered list of search results",
                        "A database table with inverted columns"
                    ],
                    "answer": 1,
                    "explanation": "An inverted index maps each word to the set of documents containing that word, enabling fast keyword lookups."
                },
                {
                    "type": "true_false",
                    "question": "Tokenization means splitting text into individual words.",
                    "answer": True,
                    "explanation": "Correct! Tokenization breaks text into tokens (usually words) for indexing and searching."
                },
                {
                    "type": "multiple_choice",
                    "question": "What does the & operator do with sets?",
                    "options": [
                        "Combines all elements from both sets",
                        "Finds elements common to both sets (intersection)",
                        "Removes elements from the first set",
                        "Compares set sizes"
                    ],
                    "answer": 1,
                    "explanation": "The & operator performs set intersection — it returns only elements that exist in both sets. This is how we find documents matching ALL query words."
                },
            ],
            "challenge": {
                "instructions": "Build a search engine that can search through a list of product descriptions. Add documents for at least 3 products, then search for products that match a given query. Return the matching product names.",
                "starter_code": """class SearchEngine:
    def __init__(self):
        self.index = {}
        self.docs = {}
    
    def add_document(self, doc_id, text):
        self.docs[doc_id] = text
        tokens = text.lower().split()
        for token in tokens:
            # Clean punctuation from tokens
            token = token.strip(".,!?;:")
            if token:
                if token not in self.index:
                    self.index[token] = set()
                self.index[token].add(doc_id)
    
    def search(self, query):
        tokens = query.lower().split()
        if not tokens:
            return []
        results = self.index.get(tokens[0], set()).copy()
        for token in tokens[1:]:
            results &= self.index.get(token, set())
        return [self.docs[doc_id] for doc_id in results]

# TODO: Create a search engine
# TODO: Add at least 3 products as documents
# TODO: Search for "python programming"
# TODO: Print the results

engine = SearchEngine()

# Add your products here

# Search and print results
""",
                "solution": """class SearchEngine:
    def __init__(self):
        self.index = {}
        self.docs = {}
    
    def add_document(self, doc_id, text):
        self.docs[doc_id] = text
        tokens = text.lower().split()
        for token in tokens:
            token = token.strip(".,!?;:")
            if token:
                if token not in self.index:
                    self.index[token] = set()
                self.index[token].add(doc_id)
    
    def search(self, query):
        tokens = query.lower().split()
        if not tokens:
            return []
        results = self.index.get(tokens[0], set()).copy()
        for token in tokens[1:]:
            results &= self.index.get(token, set())
        return [self.docs[doc_id] for doc_id in results]

engine = SearchEngine()
engine.add_document(1, "Python Programming for Beginners - Learn Python basics and data structures")
engine.add_document(2, "Advanced Python Programming - Master decorators and generators")
engine.add_document(3, "JavaScript Web Development - Build interactive websites")
engine.add_document(4, "Data Science with Python - Statistics and machine learning")

results = engine.search("python programming")
for r in results:
    print(r)
""",
            },
        },
        {
            "id": "m5-l4",
            "title": "Build Your Own Git (Version Control)",
            "order": 4,
            "duration_min": 20,
            "concept": """**What is version control?**

Version control tracks changes to files over time. Git is the most popular version control system. It lets you save snapshots (commits), branch off in different directions, and merge changes back together.

At its core, Git works by:
1. **Hashing** — Creating a unique fingerprint (SHA-256) for each file's content
2. **Storing** — Saving files with their hash as the identifier
3. **Linking** — Each commit points to a snapshot of files and the previous commit

```python
import hashlib
import json
import os

class MiniGit:
    def __init__(self, repo_dir=".minigit"):
        self.repo_dir = repo_dir
        os.makedirs(repo_dir, exist_ok=True)
    
    def hash_content(self, content):
        """Create a SHA-256 hash of file content."""
        return hashlib.sha256(content.encode()).hexdigest()[:8]
    
    def add(self, filename, content):
        """Stage a file by hashing its content."""
        file_hash = self.hash_content(content)
        filepath = os.path.join(self.repo_dir, file_hash)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Added {filename} ({file_hash})")
        return file_hash
    
    def log(self, commits):
        """Display commit history."""
        for i, commit in enumerate(reversed(commits)):
            print(f"Commit {len(commits)-i}: {commit['hash']}")
            print(f"  Message: {commit['message']}")
            print(f"  Files: {', '.join(commit['files'])}")
            print()

# Usage
repo = MiniGit()
hash1 = repo.add("hello.py", "print('Hello')")
hash2 = repo.add("hello.py", "print('Hello, World!')")
print(f"Hash 1: {hash1}")
print(f"Hash 2: {hash2}")
```

**Key concepts:**
- **Hash** — A unique fingerprint for content (same content = same hash)
- **Commit** — A saved snapshot with a message and timestamp
- **SHA-256** — A cryptographic hash function that produces 64-character hex strings
- **Content-addressable storage** — Files are stored by their hash, not their name""",
            "reference": {
                "key_syntax": [
                    "hashlib.sha256(content.encode()).hexdigest()",
                    "os.makedirs(dir, exist_ok=True)",
                    "hash[:8]",
                ],
                "notes": "Real Git uses SHA-1 (not SHA-256) and stores objects in a more complex format with headers."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does a hash function do?",
                    "options": [
                        "Encrypts data so only authorized users can read it",
                        "Creates a unique fingerprint for any input",
                        "Compresses files to save space",
                        "Sorts files alphabetically"
                    ],
                    "answer": 1,
                    "explanation": "A hash function takes any input and produces a fixed-size unique output. The same input always produces the same hash."
                },
                {
                    "type": "true_false",
                    "question": "In Git, files are stored by their hash, not their filename.",
                    "answer": True,
                    "explanation": "Correct! Git uses content-addressable storage — files are identified by their hash, which means identical files are stored only once."
                },
                {
                    "type": "multiple_choice",
                    "question": "What is a commit in Git?",
                    "options": [
                        "A promise to finish code later",
                        "A saved snapshot with a message and pointer to parent commits",
                        "A backup of the entire repository",
                        "A merge of two branches"
                    ],
                    "answer": 1,
                    "explanation": "A commit is a snapshot of files at a point in time, with a message describing the change and a pointer to the previous commit."
                },
            ],
            "challenge": {
                "instructions": "Build a simple version control system that tracks changes to a single file. Each time you 'commit', save the content with a hash and a message. Then implement a 'diff' function that shows what changed between two commits.",
                "starter_code": """import hashlib

class SimpleVC:
    def __init__(self):
        self.commits = []
    
    def hash_content(self, content):
        return hashlib.sha256(content.encode()).hexdigest()[:8]
    
    def commit(self, message, content):
        # TODO: Create a commit with hash, message, and content
        # TODO: Append to self.commits list
        # TODO: Print commit info
        pass
    
    def diff(self, commit_index_1, commit_index_2):
        # TODO: Compare content between two commits
        # TODO: Show what was added/removed (line by line)
        pass

vc = SimpleVC()
vc.commit("Initial version", "Hello World\\nThis is my program.")
vc.commit("Added greeting", "Hello World\\nThis is my program.\\nWelcome!")
vc.commit("Fixed typo", "Hello World\\nThis is my program.\\nWelcome!\\nThanks for visiting.")

# Show diff between first and last commit
vc.diff(0, 2)
""",
                "solution": """import hashlib

class SimpleVC:
    def __init__(self):
        self.commits = []
    
    def hash_content(self, content):
        return hashlib.sha256(content.encode()).hexdigest()[:8]
    
    def commit(self, message, content):
        file_hash = self.hash_content(content)
        commit = {
            "hash": file_hash,
            "message": message,
            "content": content,
        }
        self.commits.append(commit)
        print(f"[{file_hash}] {message}")
    
    def diff(self, commit_index_1, commit_index_2):
        content1 = self.commits[commit_index_1]["content"]
        content2 = self.commits[commit_index_2]["content"]
        lines1 = content1.split("\\n")
        lines2 = content2.split("\\n")
        
        print(f"Diff between commit {commit_index_1} and {commit_index_2}:")
        for line in lines1:
            if line not in lines2:
                print(f"- {line}")
        for line in lines2:
            if line not in lines1:
                print(f"+ {line}")

vc = SimpleVC()
vc.commit("Initial version", "Hello World\\nThis is my program.")
vc.commit("Added greeting", "Hello World\\nThis is my program.\\nWelcome!")
vc.commit("Fixed typo", "Hello World\\nThis is my program.\\nWelcome!\\nThanks for visiting.")

vc.diff(0, 2)
""",
            },
        },
        {
            "id": "m5-l5",
            "title": "Build Your Own Shell",
            "order": 5,
            "duration_min": 20,
            "concept": """**What is a shell?**

A shell is a command-line interpreter that lets you interact with your operating system. When you type `ls` or `cd` in a terminal, the shell parses your command, finds the program, and runs it.

The shell's job:
1. Read a command from the user
2. Parse it into a program name and arguments
3. Find the program on the system
4. Execute it and show the output

```python
import subprocess
import sys

def simple_shell():
    print("Simple Shell (type 'exit' to quit)")
    while True:
        try:
            # Show prompt
            cmd = input("$ ").strip()
            if not cmd:
                continue
            if cmd == "exit":
                print("Goodbye!")
                break
            
            # Parse command and arguments
            parts = cmd.split()
            program = parts[0]
            args = parts[1:]
            
            # Execute the command
            try:
                result = subprocess.run(
                    [program] + args,
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="", file=sys.stderr)
            except FileNotFoundError:
                print(f"Command not found: {program}")
        except (EOFError, KeyboardInterrupt):
            print()
            break

# Note: Don't run this in the code runner — it's interactive!
# But you can understand how it works:
cmd = "python -c 'print(42)'"
parts = cmd.split()
result = subprocess.run(parts, capture_output=True, text=True)
print(result.stdout.strip())
```

**Key concepts:**
- **Shell** — A command-line interpreter (bash, zsh, PowerShell)
- **subprocess** — Python module for running external commands
- **Parsing** — Breaking a command string into program name and arguments
- **stdout/stderr** — Standard output and error streams""",
            "reference": {
                "key_syntax": [
                    "subprocess.run([cmd, arg1, arg2], capture_output=True, text=True)",
                    "result.stdout",
                    "result.stderr",
                    "result.returncode",
                    "cmd.split()",
                ],
                "notes": "Real shells support pipes (|), redirection (>), variables ($VAR), and many more features."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does a shell do?",
                    "options": [
                        "Protects your computer from viruses",
                        "Parses and executes commands you type",
                        "Manages your files automatically",
                        "Compiles your code"
                    ],
                    "answer": 1,
                    "explanation": "A shell reads commands from the user, parses them, finds the programs, and executes them."
                },
                {
                    "type": "true_false",
                    "question": "subprocess.run() can capture both stdout and stderr.",
                    "answer": True,
                    "explanation": "Correct! With capture_output=True, subprocess.run() captures both standard output and standard error."
                },
                {
                    "type": "multiple_choice",
                    "question": "What happens if you try to run a command that doesn't exist?",
                    "options": [
                        "The shell crashes",
                        "FileNotFoundError is raised",
                        "Nothing happens",
                        "The command runs anyway"
                    ],
                    "answer": 1,
                    "explanation": "If the program isn't found, subprocess.run() raises a FileNotFoundError. A real shell catches this and prints 'command not found'."
                },
            ],
            "challenge": {
                "instructions": "Build a simple command executor that can run basic Python commands. Parse a command string, run it with subprocess, and return the output. Handle the case where the command fails.",
                "starter_code": """import subprocess

def run_command(cmd):
    # TODO: Split the command into parts
    # TODO: Run the command with subprocess.run
    # TODO: Return a dict with 'output' and 'success' keys
    # If the command succeeds, output = stdout
    # If it fails, output = stderr
    pass

# Test cases
result1 = run_command("python -c 'print(2 + 2)'")
print(f"Success: {result1['success']}")
print(f"Output: {result1['output'].strip()}")

result2 = run_command("python -c 'print(hello)'")
print(f"Success: {result2['success']}")
print(f"Output: {result2['output'].strip()}")
""",
                "solution": """import subprocess

def run_command(cmd):
    parts = cmd.split()
    try:
        result = subprocess.run(parts, capture_output=True, text=True)
        if result.returncode == 0:
            return {"output": result.stdout, "success": True}
        else:
            return {"output": result.stderr, "success": False}
    except FileNotFoundError:
        return {"output": f"Command not found: {parts[0]}", "success": False}

result1 = run_command("python -c 'print(2 + 2)'")
print(f"Success: {result1['success']}")
print(f"Output: {result1['output'].strip()}")

result2 = run_command("python -c 'print(hello)'")
print(f"Success: {result2['success']}")
print(f"Output: {result2['output'].strip()}")
""",
            },
        },
        {
            "id": "m5-l6",
            "title": "Build Your Own Regex Engine",
            "order": 6,
            "duration_min": 25,
            "concept": """**What is a regex engine?**

Regular expressions (regex) are patterns used to match text. Behind the scenes, a regex engine converts the pattern into a state machine and checks if the input text matches.

Let's build a simple regex engine that supports:
- `.` — matches any character
- `*` — matches zero or more of the preceding character
- `^` — matches the start of the string
- `$` — matches the end of the string

```python
def match(pattern, text):
    """Simple regex engine supporting ., *, ^, $"""
    # Handle ^ anchor (must match from start)
    if pattern.startswith("^"):
        return match_here(pattern[1:], text)
    
    # Try matching at every position
    for i in range(len(text) + 1):
        if match_here(pattern, text[i:]):
            return True
    return False

def match_here(pattern, text):
    """Match pattern at the start of text."""
    if not pattern:
        return True
    if pattern == "$":
        return not text
    if len(pattern) >= 2 and pattern[1] == "*":
        return match_star(pattern[0], pattern[2:], text)
    if text and (pattern[0] == "." or pattern[0] == text[0]):
        return match_here(pattern[1:], text[1:])
    return False

def match_star(char, pattern, text):
    """Match zero or more of char, then pattern."""
    for i in range(len(text) + 1):
        if match_here(pattern, text[i:]):
            return True
        if i >= len(text) or (char != "." and text[i] != char):
            break
    return False

# Tests
print(match("a.c", "abc"))      # True
print(match("a.*c", "abbbc"))   # True
print(match("^hello", "hello world"))  # True
print(match("world$", "hello world"))  # True
```

**Key concepts:**
- **Pattern** — The regex expression to match against
- **Anchor** — `^` (start) and `$` (end) fix the match position
- **Wildcard** — `.` matches any single character
- **Quantifier** — `*` means zero or more of the preceding element
- **Recursive matching** — The engine tries matching at each position""",
            "reference": {
                "key_syntax": [
                    "def match(pattern, text)",
                    "pattern.startswith('^')",
                    "pattern[1:]  # slice off first char",
                    "text[i:]  # slice from position i",
                ],
                "notes": "This is a simplified engine. Real regex engines use finite automata (NFA/DFA) for better performance."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does the '.' character match in regex?",
                    "options": [
                        "Only a literal dot",
                        "Any single character",
                        "Zero or more characters",
                        "The end of a string"
                    ],
                    "answer": 1,
                    "explanation": "In regex, '.' is a wildcard that matches any single character."
                },
                {
                    "type": "true_false",
                    "question": "The '^' anchor means the pattern must match from the start of the string.",
                    "answer": True,
                    "explanation": "Correct! '^' anchors the pattern to the beginning of the string."
                },
                {
                    "type": "multiple_choice",
                    "question": "What does 'a*' match?",
                    "options": [
                        "Exactly one 'a'",
                        "Zero or more 'a' characters",
                        "One or more 'a' characters",
                        "The letter 'a' followed by '*'"
                    ],
                    "answer": 1,
                    "explanation": "The '*' quantifier means zero or more of the preceding element. So 'a*' matches '', 'a', 'aa', 'aaa', etc."
                },
            ],
            "challenge": {
                "instructions": "Use the regex engine to validate email-like patterns. Create a function that checks if a string matches the pattern 'word@word.word' (a simplified email format). Use the match function to test several strings.",
                "starter_code": """def match(pattern, text):
    if pattern.startswith("^"):
        return match_here(pattern[1:], text)
    for i in range(len(text) + 1):
        if match_here(pattern, text[i:]):
            return True
    return False

def match_here(pattern, text):
    if not pattern:
        return True
    if pattern == "$":
        return not text
    if len(pattern) >= 2 and pattern[1] == "*":
        return match_star(pattern[0], pattern[2:], text)
    if text and (pattern[0] == "." or pattern[0] == text[0]):
        return match_here(pattern[1:], text[1:])
    return False

def match_star(char, pattern, text):
    for i in range(len(text) + 1):
        if match_here(pattern, text[i:]):
            return True
        if i >= len(text) or (char != "." and text[i] != char):
            break
    return False

def is_valid_email(email):
    # TODO: Use match() to check if email matches the pattern
    # Pattern: one or more chars @ one or more chars . one or more chars
    # Hint: use ^ and $ anchors, and .+ for "one or more"
    # Note: .+ is . followed by .* (one or more = one + zero or more)
    pass

# Test cases
print(is_valid_email("user@example.com"))
print(is_valid_email("admin@test.org"))
print(is_valid_email("not-an-email"))
print(is_valid_email("@missing.com"))
""",
                "solution": """def match(pattern, text):
    if pattern.startswith("^"):
        return match_here(pattern[1:], text)
    for i in range(len(text) + 1):
        if match_here(pattern, text[i:]):
            return True
    return False

def match_here(pattern, text):
    if not pattern:
        return True
    if pattern == "$":
        return not text
    if len(pattern) >= 2 and pattern[1] == "*":
        return match_star(pattern[0], pattern[2:], text)
    if text and (pattern[0] == "." or pattern[0] == text[0]):
        return match_here(pattern[1:], text[1:])
    return False

def match_star(char, pattern, text):
    for i in range(len(text) + 1):
        if match_here(pattern, text[i:]):
            return True
        if i >= len(text) or (char != "." and text[i] != char):
            break
    return False

def is_valid_email(email):
    # Pattern: .+@.+\\..+$  (one+ chars @ one+ chars . one+ chars)
    # .+ is represented as .* preceded by one .
    pattern = "^.+@.+\\..+$"
    # Our engine doesn't support +, so use .* preceded by .
    # ^.+ = ^..*  (one char + zero or more)
    pattern = "^..*@..*\\...*$"
    return match(pattern, email)

print(is_valid_email("user@example.com"))
print(is_valid_email("admin@test.org"))
print(is_valid_email("not-an-email"))
print(is_valid_email("@missing.com"))
""",
            },
        },
        {
            "id": "m5-l7",
            "title": "Build Your Own Template Engine",
            "order": 7,
            "duration_min": 15,
            "concept": """**What is a template engine?**

A template engine lets you embed variables and logic inside text (usually HTML). Jinja2 (Python), EJS (JavaScript), and Django templates all work similarly.

The basic idea:
1. You write a template with placeholders: `"Hello, {{ name }}!"`
2. You provide data: `{"name": "Alice"}`
3. The engine replaces placeholders with actual values: `"Hello, Alice!"`

```python
import re

def render(template, data):
    """Simple template engine supporting {{ variable }} syntax."""
    def replace_var(match):
        var_name = match.group(1).strip()
        return str(data.get(var_name, ""))
    
    # Replace {{ variable }} with actual values
    result = re.sub(r"\\{\\{\\s*(\\w+)\\s*\\}\\}", replace_var, template)
    return result

# Usage
template = "Hello, {{ name }}! You are {{ age }} years old."
data = {"name": "Alice", "age": 30}
print(render(template, data))
# Hello, Alice! You are 30 years old.
```

**Key concepts:**
- **Template** — Text with embedded placeholders
- **Placeholder** — `{{ variable }}` syntax for inserting values
- **Context/Data** — The dictionary of values to substitute
- **Rendering** — The process of replacing placeholders with values""",
            "reference": {
                "key_syntax": [
                    "re.sub(pattern, replacement, text)",
                    "match.group(1)",
                    "data.get(var_name, default)",
                    "str(value)",
                ],
                "notes": "Real template engines also support loops ({% for %}), conditionals ({% if %}), and filters ({{ name|upper }})."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does a template engine do?",
                    "options": [
                        "Compiles code into machine language",
                        "Replaces placeholders in text with actual values",
                        "Creates visual templates for design",
                        "Generates random text"
                    ],
                    "answer": 1,
                    "explanation": "A template engine takes a template with placeholders and fills them with data values."
                },
                {
                    "type": "true_false",
                    "question": "The re.sub() function replaces all matches of a pattern in a string.",
                    "answer": True,
                    "explanation": "Correct! re.sub() finds all matches of a regex pattern and replaces them with the given replacement."
                },
                {
                    "type": "multiple_choice",
                    "question": "What does data.get(var_name, '') do?",
                    "options": [
                        "Deletes the variable from data",
                        "Returns the value or empty string if not found",
                        "Sets a new variable in data",
                        "Checks if the key exists"
                    ],
                    "answer": 1,
                    "explanation": "dict.get(key, default) returns the value for the key, or the default if the key doesn't exist."
                },
            ],
            "challenge": {
                "instructions": "Build a template engine that can handle nested variables with dot notation (e.g., {{ user.name }}). Parse the dot-separated path and look up nested values in the data dictionary.",
                "starter_code": """import re

def get_nested(data, path):
    # TODO: Split path by '.' and traverse nested dicts
    # Example: get_nested({"user": {"name": "Alice"}}, "user.name")
    # Should return "Alice"
    # If any key is missing, return ""
    pass

def render(template, data):
    def replace_var(match):
        var_path = match.group(1).strip()
        return str(get_nested(data, var_path))
    
    return re.sub(r"\\{\\{\\s*([\\w.]+)\\s*\\}\\}", replace_var, template)

# Test
template = "Hello, {{ user.name }}! Your email is {{ user.contact.email }}."
data = {
    "user": {
        "name": "Alice",
        "contact": {
            "email": "alice@example.com"
        }
    }
}
print(render(template, data))
""",
                "solution": """import re

def get_nested(data, path):
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return ""
    return str(current)

def render(template, data):
    def replace_var(match):
        var_path = match.group(1).strip()
        return str(get_nested(data, var_path))
    
    return re.sub(r"\\{\\{\\s*([\\w.]+)\\s*\\}\\}", replace_var, template)

template = "Hello, {{ user.name }}! Your email is {{ user.contact.email }}."
data = {
    "user": {
        "name": "Alice",
        "contact": {
            "email": "alice@example.com"
        }
    }
}
print(render(template, data))
""",
            },
        },
        {
            "id": "m5-l8",
            "title": "Build Your Own Neural Network",
            "order": 8,
            "duration_min": 30,
            "concept": """**What is a neural network?**

A neural network is a computing system inspired by biological brains. It consists of layers of interconnected nodes (neurons) that process input data to make predictions.

The simplest neural network:
1. **Input layer** — Receives the data
2. **Hidden layer** — Processes with weights and biases
3. **Output layer** — Produces the prediction

Each neuron computes: `output = activation(input * weight + bias)`

```python
import random

class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights randomly
        self.w1 = [[random.uniform(-1, 1) for _ in range(input_size)] 
                    for _ in range(hidden_size)]
        self.b1 = [0] * hidden_size
        self.w2 = [[random.uniform(-1, 1) for _ in range(hidden_size)] 
                    for _ in range(output_size)]
        self.b2 = [0] * output_size
    
    def sigmoid(self, x):
        """Activation function: squashes values to 0-1 range."""
        import math
        return 1 / (1 + math.exp(-max(-500, min(500, x))))
    
    def forward(self, inputs):
        """Pass data through the network."""
        # Hidden layer
        hidden = []
        for i in range(len(self.w1)):
            val = sum(inputs[j] * self.w1[i][j] for j in range(len(inputs)))
            val += self.b1[i]
            hidden.append(self.sigmoid(val))
        
        # Output layer
        output = []
        for i in range(len(self.w2)):
            val = sum(hidden[j] * self.w2[i][j] for j in range(len(hidden)))
            val += self.b2[i]
            output.append(self.sigmoid(val))
        
        return output

# Create a network: 2 inputs, 3 hidden neurons, 1 output
nn = SimpleNeuralNetwork(2, 3, 1)
result = nn.forward([0.5, 0.8])
print(f"Output: {result[0]:.4f}")
```

**Key concepts:**
- **Neuron** — A single processing unit that computes weighted sums
- **Weight** — How much influence each input has
- **Bias** — A constant offset added to each neuron
- **Activation function** — Introduces non-linearity (sigmoid, ReLU)
- **Forward pass** — Computing output from input through all layers""",
            "reference": {
                "key_syntax": [
                    "sigmoid(x) = 1 / (1 + exp(-x))",
                    "sum(inputs[j] * weights[i][j])",
                    "output = activation(weighted_sum + bias)",
                ],
                "notes": "This is a feedforward network without training. Real networks use backpropagation to adjust weights based on errors."
            },
            "questions": [
                {
                    "type": "multiple_choice",
                    "question": "What does the sigmoid activation function do?",
                    "options": [
                        "Multiplies inputs by weights",
                        "Squashes any value to a range between 0 and 1",
                        "Adds a bias to the input",
                        "Randomizes the weights"
                    ],
                    "answer": 1,
                    "explanation": "The sigmoid function maps any input value to a value between 0 and 1, introducing non-linearity."
                },
                {
                    "type": "true_false",
                    "question": "Weights determine how much influence each input has on a neuron's output.",
                    "answer": True,
                    "explanation": "Correct! Weights are the parameters that the network learns — they determine the strength of each connection."
                },
                {
                    "type": "multiple_choice",
                    "question": "What is a forward pass?",
                    "options": [
                        "Adjusting weights based on errors",
                        "Computing the output from input through all layers",
                        "Initializing random weights",
                        "Loading training data"
                    ],
                    "answer": 1,
                    "explanation": "A forward pass computes the network's output by passing input data through each layer, applying weights, biases, and activations."
                },
            ],
            "challenge": {
                "instructions": "Build a neural network that can learn the AND logic gate. Create a network with 2 inputs, 2 hidden neurons, and 1 output. Test it with all 4 combinations of inputs (0,0), (0,1), (1,0), (1,1). The output should be close to 1 only when both inputs are 1.",
                "starter_code": """import math
import random

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = [[random.uniform(-1, 1) for _ in range(input_size)] 
                    for _ in range(hidden_size)]
        self.b1 = [0] * hidden_size
        self.w2 = [[random.uniform(-1, 1) for _ in range(hidden_size)] 
                    for _ in range(output_size)]
        self.b2 = [0] * output_size
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-500, min(500, x))))
    
    def forward(self, inputs):
        hidden = []
        for i in range(len(self.w1)):
            val = sum(inputs[j] * self.w1[i][j] for j in range(len(inputs)))
            val += self.b1[i]
            hidden.append(self.sigmoid(val))
        
        output = []
        for i in range(len(self.w2)):
            val = sum(hidden[j] * self.w2[i][j] for j in range(len(hidden)))
            val += self.b2[i]
            output.append(self.sigmoid(val))
        
        return output

# TODO: Create a network with 2 inputs, 2 hidden, 1 output
# TODO: Test with all 4 AND gate combinations
# (0,0) -> ~0, (0,1) -> ~0, (1,0) -> ~0, (1,1) -> ~1

nn = NeuralNetwork(2, 2, 1)

# Set weights manually to make it work as AND gate
# Hint: both inputs need to be high for output to be high
nn.w1 = [[2, 2], [2, 2]]
nn.b1 = [-1, -3]
nn.w2 = [[2, -1]]
nn.b2 = [-1]

# Test all combinations
for a in [0, 1]:
    for b in [0, 1]:
        result = nn.forward([a, b])
        print(f"AND({a}, {b}) = {result[0]:.4f}")
""",
                "solution": """import math
import random

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = [[random.uniform(-1, 1) for _ in range(input_size)] 
                    for _ in range(hidden_size)]
        self.b1 = [0] * hidden_size
        self.w2 = [[random.uniform(-1, 1) for _ in range(hidden_size)] 
                    for _ in range(output_size)]
        self.b2 = [0] * output_size
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-500, min(500, x))))
    
    def forward(self, inputs):
        hidden = []
        for i in range(len(self.w1)):
            val = sum(inputs[j] * self.w1[i][j] for j in range(len(inputs)))
            val += self.b1[i]
            hidden.append(self.sigmoid(val))
        
        output = []
        for i in range(len(self.w2)):
            val = sum(hidden[j] * self.w2[i][j] for j in range(len(hidden)))
            val += self.b2[i]
            output.append(self.sigmoid(val))
        
        return output

nn = NeuralNetwork(2, 2, 1)

nn.w1 = [[2, 2], [2, 2]]
nn.b1 = [-1, -3]
nn.w2 = [[2, -1]]
nn.b2 = [-1]

for a in [0, 1]:
    for b in [0, 1]:
        result = nn.forward([a, b])
        print(f"AND({a}, {b}) = {result[0]:.4f}")
""",
            },
        },
    ],
}
