import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class RecommendationApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_recommendations_endpoint_returns_results(self) -> None:
        response = self.client.post(
            "/api/v1/recommendations",
            json={
                "query": "找一个安静、预算不超过 200 的餐厅",
                "city": "Phoenix",
                "limit": 5,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("recommendations", payload)
        self.assertIn("summary", payload)
        self.assertIsInstance(payload["recommendations"], list)
        if payload["recommendations"]:
            item = payload["recommendations"][0]
            self.assertIn("business_id", item)
            self.assertIn("name", item)
            self.assertIn("reason", item)


if __name__ == "__main__":
    unittest.main()
