import json
import unittest
from app import app
from bs4 import BeautifulSoup

class TestAllListingsHR(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        self.staff_id = 160008 
        self.role = 4
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
        with self.client:
            self.client.get('/logout')

    def test_all_listings_HR_with_filters(self):
        response = self.client.post('/all_listings_HR/1', data={
            'status': 'Open',
            'recency': 'Past month',
            'country': 'Singapore',
            'department': 'Engineering',
        })

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')

        listing_divs = soup.find_all('div', class_='listing')
        self.assertEqual(len(listing_divs), 1)

        role_name = listing_divs[0].find('h5', class_='card-title').text
        date_open = listing_divs[0].find('div', class_='date-open').text
        date_close = listing_divs[0].find('div', class_='date-close').text
        status = listing_divs[0].find('div', class_='status').text

        self.assertEqual(role_name, 'Junior Engineer')
        self.assertEqual(date_open, '05/11/2023')
        self.assertEqual(date_close, '10/11/2024')
        self.assertEqual(status, 'Open')

    def test_all_listings_HR_without_filters(self):
        response = self.client.post('/all_listings_HR/1', data={
        })

        self.assertEqual(response.status_code, 200)
        print(response.data)

if __name__ == '__main__':
    unittest.main()
