import pytest
from app import app, db
from db_config.models import *
import json
from decouple import config

app.config["SQLALCHEMY_DATABASE_URI"] = config("TEST_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_data():
    role = Role(
        "Finance Manager",
        "The Finance Manager is the lead finance business partner for the organisation and has responsibilities covering all aspects of financial management, performance management, financial accounting, budgeting, corporate reporting etc. He/she has sound technical as well as management skills and be able to lead a team consisting of finance professionals with varied, in-depth or niche technical knowledge and abilities; consolidating their work and ensuring its quality and accuracy, especially for reporting purposes. The Finance Manager is expected to provide sound financial advice and counsel on working capital, financing or the financial position of the organisation by synthesising internal and external data and studying the economic environment. He often has a key role in implementing best practices in order to identify and manage all financial and business risks and to meet the organisation's desired business and fiscal goals. He is expected to have a firm grasp of economic and business trends and to implement work improvement projects that are geared towards quality, compliance and efficiency in finance.",
    )
    manager1 = Staff(
        171029,
        "Somchai",
        "Kong",
        "Finance",
        "Singapore",
        "Somchai.Kong@allinone.com.sg",
        3,
    )
    staff = Staff(
        140002,
        "Susan",
        "Goh",
        "Finance",
        "Singapore",
        "Susan.Goh@allinone.com.sg",
        3,
    )
    listing = Role_Listing(
        country="Singapore",
        dept="Finance",
        num_opening=4,
        date_open="2023-10-30 00:00:00",
        date_close="2023-11-30 00:00:00",
        role_name="Finance Manager",
        reporting_mng=171029,
    )

    return role, manager1, staff, listing

def test_apply_role(client, test_data):
    role, manager1, staff, listing = test_data

    with app.app_context():
        db.session.add(role)
        db.session.add(manager1)
        db.session.add(staff)
        db.session.add(listing)
        db.session.commit()

    with client.session_transaction() as sess:
        sess["Staff_ID"] = 140002
        sess["Role"] = 2

    response = client.post("/apply_role/0")
    data = json.loads(response.data)

    assert response.status_code == 201
    # You can add more assertions to check the response data or database state if needed
