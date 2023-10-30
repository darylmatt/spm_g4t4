import unittest
from app import app 
import json
import logging

application_id = None

class TestApplyRole(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def clean_up_application(self):
        global application_id
        if application_id is not None:
            # Make a DELETE request to the route to delete the application
            response = self.client.delete(f'/delete_application/{application_id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.clean_up_application()

    def test_apply_role(self):
        global application_id
        # Define your test data
        test_data = {
            "listing_id": 23
        }

        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 140002
            sess['Role'] = 2

        headers = {
            "Content-Type": "application/json"
        }

        # Make a POST request to the route with test data
        response = self.client.post('/apply_role/23', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        # Check the response status code
        self.assertEqual(response.status_code, 201)  # You can adjust this based on your actual implementation

        # Check the response content
        data = json.loads(response.data.decode('utf-8'))
        application_id = data.get("application_id")
        logging.info(f"Application ID in application: {application_id}")

    def test_apply_existing_role(self):
        global application_id
        # Define your test data
        test_data = {
            "listing_id": 2
        }

        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 140002
            sess['Role'] = 2

        headers = {
            "Content-Type": "application/json"
        }

        # Make a POST request to the route with test data
        response = self.client.post('/apply_role/2', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        # Check the response status code
        self.assertEqual(response.status_code, 400)  # You can adjust this based on your actual implementation

        expected_error_message = "You have already applied to this role"
        self.assertIn(expected_error_message, response.get_json()['error'])

    def test_apply_closed_role(self):
        global application_id
        # Define your test data
        test_data = {
            "listing_id": 18  # Replace with a valid listing ID for an open role
        }

        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 140002
            sess['Role'] = 2

        headers = {
            "Content-Type": "application/json"
        }

        # Make a POST request to the route with test data
        response = self.client.post('/apply_role/18', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        # Check the response status code
        self.assertEqual(response.status_code, 411)  # You can adjust this based on your actual implementation

        expected_error_message = "Role listing is closed or not yet open for applications"
        self.assertIn(expected_error_message, response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
