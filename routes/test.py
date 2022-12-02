from flask import Blueprint, session
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database import db
from sqlalchemy import text

blueprint = Blueprint("test", __name__, template_folder="templates")

@blueprint.route("/test")
def test():
    a = db.session.execute(text("SELECT data from sessions")).all()
    print(a)
    return "STUFF"
