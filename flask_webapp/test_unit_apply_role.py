import unittest
from app import app,db # Import your Flask app and db
from db_config.models import *  # Import your Role_Listing model
import json

from decouple import config

app.config["SQLALCHEMY_DATABASE_URI"] = config("TEST_DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


class TestApplyRole(unittest.TestCase):
    def setUp(self):

        self.app = app.test_client()

        self.role = Role("Finance Manager", "The Finance Manager is the lead finance business partner for the organisation and has responsibilities covering all aspects of financial management, performance management, financial accounting, budgeting, corporate reporting etc. He/she has sound technical as well as management skills and be able to lead a team consisting of finance professionals with varied, in-depth or niche technical knowledge and abilities; consolidating their work and ensuring its quality and accuracy, especially for reporting purposes. The Finance Manager is expected to provide sound financial advice and counsel on working capital, financing or the financial position of the organisation by synthesising internal and external data and studying the economic environment. He often has a key role in implementing best practices in order to identify and manage all financial and business risks and to meet the organisation's desired business and fiscal goals. He is expected to have a firm grasp of economic and business trends and to implement work improvement projects that are geared towards quality, compliance and efficiency in finance.")
        self.manager1 = Staff(171029,"Somchai", "Kong", "Finance", "Singapore", "Somchai.Kong@allinone.com.sg", 3)
        self.staff = Staff(140002,"Susan", "Goh", "Finance", "Singapore", "Susan.Goh@allinone.com.sg", 3)
        self.listing = Role_Listing("Singapore", "Finance", 4, "2023-10-30 00:00:00", "2023-11-31 00:00:00", "Finance Manager", 171029)


    def tearDown(self):
        with app.app_context():
            db.session.query(Role_Listing).filter(Role_Listing.listing_id == 0).delete()
            db.session.query(Staff).filter(Staff.staff_id == 171029).delete()
            db.session.query(Staff).filter(Staff.staff_id == 140002).delete()
            db.session.query(Role).filter(Role.role_name == "Finance Manager").delete()


            db.session.commit()
    
    def test_apply_role(self):
        # Create a test Role_Listing
        with app.app_context():
            db.session.add(self.role)
            db.session.add(self.manager1)
            db.session.add(self.staff)
            db.session.add(self.listing)
            db.session.commit()

        new_data = {
            "listing_id": 0
        }

        response = self.app.post('/apply_role/0', json=new_data)
        print(response)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)  # Check if the response status code is 201 (Created)

        # You can add more assertions to check the response data or database state if needed

if __name__ == '__main__':
    unittest.main()
