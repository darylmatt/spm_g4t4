from app import db
from sqlalchemy import ForeignKey
from access_control import Access_Control

class Staff(db.Model):

    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname= db.Column(db.String(50),nullable=False)
    staff_lname= db.Column(db.String(50),nullable=False)
    dept= db.Column(db.String(50), nullable=False)
    country= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)

    # Foreign key relationship to access_control table
    role = db.Column(db.Integer, ForeignKey('access_control.id'), nullable=False)

    # Defining a back reference to access the related access_control record
    role = db.relationship('Access_Control', backref='staff')
    
    def __init__(self, id, staff_fname, staff_lname, dept, country, email, role):
        self.staff_id = id
        self.staff_fname = staff_fname
        self.staff_lname = staff_lname
        self.dept = dept
        self.country = country
        self.email = email
        self.role = role
    
    def json(self):
        return {"id":self.staff_id, "staff_fname": self.staff_fname, "staff_lname": self.staff_lname, "department": self.dept, "country": self.country, "email": self.email, "role": self.role }
