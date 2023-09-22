from app import db

class Skill(db.Model):

    __tablename__ = 'skill'

    skill_name = db.Column(db.String(50),primary_key=True)
    skill_desc = db.Column(db.Text(length='long'), nullable=False)

    
    # def __init__(self, role_name, role_desc):
    #     self.role_name = role_name
    #     self.role_desc = role_desc
    
    # def json(self):
    #     return {"role_name":self.role_name, "role_desc": self.role_desc}