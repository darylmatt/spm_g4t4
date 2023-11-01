import unittest
from app import app, db  # Import your Flask app and db
from db_config.models import *  # Import your Role_Listing model
import json

from decouple import config


class TestViewRoleApplicant(unittest.TestCase):
    def setUp(self):

        app.config["TESTING"] = True
        self.client = app.test_client()
        app.config["SQLALCHEMY_DATABASE_URI"] = config("TEST_DATABASE_URL")

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(app)

        self.manager = Staff(
            staff_id=171029,
            staff_fname="Somchai",
            staff_lname="Kong",
            dept="Finance",
            country="Singapore",
            email="Somchai.Kong@allinone.com.sg",
            role="3",
        )

        self.role = Role(
            role_name='Finance Manager',
            role_desc="The Finance Manager is the lead finance business partner for the organisation and has responsibilities covering all aspects of financial management, performance management, financial accounting, budgeting, corporate reporting etc. He/she has sound technical as well as management skills and be able to lead a team consisting of finance professionals with varied, in-depth or niche technical knowledge and abilities; consolidating their work and ensuring its quality and accuracy, especially for reporting purposes. The Finance Manager is expected to provide sound financial advice and counsel on working capital, financing or the financial position of the organisation by synthesising internal and external data and studying the economic environment. He often has a key role in implementing best practices in order to identify and manage all financial and business risks and to meet the organisation's desired business and fiscal goals. He is expected to have a firm grasp of economic and business trends and to implement work improvement projects that are geared towards quality, compliance and efficiency in finance.",
        )

        self.role_skills = []
        skills = ['Accounting and Tax Systems', 'Accounting Standards', 'Audit Compliance', 'Audit Frameworks', 'Business Acumen', 'Collaboration', 'Communication', 'Data Analytics', 'Finance Business Partnering', 'Financial Management', 'Financial Planning', 'Financial Reporting', 'Financial Statements Analysis', 'Professional and Business Ethics', 'Project Management', 'Regulatory Compliance', 'Regulatory Risk Assessment', 'Stakeholder Management', 'Tax Implications']

        for skill in skills:
            role_skill = Role_Skill(
                role_name='Finance Manager',
                skill_name=skill
            )
            self.role_skills.append(role_skill)


        self.role_listing = Role_Listing(
            role_name='Finance Manager',
            country='Singapore',
            dept='Finance',
            num_opening=2,
            date_open='2023-10-10 00:00:00',
            date_close='2023-11-30 00:00:00',
            reporting_mng=171029,
        )
        
        self.staff = Staff(
            staff_id=140002,
            staff_fname="Susan",
            staff_lname="Goh",
            dept="Finance",
            country="Singapore",
            email="Susan.Goh@allinone.com.sg",
            role=2,
        )

    def tearDown(self):
        with app.app_context():
            db.session.query(Role_Listing).delete()
            db.session.query(Role_Skill).delete()
            db.session.query(Staff_Skill).delete()
            db.session.query(Staff).delete()
            db.session.query(Skill).delete()
            db.session.query(Role).delete()
            db.session.commit()

    def test_apply_role(self):
        # Create a test Role_Listing
        with app.app_context():
            db.session.add(self.manager)
            db.session.add(self.role)
            db.session.add(self.role_listing)
            db.session.add(self.staff)
            for role_skill in self.role_skills:  # Add each role_skill to the session
                db.session.add(role_skill)
            for skill_data in self.skills_data:
                skill = Skill(**skill_data)
                db.session.add(skill)
            for staff_skill_data in self.staff_skills_data:
                staff_skill = Staff_Skill(**staff_skill_data)
                db.session.add(staff_skill)
            db.session.commit()

        with self.client.session_transaction() as sess:
            sess["Staff_ID"] = 140002
            sess["Role"] = 2

        new_data = {"listing_id": 0}

        response = self.client.post("/get_applications_by_listing/0")
        print(response)
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 201
        )  # Check if the response status code is 201 (Created)

        # You can add more assertions to check the response data or database state if needed


if __name__ == "__main__":
    unittest.main()
