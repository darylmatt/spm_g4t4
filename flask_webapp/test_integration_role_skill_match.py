import json
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, get_all_open_role_listings, get_skills_required
from db_config.db import db
from db_config.models import * 
from test_config import TestConfig
from decouple import config
import math



class TestViewRoleSkillMatch(unittest.TestCase):
     def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        self.app_context = app.app_context()
        self.request_context = app.test_request_context()
        self.app_context.push()

        self.staff_id = 140002 
        self.role = 2  
        self.staff_fname = "Susan"
        self.staff_lname = "Goh"
        self.staff_name = self.staff_fname + " " + self.staff_lname
        self.dept = "Sales"
        self.country = "Singapore"
        self.email = "Susan.Goh@allinone.com.sg"

        with self.client:
            with self.client.session_transaction() as sess:
                sess['Staff_ID'] = self.staff_id
                sess['Role'] = self.role
                sess['Staff_Fname'] = self.staff_fname
                sess['Staff_Lname'] = self.staff_lname
                sess['Staff_Name'] = self.staff_name
                sess['Dept'] = self.dept
                sess['Country'] = self.country
                sess['Email'] = self.email

     def test_integration_role_skill_match(self):
        with app.test_request_context('/skills'):
            with self.client:
                staff_skills_json = self.client.get('/skills').get_json()
                staff_skills_dict = staff_skills_json.get('data', {})
                skill_names = staff_skills_dict.get('skill_names', [])
                descriptions = staff_skills_dict.get('descriptions', [])
                paired_skills = list(zip(skill_names, descriptions))
        
                role_search = ""
                recency = "Any time"
                country = "Country"
                department = "Department"
                required_skills = []

                '''
                unmatched_skills_results = [["Accounting Standards", "Audit Compliance", "Audit Frameworks", "Business Acumen", "Collaboration", "Communication", "Data Analytics", "Finance Business Partnering", "Financial Management", "Financial Planning", "Financial Reporting", "Financial Statements Analysis", "Project Management", "Regulatory Compliance", "Regulatory Risk Assessment", "Stakeholder Management", "Tax Implications"], 
                                            ["Audit Compliance", "Communication", "Data Analytics", "Finance Business Partnering", "Financial Management", "Financial Planning", "Financial Reporting", "Regulatory Strategy", "Stakeholder Management", "Tax Implications"],
                                            ["Audit Compliance", "Communication", "Data Analytics", "Finance Business Partnering", "Financial Management", "Financial Planning", "Financial Reporting", "Regulatory Strategy", "Stakeholder Management", "Tax Implications"],
                                            ["Automated Equipment and Control Configuration", "Collaboration", "Communication", "Problem Solving"]
                                            ]
                                            '''
                
                expected_skill_match_scores = [ 9, 0, 11, 17, 0 ]
                expected_feedback = ["You are not recommended for this role",
                                     "You are not recommended for this role",
                                     "You are not recommended for this role",
                                     "You are not recommended for this role",
                                     "You are not recommended for this role"]


                offset = 0
                limit = 5
                search_params = {"role_search": role_search, "recency": recency, "country": country, "department": department, "required_skills": required_skills}
                listings_json = get_all_open_role_listings(search_params, offset=offset, limit=5)
                listings_dict = listings_json[0].get_json()

                data = listings_dict['data']
                for listing in data:
                    listing_index = data.index(listing)
                    skills_required_json = get_skills_required(listing['role_name'])

                    skills_required_dict = json.loads(skills_required_json.data)
                    skills_required_list = skills_required_dict['data']['skills_required']
                    staff_skills_list = staff_skills_dict['skill_names']

                    matched_skills = list(set(staff_skills_list) & set(skills_required_list))
                    matched_skills.sort()

                    unmatched_skills = list(set(skills_required_list) - set(matched_skills))
                    unmatched_skills.sort()

                    skill_match_score = math.ceil((len(matched_skills) / (len(unmatched_skills) + len(matched_skills)) ) * 100)
                    expected_skill_match_score = expected_skill_match_scores[listing_index]
                    self.assertEqual(skill_match_score, expected_skill_match_score)


                    if skill_match_score < 20:
                        feedback = "You are not recommended for this role"
                    elif skill_match_score >= 40:
                        feedback = "You are recommended for this role"
                    else:
                        feedback = "You are highly recommended for this role"

                    expected_listing_feedback = expected_feedback[listing_index]
                    self.assertEqual(feedback, expected_listing_feedback)

if __name__ == '__main__':
    unittest.main()

