from app import db
from sqlalchemy import ForeignKey
from db_config.models.staff import Staff
from db_config.models.role import Role
from db_config.models.application import Application


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
    applications = db.relationship('Application', backref='role_listing')