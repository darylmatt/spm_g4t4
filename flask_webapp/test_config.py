import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig:
    TESTING = os.getenv('TESTING', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')