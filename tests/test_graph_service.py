from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.graph_service import build_service


class CurriculumGraphTests(unittest.TestCase):
    def test_summary_shape(self) -> None:
        summary = build_service().summary()
        self.assertGreaterEqual(summary["courseCount"], 7)
        self.assertGreaterEqual(summary["capstonePathLength"], 2)

    def test_pathway_reaches_capstone(self) -> None:
        path = build_service().pathway("IS-101", "IS-410")
        self.assertEqual(path[0], "IS-101")
        self.assertEqual(path[-1], "IS-410")

    def test_course_api_lookup(self) -> None:
        client = TestClient(app)
        response = client.get("/api/courses/IS-320")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Analytics Engineering")


if __name__ == "__main__":
    unittest.main()
