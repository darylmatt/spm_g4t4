from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from db_config.models import Skill
from db_config.db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/g4_sbrp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/test/<string:skill_name>', methods=['POST'])
def create_skill(skill_name):
    data = request.get_json()
    skill = Skill(Skill_Name=skill_name, Skill_Desc=data['skill_desc'])
   
    try:
        skill = Skill(Skill_Name=skill_name, Skill_Desc=data['skill_desc'])
        db.session.add(skill)
        db.session.commit()
        return "Success"
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating skill: {str(e)}")  # Print the error message for debugging
        return jsonify({
            "code": 500,
            "data": {
                "Skill_Name": skill_name,
            },
            "message": f"An error occurred creating the skill: {str(e)}"
        }), 500

    
   

@app.route('/design_reference')
def design_reference():
    dynamic_content = "This content is coming from Flask!"
    #Keep design reference untouched
    return render_template("design_reference.html")

@app.route('/index')
def index():
    #This will be our base, customised template that pages will follow
    dynamic_content = "This content is coming from Flask!"
    return render_template("index.html")

@app.route('/listings')
def listings():
    dynamic_content = "This content is coming from Flask!"
    return render_template("listings.html")

@app.route('/applied_roles')
def applied_roles():
    dynamic_content = "This content is coming from Flask!"
    return render_template("applied_roles.html")


@app.route('/role_creation')
def role_creation():
    dynamic_content = "This content is coming from Flask!"
    return render_template("role_creation.html")

if __name__ == '__main__':
    app.run(port=5500,debug=True)

    