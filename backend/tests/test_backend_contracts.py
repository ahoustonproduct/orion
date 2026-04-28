import os
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

_tmpdir = tempfile.TemporaryDirectory()
os.environ["ORION_DB_PATH"] = os.path.join(_tmpdir.name, "orion_test.db")

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402


class BackendContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client_context.__exit__(None, None, None)
        _tmpdir.cleanup()

    def test_first_lesson_update_starts_streak_and_validates_confidence(self):
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
        self.assertEqual(progress["streak"], 1)
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

    def test_ai_quiz_generation_falls_back_when_model_response_fails(self):
        with patch(
            "routes.quiz.client.chat.completions.create",
            side_effect=RuntimeError("model unavailable"),
        ):
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
