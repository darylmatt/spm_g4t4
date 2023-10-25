import json
import unittest
from app import app  # Replace with the actual import path to your Flask app
from flask import session

class TestAllListingsHR(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Replace the following with your session data
        self.staff_id = 160008 # staff ID for Sally Loh HR Singapore
        self.role =  4 # HR
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
        # Clean up session data (log out if necessary)
        with self.client:
            self.client.get('/logout')  # You may need to define a /logout route

    def test_all_listings_HR_with_filters(self):
        # Test with filters
        response = self.client.post('/all_listings_HR', data={
            'status': 'Open',
            'role_name': 'Example Role',
            'recency': 'Past month',
            'country': 'Singapore',
            'department': 'Engineering',
            'required_skills[]': []
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('listings', data)
        self.assertIn('num_results', data)
        self.assertIn('Staff_Name', data)
        self.assertIn('countries', data)
        self.assertIn('departments', data)
        self.assertIn('skills', data)

        # Assertions for the expected listing
        listings = data['listings']
        self.assertEqual(len(listings), 1)  # Should have only one listing
        listing = listings[0]
        self.assertEqual(listing['role_name'], 'Senior Engineer')
        self.assertEqual(listing['date_open'], '10/10/2023')
        self.assertEqual(listing['date_close'], '03/11/2023')
        self.assertEqual(listing['status'], 'Open')
        self.assertEqual(listing['num_opening'], 4)
        self.assertEqual(listing['num_applicants'], 1)
        self.assertEqual(listing['country'], 'Singapore')
        self.assertEqual(listing['dept'], 'Engineering')

        # Add more assertions based on the expected behavior of your route with filters

    def test_all_listings_HR_without_filters(self):
        # Test without filters
        response = self.client.post('/all_listings_HR')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('listings', data)
        self.assertIn('num_results', data)
        self.assertIn('Staff_Name', data)
        self.assertIn('countries', data)
        self.assertIn('departments', data)
        self.assertIn('skills', data)

        # Assertions for the expected listing
        listings = data['listings']
        self.assertEqual(len(listings), 20)


        # Add more assertions based on the expected behavior of your route

if __name__ == '__main__':
    unittest.main()
