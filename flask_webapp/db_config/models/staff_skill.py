from app import db
from sqlalchemy import ForeignKey
from db_config.models.skill import Skill
from db_config.models.staff import Staff


class Staff_Skill(db.Model):

    __tablename__ = 'staff_skill'

    # Foreign key relationship to access_control table
    staff_id = db.Column(db.Integer, ForeignKey('staff.staff_id'), primary_key = True,)
    skill_name = db.Column(db.Text(length='long'), ForeignKey('skill.skill_name'),primary_key = True)

    # Defining a back reference to access the related access_control record
    staff = db.relationship('Staff', backref='role_skill')
    skill = db.relationship('Skill', backref = 'role_skill')


    # def __init__(self, role_name, skill_name):
    #     self.role_name = role_name
    #     self.skill_name = skill_name
    
    # def json(self):
    #     return {"role_name":self.role_name, "skill_name": self.skill_name}