from app import db
from sqlalchemy import ForeignKey
from db_config.models.role_listing import Role_Listing
from db_config.models.staff import Staff


class Application(db.Model):

    __tablename__ = 'application'

    application_id = db.Column(db.Integer, primary_key= True)
    status = db.Column(db.String(20), nullable = False)
    applied_date = db.Column(db.DateTime, nullable=False)

    # Foreign attributes
    listing_id = db.Column(db.Integer, ForeignKey('role_listing.listing_id'), primary_key = True)
    staff_id = db.Column(db.Integer, ForeignKey('staff.staff_id'), primary_key = True)

    # Backref
    role_listing = db.relationship('Role_Listing', backref='application')
    applicant = db.relationship('Staff', backref = 'application')