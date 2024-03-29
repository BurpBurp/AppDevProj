# Darwin's Stuff
from flask import Blueprint, request, redirect, url_for, session, abort
from sqlalchemy import exc, select, or_, and_
import http
import forms.SignUpForm
from database import db
from werkzeug.security import generate_password_hash

from database_models.UserDBModel import User, get_user_by_username, get_user_by_id, get_all_users, create_user, get_user_by_email,UserStats
from database_models.CartDBModel import create_cart

import custom_exceptions
import helper_functions
import flask_login
from forms import SignUpForm

blueprint = Blueprint("admin", __name__, template_folder="templates")


@blueprint.route("/admin", methods=["GET", "POST"])
@flask_login.login_required
def admin():
    if flask_login.current_user.role < 1:
        helper_functions.flash_error("Permission Denied")
        return redirect(url_for('index.index'))
    else:
        match request.method:
            case "GET":
                users = get_all_users()
                return helper_functions.helper_render("admin.html", user_list=users,stats=UserStats())

            case "POST":
                pass



@blueprint.route("/adminCreateAccount", methods=["GET", "POST"])
@flask_login.login_required
def admin_create_account():
    if flask_login.current_user.role < 1:
        helper_functions.flash_error("Permission Denied")
        return redirect(url_for("index.index"))
    else:
        if flask_login.current_user.role >= 2:
            form = forms.SignUpForm.AdminCreateAccountForm()
        else:
            form = forms.SignUpForm.EmployeeCreateAccountForm()
        match request.method:
            case "GET":

                return helper_functions.helper_render("signup.html",form=form,admin_create=True)
            case "POST":
                if form.validate_on_submit():
                    try:
                        user = create_user(form.username.data,generate_password_hash(form.password.data),form.f_name.data,form.l_name.data,form.email.data,role=form.role.data)
                        helper_functions.flash_success("Account Created Successfully")
                        create_cart(user)
                        return redirect(url_for("admin.admin"))
                    except custom_exceptions.UserAlreadyExistsError:
                        helper_functions.flash_error("User Already Exists")
                        if get_user_by_username(form.username.data):
                            form.username.errors.append("Username Taken")
                        if get_user_by_email(form.email.data):
                            form.email.errors.append("Email Taken")
                        return helper_functions.helper_render("signup.html",form=form,title="Create Account",admin_create=True)
                else:
                    return helper_functions.helper_render("signup.html",form=form,title="Create Account",admin_create=True)


@blueprint.route("/admin_delete_user")
@flask_login.login_required
def admin_user_delete():
    if not (target_user := get_user_by_id(request.args.get("id"))):
        helper_functions.flash_error("No user found")
        return abort(http.HTTPStatus.BAD_REQUEST)
    if flask_login.current_user.role < target_user.role and flask_login.current_user.role < 2:
        helper_functions.flash_error("Permission Denied")
        return abort(http.HTTPStatus.FORBIDDEN)

    target_user.admin_delete_user()
    helper_functions.flash_success(f"Success! Deleted User {target_user.username}")

    return redirect(url_for("admin.admin"))
