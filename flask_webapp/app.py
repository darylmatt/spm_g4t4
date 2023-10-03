from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from db_config.db import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from db_config.models import *
from sqlalchemy import text
from sqlalchemy import and_
import json
import requests


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://g4t4:password@spm-g4t4.cybxkypjkirc.ap-southeast-2.rds.amazonaws.com:3306/sbrp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


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
    try:
        # Fetch staff skills using the existing route
        staff_skills_json = requests.get('http://127.0.0.1:5500/skills')
        staff_skills_dict = staff_skills_json.json()
        staff_skills_set = set(staff_skills_dict.get('data', []))

        listings_json = get_all_open_role_listings()
        listings_dict = json.loads(listings_json.data)
        listings = []

        if listings_dict:
            data = listings_dict['data']
            for listing in data:
                date_open = listing['date_open']
                input_open_datetime = datetime.strptime(date_open, "%Y-%m-%dT%H:%M:%S")
                date_close = listing['date_close']
                input_close_datetime = datetime.strptime(date_close, "%Y-%m-%dT%H:%M:%S")

                if input_open_datetime < datetime.now() and input_close_datetime > datetime.now():
                    status = "Open"
                else:
                    status = "Closed"

                manager_json = get_staff_details(listing['reporting_mng'])
                manager_dict = json.loads(manager_json.data)
                manager_name = manager_dict['data']['staff_fname'] + " " + manager_dict['data']['staff_lname']
                manager_dept = manager_dict['data']['dept']

                role_desc_json = get_role_description(listing['role_name'])
                role_desc_dict = json.loads(role_desc_json.data)
                role_desc = role_desc_dict['data']

                skills_required_json = get_skills_required(listing['role_name'])
                skills_required_dict = json.loads(skills_required_json.data)
                skills_required_list = skills_required_dict['data']['skills_required']

                # Calculate matched and unmatched skills for each listing
                matched_skills = set(skills_required_list) & staff_skills_set
                unmatched_skills = set(skills_required_list) - matched_skills

                listingData = {
                    'role_name': listing['role_name'],
                    'date_open': listing['date_open'],
                    'date_close': listing['date_close'],
                    'dept': listing['dept'],
                    'country': listing['country'],
                    'num_opening': listing['num_opening'],
                    'listing_id': listing['listing_id'],
                    'manager_name': manager_name,
                    'manager_dept': manager_dept,
                    'status': status,
                    'role_desc': role_desc,
                    'skills_required_list': skills_required_list,
                    'matched_skills': list(matched_skills),  # Include matched skills
                    'unmatched_skills': list(unmatched_skills)  # Include unmatched skills
                }
                listings.append(listingData)
                num_results = len(listings)

        return render_template("all_listings_staff.html",
                               listings=listings,
                               num_results=num_results
                               )
    except Exception as e:
        # Handle exceptions (e.g., network errors) here
        return str(e), 500  # Return an error response with a 500 status code


@app.route('/get_all_open_role_listings', methods=["GET"])
def get_all_open_role_listings():
    try:
        current_time = datetime.now()
        role_listings = Role_Listing.query.filter(and_(
            Role_Listing.date_open <= current_time,
            Role_Listing.date_close >= current_time,
            Role_Listing.num_opening > 0,
            Role_Listing.date_close >= current_time
        )).all()

        if len(role_listings) > 0:
            return jsonify(
                {
                    "code":200, 
                    "data": [listing.json() for listing in role_listings]
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "There are no role listings"
                }
            ), 404
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500

        

@app.route('/get_all_listings', methods=["GET"])
def get_all_listings():
    try:
        role_listings = Role_Listing.query.all()
        if len(role_listings) > 0:
            return jsonify(
                {
                    "code":200, 
                    "data": [listing.json() for listing in role_listings]
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "There are no role listings"
                }
            ), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500

@app.route('/view_a_listing/<int:listing_id>', methods=['GET'])
def view_a_listing(listing_id):
    try:
        # Check if the listing exists
        listing = Role_Listing.query.filter_by(listing_id=listing_id).first()
        if not listing:
            return jsonify({"error": "Role listing not found"}), 404
        else:
            return jsonify(
                {
                    "code":200, 
                    "data": listing.json()
                }
            )
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500

