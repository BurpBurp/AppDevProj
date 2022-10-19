from flask import Blueprint
from database import db
from UserDBModel import User
from sqlalchemy import select

blueprint = Blueprint("test", __name__, template_folder="templates")


def test_add_user():
    user = User(username="Jon", email="Jon@gmail.com", password="Password")
    db.session.add(user)
    db.session.commit()


@blueprint.route("/test")
def test():
    user = db.session.execute(select(User)).scalar()
    if user:
        return f"name: {user.username}, email: {user.email}, password: {user.password}"
    else:
        test_add_user()
        return "Added User"
