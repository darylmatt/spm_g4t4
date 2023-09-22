from app import db

class Role(db.Model):

    __tablename__ = 'role'

    role_name = db.Column(db.String(20),primary_key=True)
    role_desc = db.Column(db.String(100000), nullable=False)

    
    def __init__(self, role_name, role_desc):
        self.role_name = role_name
        self.role_desc = role_desc
    
    def json(self):
        return {"role_name":self.role_name, "role_desc": self.role_desc}