import json
from app import app
from db_config.db import db
from db_config.models import Role, Staff, Role_Listing
import os
from decouple import config
import pytest
from flask_webapp.app_factory import create_app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    test_database_url = config("TEST_DATABASE_URL")
    print("Test Database URL:", test_database_url)

    app.config["SQLALCHEMY_DATABASE_URI"] = test_database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_create_role(client):
    manager1 = Staff(
        180012,
        "Ji",
        "Han",
        "Consultancy",
        "Singapore",
        "Ji.Han@allinone.com.sg",
        3,
    )

    role1 = Role(
        "Consultant",
        "The Consultant is responsible for providing Sales technical expertise to the sales team and clients during the sales process..."
    )

    with client.session_transaction() as sess:
        sess["Staff_ID"] = 16008
        sess["Role"] = 4

    new_data = {
        "title": "Consultant",
        "department": "Consultancy",
        "country": "Singapore",
        "startDate": "2023-11-08",
        "endDate": "2023-11-15",
        "manager": 180012,
        "vacancy": 4,
    }

    response = client.post("/create/check_listing_exist", json=new_data)

    assert response.status_code == 201


def test_create_overlap_existing(client):
    manager1 = Staff(
        180012,
        "Ji",
        "Han",
        "Consultancy",
        "Singapore",
        "Ji.Han@allinone.com.sg",
        3,
    )

    role1 = Role(
        "Consultant",
        "The Consultant is responsible for providing Sales technical expertise to the sales team and clients during the sales process..."
    )

    existing_listing1 = Role_Listing(
        country="Singapore",
        dept="Consultancy",
        num_opening=4,
        date_open="2023-11-4 00:00:00",
        date_close="2023-11-18 00:00:00",
        role_name="Consultant",
        reporting_mng=180012,
    )

    with client.session_transaction() as sess:
        sess["Staff_ID"] = 16008
        sess["Role"] = 4

    new_data = {
        "title": "Consultant",
        "department": "Consultancy",
        "country": "Singapore",
        "startDate": "2023-11-08",
        "endDate": "2023-11-15",
        "manager": 180012,
        "vacancy": 2,
    }

    response = client.post("/create/check_listing_exist", json=new_data)

    assert response.status_code == 400
