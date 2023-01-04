from flask import Blueprint, session
from database_models.UserDBModel import *
from database_models.CartDBModel import *

blueprint = Blueprint("test", __name__, template_folder="templates")

@blueprint.route("/test")
def test():
    pass
