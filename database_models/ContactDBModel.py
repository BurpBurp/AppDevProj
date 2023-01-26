from sqlalchemy import select, ForeignKey
from database import db
from database_models.UserDBModel import User
import custom_exceptions


class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, default="-")
    message = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default="OPEN")

def get_contact_by_id(id):
    return ContactUs.query.filter_by(id=id).first()

def get_all_contact():
    return ContactUs.query.all()
