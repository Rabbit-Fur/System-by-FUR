import os
import sys
import tempfile
import unittest
from flask import session

# Ensure project root is in sys.path so Blueprints can be found
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from app import create_app, get_db

class DashboardFunctionsTest(unittest.TestCase):
    """Tests for admin dashboard and agent services."""

    def setUp(self):
        # Set up a temp database
        self.db_fd, db_path = tempfile.mkstemp()
        os.environ['DATABASE_PATH'] = db_path
        os.environ['FLASK_ENV'] = 'development'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db = get_db()
            # Create admin_users table and insert a test user
            db.execute(
                'CREATE TABLE IF NOT EXISTS admin_users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
            )
            db.execute(
                'INSERT INTO admin_users (username, password) VALUES (?, ?)',
                ('admin', 'pass')
            )
            db.commit()
        # Log in as admin
        with self.client.session_transaction() as sess:
            sess['admin_logged_in'] = True
            sess['admin_username'] = 'admin'

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(os.environ['DATABASE_PATH'])

    def test_dashboard_page(self):
        """Dashboard page should be accessible to admin."""
        resp = self.client.get('/admin/dashboard')
        self.assertEqual(resp.status_code, 200)

    def test_create_event_page(self):
        """Create Event GET loads the form."""
        resp = self.client.get('/admin/events/create')
        self.assertEqual(resp.status_code, 200)

    def test_create_event_post(self):
        """Create Event POST returns valid response (200 or redirect)."""
        resp = self.client.post('/admin/events/create', data={'name':'Test','date':'2025-05-05'})
        self.assertIn(resp.status_code, (200, 302))

    def test_logout(self):
        """Logout should clear session and flash message."""
        resp = self.client.get('/admin/logout', follow_redirects=True)
        self.assertIn(b'Logged out', resp.data)

    def test_design_agent(self):
        """DesignAgent should generate a template string."""
        from app.services.design_agent import DesignAgent
        da = DesignAgent()
        tpl = da.generate_design_template('TestEvent')
        self.assertIsInstance(tpl, str)
        self.assertIn('TestEvent', tpl)

    def test_coding_agent(self):
        """CodingAgent should generate module code string."""
        from app.services.coding_agent import CodingAgent
        ca = CodingAgent()
        code = ca.generate_tool_module('TestSystem')
        self.assertIsInstance(code, str)
        self.assertIn('TestSystem', code)

if __name__ == '__main__':
    unittest.main()
