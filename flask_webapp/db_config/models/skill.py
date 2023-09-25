from db_config.db import db

class Skill(db.Model):

    __tablename__ = 'skill'

    skill_name = db.Column(db.String(50),primary_key=True)
    skill_desc = db.Column(db.Text(length='long'), nullable=False)

    role_skills = db.relationship('Role_Skill', backref='skill')
    staff_skills = db.relationship('Staff_Skill', backref='skill')

    
    def __init__(self, skill_name, skill_desc):
        self.skill_name = skill_name
        self.skill_desc = skill_desc
    
    def json(self):
        return {"Skill_Name":self.skill_name, "Skill_Desc": self.skill_desc}
    
