import unittest

from app import create_app


class SmokeTest(unittest.TestCase):
    """Basic smoke tests for the Flask application."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health(self):
        """Test the /health endpoint returns 200 OK."""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b"OK")

    def test_home_redirect(self):
        """Test the root redirects to landing page or returns 200."""
        resp = self.client.get("/")
        self.assertIn(resp.status_code, (200, 302, 301))


if __name__ == "__main__":
    unittest.main()
