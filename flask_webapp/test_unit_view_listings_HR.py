import unittest
from flask import Flask
from app import app, get_all_listings # Import your Flask app and db
from db_config.db import db
from db_config.models import Role_Listing  # Import your Role_Listing model
from test_config import TestConfig  # Import your TestConfig

class TestGetAllListings(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        app.config.from_object(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = app.test_client()

        # Replace the following with your session data
        self.staff_id = 160008  # staff ID for Sally Loh HR Singapore
        self.role = 4  # HR
        self.staff_fname = "Cloudie"
        self.staff_lname = "Heng"
        self.staff_name = self.staff_fname + " " + self.staff_lname
        self.dept = "HR"
        self.country = "Singapore"
        self.email = "Sally.Loh@allinone.com.sg"

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
        self.app_context.pop()
        with self.client:
            # You may need to define a /logout route
            self.client.get('/logout')

    def test_get_all_listings_with_filters(self):
        with self.app.app_context():
            # Now you can call your Flask functions safely within the app context
            search_filters = {
                'status': 'Closed',
                'recency': 'Any time',
                'country': 'Country',
                'department': 'Consultancy',
                'role_search': None,
                'required_skills': None
            }
            response = get_all_listings(search_filters)

            # Assuming you return a JSON response, you can access the JSON data as follows:
            json_data = response[0]
            data = json_data.get_json()
            self.assertEqual(data['code'], 200)
            print(data)

            # # Example of assertions for specific elements within the JSON response
            # listings = data['data']
            # self.assertEqual(len(listings), 1)  # Should have only one listing

            # # Example of assertions for specific properties within the listing
            # first_listing = listings[0]
            # self.assertEqual(first_listing['role_name'], 'Senior Engineer')
            # self.assertEqual(first_listing['date_open'], '10/10/2023')
            # self.assertEqual(first_listing['date_close'], '06/11/2023')
            # self.assertEqual(first_listing['status'], 'Open')
            # Add more assertions based on the structure of your JSON response

    def test_get_all_listings_without_filters(self):
        with self.app.app_context():
            search_filters = {}
            response = get_all_listings(search_filters)

            json_data = response[0]
            data = json_data.get_json()
            self.assertEqual(data['code'], 200)
            print(data)


if __name__ == '__main__':
    unittest.main()
