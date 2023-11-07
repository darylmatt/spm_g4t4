import unittest
from app import app,db
from db_config.models import Application
import json
import logging

class TestApplyRole(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.application_id = None

    def tearDown(self):
        if self.application_id:
            with app.app_context():
                application = Application.query.get(self.application_id)
                if application:
                    db.session.delete(application)
                    db.session.commit()


    def test_apply_role(self):
        test_data = {
            "listing_id": 21
        }

        with self.client.session_transaction() as sess:
            sess["Staff_ID"] = 140002
            sess["Role"] = 2

        headers = {"Content-Type": "application/json"}

        response = self.client.post('/apply_role/21', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        self.assertEqual(
            response.status_code, 201
        )

        data = json.loads(response.data.decode("utf-8"))
        self.application_id = data.get("application_id")
        logging.info(f"Application ID in application: {self.application_id}")
        
    def test_apply_existing_role(self):
        global application_id
        test_data = {
            "listing_id": 17
        }

        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 140002
            sess['Role'] = 2

        headers = {
            "Content-Type": "application/json"
        }

        response = self.client.post('/apply_role/17', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 400)

        expected_error_message = "You have already applied to this role"
        self.assertIn(expected_error_message, response.get_json()['error'])

    def test_apply_closed_role(self):
        global application_id
        test_data = {
            "listing_id": 18
        }

        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 140002
            sess['Role'] = 2

        headers = {
            "Content-Type": "application/json"
        }

        response = self.client.post('/apply_role/18', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 411)

        expected_error_message = "Role listing is closed or not yet open for applications"
        self.assertIn(expected_error_message, response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
