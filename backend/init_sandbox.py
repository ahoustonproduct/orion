import sqlite3
import os

def init_sandbox():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sandbox.db")
    # Always recreate for a fresh sandbox
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            status TEXT
        )
    """)

    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com")
    ])

    cursor.executemany("INSERT INTO orders (user_id, amount, status) VALUES (?, ?, ?)", [
        (1, 99.99, "completed"),
        (1, 49.50, "pending"),
        (2, 199.00, "completed"),
        (3, 29.99, "completed")
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_sandbox()
