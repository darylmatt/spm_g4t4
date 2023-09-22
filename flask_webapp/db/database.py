from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_db():
    app = Flask(__name__)

    # Load database configurations from config.py or elsewhere
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@42.61.167.85:3306/spm_g4t4'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    print("Success")

    return db
