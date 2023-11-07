import json
import unittest
from app import app

class TestEditListing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.config['TESTING'] = True
        cls.listing_id = 15
        cls.original_listing_data = None

    def setUp(self):
        self.session_headers = {"Content-Type": "application/json"}
        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 160008
            sess['Role'] = 4 
            sess['Staff_Fname'] = "Sally"
            sess['Staff_Lname'] = "Loh"
            sess['Staff_Name'] = "Sally Loh"
            sess['Dept'] = "HR"
            sess['Country'] = "Singapore"
            sess['Email'] = "Sally.Loh@allinone.com.sg"

        response = self.client.get('/get_listing_by_id/' + str(self.listing_id))
        print('Response data:', response.data)
        if response.status_code == 200:
            fetched_data = response.get_json()['data']
            TestEditListing.original_listing_data = {
                "listing_id": fetched_data['listing_id'],
                "title": fetched_data['role_name'],
                "department": fetched_data['dept'],
                "country": fetched_data['country'],
                "vacancy": fetched_data['num_opening'],
                "manager": fetched_data['reporting_mng'],
                "startDate": fetched_data['date_open'].split("T")[0], 
                "endDate": fetched_data['date_close'].split("T")[0],
            }
        else:
            self.fail(f"Setup failed: Unable to fetch original listing data. Status code: {response.status_code}, Response: {response.data}")
    def tearDown(self):
        if TestEditListing.original_listing_data is not None:
            response = self.client.put(
                '/update/check_listing_exist/' + str(self.listing_id),
                data=json.dumps(TestEditListing.original_listing_data),
                headers=self.session_headers
            )
            self.assertEqual(response.status_code, 201, "Failed to restore the listing to its original state")
            TestEditListing.original_listing_data = None


    def test_edit_listing(self):
        updated_test_data = {
            "listing_id": self.listing_id,
            "title": "Senior Engineer",
            "department": "Engineering",
            "country": "Singapore",
            "vacancy": 1,
            "manager": 150866,
            "startDate": "2024-08-01",
            "endDate": "2024-12-31",
        }

        response = self.client.put(
            '/update/check_listing_exist/' + str(updated_test_data['listing_id']),
            data=json.dumps(updated_test_data),
            headers=self.session_headers
        )
        self.assertEqual(response.status_code, 201)


    def test_edit_listing_invalid_id(self):
        invalid_test_data = {
            "listing_id": 999,
            "title": "Senior Engineer",
            "department": "Engineering",
            "country": "Singapore",
            "vacancy": 1,
            "manager": 150866,
            "startDate": "2024-08-01",
            "endDate": "2024-12-31",
        }

        response = self.client.put(
            '/update/check_listing_exist/' + str(invalid_test_data['listing_id']),
            data=json.dumps(invalid_test_data),
            headers=self.session_headers
        )
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