@app.route('/skills')
def get_skills():
    try:
        staff_id = 20  # REPLACE with the actual staff_id

        # Check if staff exists
        staff = Staff.query.filter_by(staff_id = staff_id).first()
        if not staff:
            return{
                "code":404,
                "message":"Staff does not exist"            
            },404

        # Staff is found, get staff_skills
        staff_details = staff.json()
        staff_skills = staff_details.get('staff_skills', [])

        if (len(staff_skills)== 0):
            return{
                "code":404,
                "message": "You do not possess any skills."
            },404
        
        skills = [skill.get('skill_name') for skill in staff_skills]

        #Get skill description
        desc_list = [Skill.query.filter_by(skill_name=name).first().json().get('skill_desc',[]) for name in skills]

        return{
           "code":200,
           "data":{
                "skill_names":skills,
                "descriptions": desc_list 
           }
          
        },200


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e),"code": 500}), 500


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


@app.route('/login')
def login():
    dynamic_content = "This content is coming from Flask!"
    return render_template("login.html")


def all_listings_HR():
    listings_json = get_all_listings()
    listings_dict = json.loads(listings_json.data)
    listings=[]
    if listings_dict:
        data = listings_dict['data']
        for listing in data:
            date_open = listing['date_open']
            input_open_datetime = datetime.strptime(date_open, "%Y-%m-%dT%H:%M:%S")
            date_close = listing['date_close']
            input_close_datetime = datetime.strptime(date_close, "%Y-%m-%dT%H:%M:%S")

            if (input_open_datetime < datetime.now() and input_close_datetime > datetime.now()):
                status = "Open"
            else:
                status = "Closed"

            manager_json=  get_staff_details(listing['reporting_mng'])
            manager_dict = json.loads(manager_json.data)
            manager_name = manager_dict['data']['staff_fname'] + " " + manager_dict['data']['staff_lname']
            manager_dept = manager_dict['data']['dept']

            role_desc_json = get_role_description(listing['role_name'])
            role_desc_dict = json.loads(role_desc_json.data)
            role_desc = role_desc_dict['data']

            skills_required_json = get_skills_required(listing['role_name'])
            skills_required_dict = json.loads(skills_required_json.data)
            skills_required_list = skills_required_dict['data']['skills_required']

            listingData = {
                'role_name': listing['role_name'],
                'date_open': listing['date_open'],
                'date_close': listing['date_close'],
                'dept': listing['dept'],
                'country': listing['country'],
                'num_opening': listing['num_opening'],
                'listing_id': listing['listing_id'],
                'manager_name': manager_name,
                'manager_dept': manager_dept,
                'status': status,
                'role_desc': role_desc,
                'skills_required_list': skills_required_list
            }
            listings.append(listingData)
            num_results = len(listings)

        return render_template("all_listings_HR.html", 
                           listings=listings,
                           num_results=num_results
                           )
# Define a route to get the listing ID by name
@app.route('/get_listing_id_by_name/<string:role_name>', methods=["GET"])
def get_listing_id_by_name(role_name):
    try:
        # Query the Role_Listing table to find the listing ID by role name
        role_listing = Role_Listing.query.filter(Role_Listing.role_name == role_name).first()
        if role_listing:
            return jsonify({"listingId": role_listing.listing_id}), 200
        else:
            return jsonify({"error": "Role listing not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#apply for a open role
@app.route('/apply_role/<int:listing_id>', methods=["POST"])
def apply_role(listing_id):
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

        return jsonify({"message": "Application submitted successfully", "code": 201}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e),"code": 500}), 500
    
@app.route('/get_staff_details/<int:staff_id>', methods=["GET"])
def get_staff_details(staff_id):
    try:
        staff = Staff.query.filter_by(staff_id=staff_id).first()
        if staff:
            return jsonify(
                {
                    "code":200, 
                    "data": staff.json()
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Staff not found"
                }
            ), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500

@app.route('/get_role_description/<string:role_name>', methods=["GET"])
def get_role_description(role_name):
    try:
        role = Role.query.filter_by(role_name=role_name).first()
        if role:
            return jsonify(
                {
                    "code":200, 
                    "data": role.role_desc
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Role not found"
                }
            ), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500

