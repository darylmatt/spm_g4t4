import json
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, get_all_listings # Import your Flask app and db
from db_config.db import db
from db_config.models import *  # Import your Role_Listing model
from test_config import TestConfig  # Import your TestConfig
from decouple import config

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://g4t4:password@spm-g4t4-sbrp.cybxkypjkirc.ap-southeast-2.rds.amazonaws.com:3306/sbrp_test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class TestGetAllListings(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
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
        with app.app_context():
            # Now you can call your Flask functions safely within the app context
            search_filters = {
                'status': 'Open',
                'recency': 'Any time',
                'country': 'Singapore',
                'department': 'Engineering',
                'role_search': "",
                'required_skills': []
            }
            offset = 0
            limit = 10
            response = get_all_listings(search_filters, offset, limit)

            # Assuming you return a JSON response, you can access the JSON data as follows:
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            print(data)

            listings = data[0]['data']
            self.assertEqual(len(listings), 1)  # Should have only one listing

            first_listing = listings[0]
            self.assertEqual(first_listing['listing_id'], 2)
            self.assertEqual(first_listing['num_opening'], 2)
            self.assertEqual(first_listing['reporting_mng'], 151408)
            self.assertEqual(first_listing['role_name'], 'Senior Engineer')
            self.assertEqual(first_listing['date_open'], '2023-10-10T00:00:00')
            self.assertEqual(first_listing['date_close'], '2023-11-06T00:00:00')
            self.assertEqual(first_listing['country'], 'Singapore')
            self.assertEqual(first_listing['dept'], 'Engineering')

    def test_get_all_listings_without_filters(self):
        with app.app_context():
            search_filters = {}
            offset = 0
            limit = 10
            response = get_all_listings(search_filters, offset, limit)

            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
