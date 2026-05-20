import json
import os
import unittest
from datetime import date

_test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".tmp", "tests"))
os.makedirs(_test_dir, exist_ok=True)
_test_db = os.path.join(_test_dir, "orion_test.db")
if os.path.exists(_test_db):
    os.remove(_test_db)

os.environ["ORION_DB_PATH"] = _test_db

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402
from models import (  # noqa: E402
    engine,
    SessionLocal,
    Notebook,
    UserProgress,
    BookmarkedPosition,
    ConfidenceRating,
    ReviewItem,
    ConceptMastery,
)


class BackendContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client_context.__exit__(None, None, None)
        engine.dispose()
        if os.path.exists(_test_db):
            os.remove(_test_db)

    def test_first_lesson_update_records_study_time_and_validates_confidence(self):
        user_key = "contract_progress_user"
        response = self.client.post(
            f"/progress/{user_key}/lesson",
            json={
                "lesson_id": "m01_l01",
                "stars": 3,
                "attempts": 1,
                "hints_used": 0,
                "completed": True,
                "time_spent_minutes": 5,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True, "stars": 3})

        progress = self.client.get(f"/progress/{user_key}").json()
        self.assertEqual(progress["study_log"][date.today().isoformat()], 5)

        invalid = self.client.post(
            f"/progress/{user_key}/confidence",
            json={"lesson_id": "m01_l01", "rating": 999},
        )
        self.assertEqual(invalid.status_code, 422)

    def test_sql_executor_uses_sandbox_database(self):
        ok = self.client.post(
            "/execute/sql",
            json={"query": "SELECT name, email FROM users LIMIT 1"},
        )
        self.assertEqual(ok.status_code, 200)
        self.assertIsNone(ok.json()["error"])
        self.assertEqual(ok.json()["columns"], ["name", "email"])

        blocked = self.client.post(
            "/execute/sql",
            json={"query": "SELECT * FROM user_progress LIMIT 1"},
        )
        self.assertEqual(blocked.status_code, 200)
        self.assertIn("no such table", blocked.json()["error"])

    def test_sql_executor_enforces_read_only_limits(self):
        rows = self.client.post(
            "/execute/sql",
            json={
                "query": (
                    "WITH RECURSIVE n(x) AS ("
                    "SELECT 1 UNION ALL SELECT x + 1 FROM n WHERE x < 600"
                    ") SELECT x FROM n"
                )
            },
        )
        self.assertEqual(rows.status_code, 200)
        self.assertIsNone(rows.json()["error"])
        self.assertEqual(rows.json()["row_count"], 500)
        self.assertEqual(rows.json()["rows"][0], [1])
        self.assertEqual(rows.json()["rows"][-1], [500])

        blocked_function = self.client.post(
            "/execute/sql",
            json={"query": "SELECT randomblob(16)"},
        )
        self.assertEqual(blocked_function.status_code, 200)
        self.assertIn("not allowed", blocked_function.json()["error"])

        too_long = self.client.post(
            "/execute/sql",
            json={"query": "SELECT " + ("1" * 10050)},
        )
        self.assertEqual(too_long.status_code, 200)
        self.assertIn("too long", too_long.json()["error"])

    def test_python_executor_blocks_unapproved_imports_and_remote_origins(self):
        ok = self.client.post("/execute/python", json={"code": "import math\nprint(math.sqrt(16))"})
        self.assertEqual(ok.status_code, 200)
        self.assertIsNone(ok.json()["error"])
        self.assertIn("4.0", ok.json()["output"])

        blocked_import = self.client.post(
            "/execute/python",
            json={"code": "from os import getcwd\nprint(getcwd())"},
        )
        self.assertEqual(blocked_import.status_code, 200)
        self.assertIn("Import not allowed", blocked_import.json()["error"])

        blocked_network = self.client.post(
            "/execute/python",
            json={"code": "import urllib.request\nprint('network')"},
        )
        self.assertEqual(blocked_network.status_code, 200)
        self.assertIn("Import not allowed", blocked_network.json()["error"])

        remote_origin = self.client.post(
            "/execute/python",
            headers={"origin": "http://192.0.2.10:3000"},
            json={"code": "print('remote')"},
        )
        self.assertEqual(remote_origin.status_code, 200)
        self.assertIn("local requests", remote_origin.json()["error"])

        too_long = self.client.post("/execute/python", json={"code": "#" * 26000})
        self.assertEqual(too_long.status_code, 200)
        self.assertIn("too long", too_long.json()["error"])

    def test_python_sqlite_challenges_run_only_in_memory(self):
        ok = self.client.post(
            "/execute/python",
            json={
                "code": """import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT)')
cursor.executemany('INSERT INTO products VALUES (?, ?)', [(1, 'Laptop'), (2, 'Mouse')])
print('products:', cursor.execute('SELECT name FROM products ORDER BY id').fetchall())
"""
            },
        )
        self.assertEqual(ok.status_code, 200)
        self.assertIsNone(ok.json()["error"], ok.json())
        self.assertIn("products:", ok.json()["output"])
        self.assertIn("Laptop", ok.json()["output"])

        file_db = self.client.post(
            "/execute/python",
            json={"code": "import sqlite3\nsqlite3.connect('lesson.db')\n"},
        )
        self.assertEqual(file_db.status_code, 200)
        self.assertIn(":memory:", file_db.json()["error"])

        attach = self.client.post(
            "/execute/python",
            json={
                "code": (
                    "import sqlite3\n"
                    "conn = sqlite3.connect(':memory:')\n"
                    "sql = \"ATTACH DATABASE 'lesson.db' AS lesson\"\n"
                    "conn.execute(sql)\n"
                )
            },
        )
        self.assertEqual(attach.status_code, 200)
        self.assertIn("not authorized", attach.json()["error"])

    def test_python_sqlalchemy_challenge_uses_memory_sqlite(self):
        ok = self.client.post(
            "/execute/python",
            json={
                "code": """from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Product(id=1, name='Laptop'), Product(id=2, name='Mouse')])
    session.commit()
    print([p.name for p in session.query(Product).order_by(Product.id).all()])
"""
            },
        )
        self.assertEqual(ok.status_code, 200)
        self.assertIsNone(ok.json()["error"], ok.json())
        self.assertIn("Laptop", ok.json()["output"])

        file_engine = self.client.post(
            "/execute/python",
            json={
                "code": "from sqlalchemy import create_engine\ncreate_engine('sqlite:///lesson.db')\n"
            },
        )
        self.assertEqual(file_engine.status_code, 200)
        self.assertIn("in-memory", file_engine.json()["error"])

    def test_api_security_headers_are_present(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["x-frame-options"], "DENY")
        self.assertIn("frame-ancestors 'none'", response.headers["content-security-policy"])

    def test_curriculum_normalizes_mixed_lesson_shapes(self):
        module = self.client.get("/curriculum/modules/module3")
        self.assertEqual(module.status_code, 200)
        self.assertEqual(len(module.json()["lessons"]), 30)
        self.assertEqual(module.json()["lessons"][8]["order"], 9)
        self.assertGreaterEqual(module.json()["lessons"][8]["duration_min"], 60)

        lesson = self.client.get("/curriculum/lessons/m3-l9")
        self.assertEqual(lesson.status_code, 200)
        body = lesson.json()
        self.assertIsInstance(body["concept"], str)
        self.assertGreaterEqual(len(body["questions"]), 20)
        self.assertIn("key_syntax", body["reference"])

    def test_notebook_lesson_requires_matching_user_scope(self):
        owner_key = "contract_notebook_owner"
        other_key = "contract_notebook_other"
        notebook_id = "notebook_1234-abcd"
        lesson_id = f"{notebook_id}-l1"

        with SessionLocal() as db:
            db.add(Notebook(
                id=notebook_id,
                user_key=owner_key,
                title="Private Notebook",
                status="ready",
                module_data={
                    "title": "Private Notebook",
                    "course": "Saved Module",
                    "lessons": [
                        {
                            "id": lesson_id,
                            "title": "Owner Only Lesson",
                            "concept": "Private concept",
                            "questions": [],
                        }
                    ],
                },
            ))
            db.commit()

        owner = self.client.get(f"/curriculum/lessons/{lesson_id}?user_key={owner_key}")
        self.assertEqual(owner.status_code, 200)
        self.assertEqual(owner.json()["title"], "Owner Only Lesson")

        anonymous = self.client.get(f"/curriculum/lessons/{lesson_id}")
        self.assertEqual(anonymous.status_code, 404)
        self.assertEqual(anonymous.json()["detail"], "Lesson not found")

        other = self.client.get(f"/curriculum/lessons/{lesson_id}?user_key={other_key}")
        self.assertEqual(other.status_code, 404)
        self.assertEqual(other.json()["detail"], "Lesson not found")

    def test_progress_bookmark_and_confidence_updates_are_non_destructive(self):
        user_key = "contract_safe_persistence_user"
        lesson_id = "m1-l1"

        first = self.client.post(
            f"/progress/{user_key}/lesson",
            json={
                "lesson_id": lesson_id,
                "stars": 3,
                "attempts": 4,
                "hints_used": 2,
                "completed": True,
                "time_spent_minutes": 0,
            },
        )
        self.assertEqual(first.status_code, 200)

        second = self.client.post(
            f"/progress/{user_key}/lesson",
            json={
                "lesson_id": lesson_id,
                "stars": 1,
                "attempts": 1,
                "hints_used": 0,
                "completed": False,
                "time_spent_minutes": 0,
            },
        )
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.json(), {"success": True, "stars": 3})

        progress = self.client.get(f"/progress/{user_key}").json()
        lesson_progress = next(item for item in progress["lessons"] if item["lesson_id"] == lesson_id)
        self.assertEqual(lesson_progress["stars"], 3)
        self.assertEqual(lesson_progress["attempts"], 4)
        self.assertTrue(lesson_progress["completed"])
        self.assertNotIn(lesson_id, progress["weak_topics"])
        self.assertIn(lesson_id, progress["mastered_concepts"])

        self.client.post(
            f"/progress/{user_key}/bookmark",
            json={
                "lesson_id": lesson_id,
                "step_index": 1,
                "sub_step": 2,
                "saved_code": "print('keep me')",
            },
        )
        bookmark_update = self.client.post(
            f"/progress/{user_key}/bookmark",
            json={"lesson_id": lesson_id, "step_index": 2, "sub_step": 0},
        )
        self.assertEqual(bookmark_update.status_code, 200)
        bookmark = self.client.get(f"/progress/{user_key}/bookmark/{lesson_id}").json()
        self.assertEqual(bookmark["step_index"], 2)
        self.assertEqual(bookmark["saved_code"], "print('keep me')")

        self.assertEqual(
            self.client.post(
                f"/progress/{user_key}/confidence",
                json={"lesson_id": lesson_id, "rating": 4},
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(
                f"/progress/{user_key}/confidence",
                json={"lesson_id": lesson_id, "rating": 2},
            ).status_code,
            200,
        )
        progress = self.client.get(f"/progress/{user_key}").json()
        self.assertEqual(progress["topic_confidence"][lesson_id], 2)

        with SessionLocal() as db:
            self.assertEqual(
                db.query(UserProgress).filter_by(user_key=user_key, lesson_id=lesson_id).count(),
                1,
            )
            self.assertEqual(
                db.query(BookmarkedPosition).filter_by(user_key=user_key, lesson_id=lesson_id).count(),
                1,
            )
            self.assertEqual(
                db.query(ConfidenceRating).filter_by(user_key=user_key, lesson_id=lesson_id).count(),
                1,
            )

    def test_review_misses_due_queue_and_mastery_are_separate_from_confidence(self):
        user_key = "contract_review_mastery_user"
        question = {
            "id": "risk-q1",
            "type": "multiple_choice",
            "question": "Which control catches a high-risk loan?",
            "options": ["Skip review", "Manual review", "Delete the row"],
            "correct_index": 1,
            "explanation": "High-risk loans should be reviewed before approval.",
            "concept_tags": ["risk_controls"],
        }

        added = self.client.post(
            f"/review/{user_key}/add",
            json={
                "question_id": "risk-q1",
                "lesson_id": "m1-l1",
                "question_json": json.dumps(question),
            },
        )
        self.assertEqual(added.status_code, 200)
        self.client.post(
            f"/review/{user_key}/add",
            json={
                "question_id": "risk-q1",
                "lesson_id": "m1-l1",
                "question_json": json.dumps(question),
            },
        )

        queue = self.client.get(f"/review/{user_key}/queue").json()
        self.assertEqual(queue["total_due"], 1)
        self.assertEqual(queue["due_review_count"], 1)
        self.assertEqual(queue["questions"][0]["question_id"], "risk-q1")
        self.assertEqual(queue["questions"][0]["wrong_count"], 2)
        self.assertEqual(queue["recent_misses"][0]["question_id"], "risk-q1")

        recorded = self.client.post(
            f"/review/{user_key}/record",
            json={"question_id": "risk-q1", "correct": True},
        )
        self.assertEqual(recorded.status_code, 200)
        queue = self.client.get(f"/review/{user_key}/queue").json()
        self.assertEqual(queue["total_due"], 0)
        self.assertEqual(queue["recent_misses"][0]["question_id"], "risk-q1")

        self.client.post(
            f"/progress/{user_key}/confidence",
            json={"lesson_id": "m1-l1", "rating": 4},
        )
        mastery_record = self.client.post(
            f"/mastery/{user_key}/record",
            json={"concept_tag": "risk_controls", "correct": False},
        )
        self.assertEqual(mastery_record.status_code, 200)

        progress = self.client.get(f"/progress/{user_key}").json()
        self.assertEqual(progress["topic_confidence"], {"m1-l1": 4})

        mastery = self.client.get(f"/mastery/{user_key}").json()
        self.assertEqual(mastery["tags"]["risk_controls"], 47)
        heatmap_row = next(item for item in mastery["heatmap_data"] if item["tag"] == "risk_controls")
        self.assertEqual(heatmap_row["attempts"], 1)

        with SessionLocal() as db:
            self.assertEqual(
                db.query(ReviewItem).filter_by(user_key=user_key, question_id="risk-q1").count(),
                1,
            )
            self.assertEqual(
                db.query(ConceptMastery).filter_by(user_key=user_key, concept_tag="risk_controls").count(),
                1,
            )

    def test_decision_evaluate_contract(self):
        response = self.client.post(
            "/decision/evaluate",
            json={
                "lesson_id": "m01_l01",
                "block_id": "decision_block",
                "decision_type": "policy_choice",
                "user_value": "approve",
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("score", body)
        self.assertIn("user_outcome", body)

    def test_quiz_generation_uses_built_in_questions(self):
        response = self.client.post(
            "/quiz/generate",
            json={"user_key": "contract_quiz_user", "lesson_ids": ["m1-l1"]},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body["questions"]), 1)
        self.assertEqual(body["questions"][0]["lesson_id"], "m1-l1")


if __name__ == "__main__":
    unittest.main()
