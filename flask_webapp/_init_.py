from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from db_config.db import db
from decouple import config
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from db_config.models import *
# from db_config.models import Role_Listing, Application, Country, Department, Skill, Staff, Access_Control, Role, Role_Skill, Staff_Skill
from sqlalchemy import text, asc, desc
from sqlalchemy import and_, or_
import json
import requests
from authorisation import login_required
import traceback


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