@app.route('/get_skills_required/<string:role_name>', methods=["GET"])
def get_skills_required(role_name):
    try:
        skills_required = Role_Skill.query.filter_by(role_name=role_name).all()
        if len(skills_required) > 0:
            return jsonify(
                {
                    "code":200, 
                    "data": {   
                                "role_name": role_name,
                                "skills_required":[skill.skill_name for skill in skills_required]
                            } 
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Skills not found"
                }
            ), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500
    

@app.route("/match_skills/<int:listing_id>", methods=["GET"])
def match_skills(listing_id):
    try:
        staff_id = 19  # Placeholder for staff_id (to integrate with login staff_id later on)

        # Check if the role exists
        role = Role_Listing.query.filter_by(listing_id=listing_id).first()
        if not role:
            return jsonify({"error": "Role does not exist.", "code": "404"}), 404

        # Retrieve the role_name using the listing_id
        role_name = (
            db.session.query(Role_Listing.role_name)
            .filter_by(listing_id=listing_id)
            .scalar()
        )

        # Retrieve the role's required skills
        role_skills = set(
            skill[0] for skill in
            db.session.query(Role_Skill.skill_name)
            .filter_by(role_name=role_name)
            .all()
        )

        # Retrieve the staff's skills
        staff_skills = set(
            skill[0] for skill in
            db.session.query(Staff_Skill.skill_name)
            .filter_by(staff_id=staff_id)
            .all()
        )

        # Debugging: Print the retrieved skills
        print("Role Name:", role_name)
        print("Role Skills:", role_skills)
        print("Staff Skills:", staff_skills)

        # Calculate lacking skills
        lacking_skills = role_skills - staff_skills

        # Perform skill matching logic
        matched_skills = staff_skills.intersection(role_skills)

        response_data = {
            "listing_id": listing_id,
            "role_name": role_name,
            "staff_id": staff_id,
            "matched_skills": list(matched_skills),
            "lacking_skills": list(lacking_skills)
        }

        message = None
        if not matched_skills:
            message = "You have no matching skills with this role."
        else:
            message = "You have matching skills with this role!"

        return jsonify({"response_data": response_data, "message": message, "code": 200})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "code": 500}), 500
    
#Get roles, countries and departments for role creation
@app.route("/create/get_data")
def get_dept_and_countries():
    try:
        #Check roles
        role_list = Role.query.all()
        if (len(role_list) == 0):
              return jsonify(
                {
                    "code":404,
                    "message": "No roles in roles list"
                },404
            )

        #Check countries
        country_list = Country.query.all()
        if (len(country_list) == 0):
            return jsonify(
                {
                    "code":404,
                    "message": "Error, no countries are found."
                },404
            )
        
        #Check departments
        department_list = Department.query.all()
        if (len(department_list) == 0):
              return jsonify(
                {
                    "code":404,
                    "message": "Error, no departments are found."
                },404
            )
        
        # skills = [skill.get('skill_name') for skill in staff_skills]
        roles = [r.json().get('role_name') for r in role_list]
        countries  = [c.json() for c in country_list]
        departments = [j.json() for j in department_list]

        #Return both departments and countries
        return jsonify(
            {
                "code": 200,
                "data":{
                    "roles": roles,
                    "countries": countries,
                    "departments":departments
                }
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "code": 500}), 500


# Get reporting manager given a selected department
@app.route('/get_manager/<string:country>/<string:dept>', methods=["GET"])
def get_manager(country,dept):
    try:
        staff_list = Staff.query.filter_by(dept=dept,country=country).all()
        if len(staff_list) > 0:
            manager_list = []
            manager_id = []
            for s in staff_list:
                if (s.json().get('role')) <= 2:
                    fname = s.json().get('staff_fname')
                    lname = s.json().get('staff_lname')
                    manager_list.append(fname+ " " + lname)
                    manager_id.append(s.json().get('staff_id'))

            return jsonify(
                {
                    "code":200, 
                    "data": {
                        "name_list": manager_list,
                        "id_list": manager_id
                }
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "No managers found."
                }
            ), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": str(e)
            }), 500




if __name__ == '__main__':
    app.run(port=5500,debug=True)

    