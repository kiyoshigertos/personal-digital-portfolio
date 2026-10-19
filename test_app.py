import unittest
import json
import os
from app import app, init_db, get_db_connection

class PortfolioAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        init_db()

    def tearDown(self):
        """Clean up any test contact rows so tests remain idempotent."""
        conn = get_db_connection()
        conn.execute("DELETE FROM contact_messages WHERE email LIKE '%@example.com'")
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Positive-path tests
    # ------------------------------------------------------------------

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Michael Angelo Gertos', response.data)
        self.assertIn(b'SmartPOS', response.data)
        self.assertIn(b'ELARA AI', response.data)
        self.assertIn(b'Philippine Countryville College', response.data)
        self.assertIn(b'Computer Systems Servicing', response.data)
        self.assertIn(b'Harvey', response.data)

    def test_projects_page(self):
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Featured Projects', response.data)

    def test_project_detail_routes(self):
        for slug in ['smartpos', 'elara-ai', 'smart-bin', 'space-dodger']:
            response = self.client.get(f'/project/{slug}')
            self.assertEqual(response.status_code, 200, f"Failed for project slug: {slug}")
            self.assertIn(b'Project Case Study', response.data)

    def test_api_projects(self):
        response = self.client.get('/api/projects')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 4)

    def test_api_project_detail(self):
        response = self.client.get('/api/project/smartpos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['project']['title'], 'SmartPOS')

    def test_api_certifications(self):
        response = self.client.get('/api/certifications')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 6)

    def test_api_certification_detail(self):
        response = self.client.get('/api/certifications/tesda-nc2-css')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('Computer Systems Servicing', data['certification']['title'])
        self.assertEqual(data['certification']['cert_no'], '24101302001324')

    def test_contact_form_submission(self):
        payload = {
            "name": "Jane Tester",
            "email": "jane.tester@example.com",
            "subject": "System Collaboration",
            "message": "Hello Michael, love your SmartPOS project!"
        }
        response = self.client.post('/api/contact', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

        # Check DB
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM contact_messages WHERE email = ?', ('jane.tester@example.com',)).fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], 'Jane Tester')

    def test_download_resume(self):
        response = self.client.get('/download-resume')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/pdf')
        response.close()

    def test_favicon_route(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'svg', response.mimetype.encode())
        response.close()

    def test_serverless_entrypoint_import(self):
        from api.index import app as vercel_app
        self.assertIsNotNone(vercel_app)
        self.assertEqual(vercel_app.name, 'app')

    def test_404_error_page(self):
        response = self.client.get('/invalid-page-does-not-exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)
        self.assertIn(b'Page Not Found', response.data)

    # ------------------------------------------------------------------
    # Negative-path tests
    # ------------------------------------------------------------------

    def test_contact_missing_name(self):
        """Contact form should reject submissions with no name."""
        response = self.client.post('/api/contact', json={
            "name": "",
            "email": "valid@example.com",
            "message": "Some message"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

    def test_contact_missing_email(self):
        """Contact form should reject submissions with no email."""
        response = self.client.post('/api/contact', json={
            "name": "Jane",
            "email": "",
            "message": "Some message"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

    def test_contact_invalid_email_format(self):
        """Contact form should reject emails that lack @ or a dot."""
        response = self.client.post('/api/contact', json={
            "name": "Jane",
            "email": "notanemail",
            "message": "Some message"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

    def test_contact_missing_message(self):
        """Contact form should reject submissions with no message body."""
        response = self.client.post('/api/contact', json={
            "name": "Jane",
            "email": "valid@example.com",
            "message": ""
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

    def test_api_project_unknown_slug(self):
        """API should return 404 JSON for an unknown project slug."""
        response = self.client.get('/api/project/does-not-exist')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

    def test_project_detail_unknown_slug(self):
        """HTML route should return 404 for an unknown project slug."""
        response = self.client.get('/project/nonexistent-project')
        self.assertEqual(response.status_code, 404)

    def test_api_certification_unknown_id(self):
        """API should return 404 JSON for an unknown certification ID."""
        response = self.client.get('/api/certifications/fake-cert-id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')


if __name__ == '__main__':
    unittest.main()
