from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from db_config.db import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from db_config.models import *
from sqlalchemy import text


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://g4t4:password@spm-g4t4.cybxkypjkirc.ap-southeast-2.rds.amazonaws.com:3306/sbrp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Testing
@app.route("/roles")
def get_all():
    skills = Staff.query.all()

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

@app.route('/applied_roles_staff/<int:listing_id>', methods=["POST"])
def applied_roles(listing_id):
    try:
        staff_id = 19  # REPLACE with the actual staff_id
        status = "Pending"
        applied_date = datetime.now()

        # Check if the listing exists
        role_listing = Role_Listing.query.filter_by(listing_id=listing_id).first()
        if not role_listing:
            return jsonify({"error": "Role listing not found"}), 404

        # Check if the listing is closed (past the application deadline)
        current_datetime = datetime.now()
        if role_listing.date_open > current_datetime or role_listing.date_close < current_datetime:
            return jsonify({"error": "Role listing is closed or not yet open for applications"}), 400

        # Check if the staff member has already applied to this listing
        existing_application = Application.query.filter_by(listing_id=listing_id, staff_id=staff_id).first()
        if existing_application:
            return jsonify({"error": "You have already applied to this role"}), 400

        # insert application details
        insert_sql = text("""
            INSERT INTO application (listing_id, staff_id, status, applied_date)
            VALUES (:listing_id, :staff_id, :status, :applied_date)
        """)

        params = {
            "listing_id": listing_id,
            "staff_id": staff_id,
            "status": status,
            "applied_date": applied_date,
        }
        
        db.session.execute(insert_sql, params)
        db.session.commit()

        return jsonify({"message": "Application submitted successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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

    