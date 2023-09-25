from app import db
from db_config.models.staff import Staff

class Access_Control(db.Model):

    __tablename__ = 'access_control'

    access_id = db.Column(db.Integer,primary_key=True)
    access_control_name = db.Column(db.String(20), nullable=False)
    # One to many relationship with staff
    staffs = db.relationship('Staff', backref='access_control')

    
    def __init__(self, id, access_control_name):
        self.id = id
        self.access_control_name = access_control_name
    
    def json(self):
        return {"id":self.access_id, "access_control_name": self.access_control_name}