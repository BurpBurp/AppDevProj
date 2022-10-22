from flask import Blueprint, session
from database_models.UserDBModel import *

blueprint = Blueprint("test", __name__, template_folder="templates")


def test_add_user():
    user = User(username="Jon", email="Jon@gmail.com", password="Password")
    db.session.add(user)
    db.session.commit()


@blueprint.route("/test")
def test():
    try:
        user = HelperUser(get_user_by_username(session["username"]))
        user.change_username("admin","123")
        session["username"] = "admin"
        return session["username"]
    except Exception as e:
        print(e)
        return str(e)
