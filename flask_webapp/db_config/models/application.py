from app import db
from sqlalchemy import ForeignKey

class Application(db.Model):

    __tablename__ = 'application'

    application_id = db.Column(db.Integer, primary_key= True)
    status = db.Column(db.String(20), nullable = False)
    applied_date = db.Column(db.DateTime, nullable=False)

    # Foreign attributes
    listing_id = db.Column(db.Integer, ForeignKey('role_listing.listing_id'), primary_key = True)
    staff_id = db.Column(db.Integer, ForeignKey('staff.staff_id'), primary_key = True)

    