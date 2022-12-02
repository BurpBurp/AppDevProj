from flask import Blueprint, session, redirect,url_for
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database import db
import flask_login
from sqlalchemy import text

blueprint = Blueprint("test", __name__, template_folder="templates")

@blueprint.route("/test")
def test():
    flask_login.login_user(get_user_by_username(session["username"]),remember=True)
    print(flask_login.current_user)
    return redirect(url_for("admin.admin"))
    return "HELLO"
