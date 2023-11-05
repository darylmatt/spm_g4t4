import json
import unittest
from app import app
import logging

class TestEditListing(unittest.TestCase):
    def setUp(self):
        global listing_id
        listing_id = 15
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Replace the following with your session data
        self.staff_id = 160008  # staff ID for Sally Loh HR Singapore
        self.role = 4  # HR
        self.staff_fname = "Sally"
        self.staff_lname = "Loh"
        self.staff_name = self.staff_fname + " " + self.staff_lname
        self.dept = "HR"
        self.country = "Singapore"
        self.email = "Sally.Loh@allinone.com.sg"

        response = self.client.get('/get_listing_by_id/'+str(listing_id))

        global test_initial_json
        test_initial_json = json.loads(response.data)['data']
        # logging.info(f"Application ID in application: {test_initial_json}")


        with self.client:
            with self.client.session_transaction() as sess:
                sess['Staff_ID'] = self.staff_id
                sess['Role'] = self.role
                sess['Staff_Fname'] = self.staff_fname
                sess['Staff_Lname'] = self.staff_lname
                sess['Staff_Name'] = self.staff_name
                sess['Dept'] = self.dept
                sess['Country'] = self.country
                sess['Email'] = self.email

    def tearDown(self):
        # Clean up session data (log out if necessary)
        test_data = {
            "listing_id": 15,
            "title" : "Junior Engineer",
            "department" : "Engineering",
            "country" : "Singapore",
            "vacancy" : 2,
            "manager" : 150866,
            "startDate" : "2024-07-04",
            "endDate" : "2024-11-06",
        }
        headers = {"Content-Type": "application/json"}

        # Test with filters
        response = self.client.put('/update/check_listing_exist/'+str(listing_id), data=json.dumps(test_initial_json),headers=headers, follow_redirects=True)

        with self.client:
            # You may need to define a /logout route
            self.client.get('/logout')

    def test_edit_listing(self):
        # Define your test data
        test_data = {
            "listing_id": 15,
            "title" : "Junior Engineer",
            "department" : "Engineering",
            "country" : "Singapore",
            "vacancy" : 3,
            "manager" : 150866,
            "startDate" : "2024-07-04",
            "endDate" : "2024-11-06",
        }
        headers = {"Content-Type": "application/json"}

        # Test with filters
        response = self.client.put('/update/check_listing_exist/'+str(test_data['listing_id']), data=json.dumps(test_data),headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 201)
        # Add more assertions based on the structure of your HTML template

    def test_edit_listing_invalid_id(self):
        # Define your test data
        test_data = {
            "listing_id": 5,
            "title" : "Junior Engineer",
            "department" : "Engineering",
            "country" : "Singapore",
            "vacancy" : 3,
            "manager" : 150866,
            "startDate" : "2024-07-04",
            "endDate" : "2024-11-06",
        }
        headers = {"Content-Type": "application/json"}

        # Test with filters
        response = self.client.put('/update/check_listing_exist/'+str(test_data['listing_id']), data=json.dumps(test_data),headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
