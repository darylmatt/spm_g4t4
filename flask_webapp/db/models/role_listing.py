from app import db
from sqlalchemy import ForeignKey
from staff import Staff
from role import Role

class Role_Listing(db.Model):

    __tablename__ = 'role_listing'

    listing_id = db.Column(db.Integer, primary_key=True)
    country= db.Column(db.String(50),nullable=False)
    dept= db.Column(db.String(50),nullable=False)
    num_opening= db.Column(db.Integer,nullable=False)
    date_open= db.Column(db.DateTime,nullable=False)
    date_close= db.Column(db.DateTime,nullable=False)

    # Foreign key relationship to role table
    role_name = db.Column(db.String(20), ForeignKey('role.role_name'), nullable=False)
    reporting_mng = db.Column(db.Integer, ForeignKey('staff.staff_id'), nullable=False)

    # backref
    role = db.relationship('Role_Listing', backref='role_listings')
    staff = db.relationship('Role_Listing', backref='role_listings')

    
    # def __init__(self, id, staff_fname, staff_lname, dept, country, email, role):
    #     self.id = id
    #     self.staff_fname = staff_fname
    #     self.staff_lname = staff_lname
    #     self.dept = dept
    #     self.country = country
    #     self.email = email
    #     self.role = role
    
    # def json(self):
    #     return {"id":self.id, "staff_fname": self.fname, "staff_lname": self.lname, "department": self.dept, "country": self.country, "email": self.email, "role": self.role }
