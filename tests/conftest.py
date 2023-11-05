import pytest
from flask_webapp.app_factory import create_app
from flask_webapp.db_config.db import db

@pytest.fixture
def app():
    app = create_app("TEST_DATABASE_URL")

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
