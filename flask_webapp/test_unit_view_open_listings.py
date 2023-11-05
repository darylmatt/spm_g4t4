import json
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, get_all_open_role_listings # Import your Flask app and db
from db_config.db import db
from db_config.models import *  # Import your Role_Listing model
from test_config import TestConfig  # Import your TestConfig
from decouple import config

class TestGetOpenListings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = config('TEST_DATABASE_URL')
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()


        # Replace the following with your session data
        self.staff_id = 140002  # staff ID for Sally Loh HR Singapore
        self.role = 2  # HR
        self.staff_fname = "Susan"
        self.staff_lname = "Goh"
        self.staff_name = self.staff_fname + " " + self.staff_lname
        self.dept = "Sales"
        self.country = "Singapore"
        self.email = "Susan.Goh@allinone.com.sg"

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


        self.role1 = Role(
            "Senior Engineer",
            "The Senior Engineer applies advanced engineering principles and techniques to troubleshoot complex engineering problems encountered within the manufacturing facility and provides expert technical advice to guide the installation and maintenance of equipment and systems. He/She is expected to lead the technical cross-collaboration with the Process Development/Manufacturing Science and Technology (PD/MSAT) department in order to identify appropriate biopharmaceuticals manufacturing equipment and optimise their functionalities. The Senior Engineer leads manufacturing equipment and systems innovation projects by guiding feasibility assessments and tests on new technologies. He is expected to review and approve solutions and initiatives to optimise machine availability while managing energy and utility use. He sets parameters for equipment qualification and validation in line with biopharmaceuticals manufacturing regulatory requirements. The Principal/Engineer must ensure compliance with Standard Operating Procedures (SOPs), Health, Safety and Environment (HSE) regulations and Current Good Manufacturing Practices (CGMPs) within his purview. The Engineering and Maintenance Principal/Engineer carries the responsibility of the in-house technical expert. He should possess a deep passion for analysing and resolving multifaceted engineering problems and be able to apply advanced critical and analytical thinking skills to deal with immediate situations. He should have a developmental and amiable approach in his interactions working as part of a team while guiding and mentoring others. He must also be able to communicate engineering concepts in a manner that will be understood by others within and beyond the team.",
        )
        self.role2 = Role(
            "Finance Manager",
            "The Finance Manager is the lead finance business partner for the organisation and has responsibilities covering all aspects of financial management, performance management, financial accounting, budgeting, corporate reporting etc. He/she has sound technical as well as management skills and be able to lead a team consisting of finance professionals with varied, in-depth or niche technical knowledge and abilities; consolidating their work and ensuring its quality and accuracy, especially for reporting purposes. The Finance Manager is expected to provide sound financial advice and counsel on working capital, financing or the financial position of the organisation by synthesising internal and external data and studying the economic environment. He often has a key role in implementing best practices in order to identify and manage all financial and business risks and to meet the organisation's desired business and fiscal goals. He is expected to have a firm grasp of economic and business trends and to implement work improvement projects that are geared towards quality, compliance and efficiency in finance."
        )
        self.role3 = Role(
            "Account Manager",
            "The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily."
        )
        
        self.manager1 = Staff(
            150555,
            "Jaclyn",
            "Wong",
            "Engineering",
            "Singapore",
            "Jaclyn.Wong@allinone.com.sg",
            3
        )
        self.manager2 = Staff(
            171009,
            "Nanda",
            "Kesavan",
            "Finance",
            "Singapore",
            "Nanda.Kesavan@allinone.com.sg",
            3
        )
        self.manager3 = Staff(
        171014,
        "Kumari",
        "Pillai",
        "Finance",
        "Singapore",
        "Kumari.Pillai@allinone.com.sg",
        3,
        )

        self.country1 = Country(
        "Singapore",
        "Singapore"
        ) 

        self.department1 = Department(
        "Engineering"
        )
        self.department2 = Department(
        "Finance"
        )

        self.listing1 = Role_Listing(
        "Singapore",
        "Engineering",
        4,
        "2023-10-10 00:00:00",
        "2023-11-20 00:00:00",
        "Senior Engineer",
        150555,
        )

        db.session.add(self.role1)
        db.session.add(self.role2)
        db.session.add(self.role3)
        db.session.add(self.country1)
        db.session.add(self.department1)
        db.session.add(self.department2)
        db.session.add(self.manager1)
        db.session.add(self.manager2)
        db.session.add(self.manager3)
        db.session.add(self.listing1)
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.query(Role_Listing).delete()
            db.session.query(Staff).delete()
            db.session.query(Role).delete()
            db.session.query(Country).delete()
            db.session.query(Department).delete()

            db.session.commit()

        db.session.remove()
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls):
        # This can be used to do cleanup that applies to the whole test case,
        # not just an individual test method
        pass

    def test_get_open_listings_with_filters(self):
            search_filters = {
                'recency': 'Any time',
                'country': 'Singapore',
                'department': 'Consultancy',
                'role_search': "",
                'required_skills': []
            }
            offset = 0
            limit = 10
            response = get_all_open_role_listings(search_filters, offset, limit)

            # Assuming you return a JSON response, you can access the JSON data as follows:
            data = response[0].get_json()
            self.assertEqual(data['code'], 404)

    def test_get_open_listings_without_filters(self):
        with app.app_context():
            search_filters = {}
            offset = 0
            limit = 10
            response = get_all_open_role_listings(search_filters, offset, limit)

            data = response[0].get_json()
            self.assertEqual(data['code'], 200)
            print(data)

            listings = data['data']
            self.assertEqual(len(listings), 1)  # Should have only one listing

            first_listing = listings[0]
            self.assertEqual(first_listing['listing_id'], 0)
            self.assertEqual(first_listing['num_opening'], 4)
            self.assertEqual(first_listing['reporting_mng'], 150555)
            self.assertEqual(first_listing['role_name'], 'Senior Engineer')
            self.assertEqual(first_listing['date_open'], '2023-10-10T00:00:00')
            self.assertEqual(first_listing['date_close'], '2023-11-20T00:00:00')
            self.assertEqual(first_listing['country'], 'Singapore')
            self.assertEqual(first_listing['dept'], 'Engineering')



if __name__ == '__main__':
    unittest.main()
