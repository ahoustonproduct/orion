import os
import unittest
from datetime import date

_test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".tmp", "tests"))
os.makedirs(_test_dir, exist_ok=True)
_test_db = os.path.join(_test_dir, "orion_test.db")
if os.path.exists(_test_db):
    os.remove(_test_db)

os.environ["ORION_DB_PATH"] = _test_db
os.environ["ORION_AI_ENABLED"] = "false"

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402
from models import engine  # noqa: E402


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

    def test_curriculum_normalizes_mixed_lesson_shapes(self):
        module = self.client.get("/curriculum/modules/module3")
        self.assertEqual(module.status_code, 200)
        self.assertEqual(module.json()["lessons"][8]["order"], 9)
        self.assertEqual(module.json()["lessons"][8]["duration_min"], 20)

        lesson = self.client.get("/curriculum/lessons/m3-l9")
        self.assertEqual(lesson.status_code, 200)
        body = lesson.json()
        self.assertIsInstance(body["concept"], str)
        self.assertGreater(len(body["questions"]), 0)
        self.assertIn("key_syntax", body["reference"])

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

    def test_quiz_generation_uses_built_in_questions_without_ai(self):
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
