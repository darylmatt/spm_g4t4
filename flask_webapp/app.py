from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from db_config.db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from db_config.models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://g4t4:password@spm-g4t4.cybxkypjkirc.ap-southeast-2.rds.amazonaws.com:3306/sbrp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Testing
@app.route("/skills")
def get_all():
    skills = Skill.query.all()

    if len(skills):
        return jsonify(
            {
                "code":200, 
                "data": [skill.json() for skill in skills]
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills"
        }
    ), 404



@app.route('/design_reference')
def design_reference():
    dynamic_content = "This content is coming from Flask!"
    #Keep design reference untouched
    return render_template("design_reference.html")

@app.route('/staff_profile')
def staff_profile():
    return render_template("staff_profile.html")

@app.route('/all_listings_staff')
def index():
    #This will be our base, customised template that pages will follow
    dynamic_content = "This content is coming from Flask!"
    return render_template("all_listings_staff.html")

@app.route('/listings')
def listings():
    dynamic_content = "This content is coming from Flask!"
    return render_template("listings.html")

@app.route('/applied_roles_staff')
def applied_roles():
    dynamic_content = "This content is coming from Flask!"
    return render_template("applied_roles.html")

@app.route('/role_creation')
def role_creation():
    dynamic_content = "This content is coming from Flask!"
    return render_template("role_creation.html")

@app.route('/all_listings_HR')
def all_listings_HR():
    dynamic_content = "This content is coming from Flask!"
    return render_template("all_listings_HR.html")

if __name__ == '__main__':
    app.run(port=5500,debug=True)

    