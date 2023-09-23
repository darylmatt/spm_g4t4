from db_config.db import db

class Skill(db.Model):

    __tablename__ = 'skill'

    Skill_Name = db.Column(db.String(50),primary_key=True)
    Skill_Desc = db.Column(db.Text(length='long'), nullable=False)

    
    def __init__(self, Skill_Name, Skill_Desc):
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc
    
    def json(self):
        return {"Skill_Name":self.Skill_Name, "Skill_Desc": self.Skill_Desc}
    


        