from flask import Blueprint, request, redirect, url_for, session, abort
from sqlalchemy import exc, select, or_, and_
from database import db
from database_models.UserDBModel import User, HelperUser, get_user_by_username, get_user_by_id, get_all_users
import custom_exceptions
import helper_functions

blueprint = Blueprint("admin",__name__,template_folder="templates")

@blueprint.route("/admin", methods=["GET","POST"])
def admin():
    match request.method:
        case "GET":
            users = get_all_users()
            return helper_functions.helper_render("admin.html", user_list = users)

        case "POST":
            pass



