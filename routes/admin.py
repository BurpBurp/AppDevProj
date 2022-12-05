from flask import Blueprint, request, redirect, url_for, session, abort
from sqlalchemy import exc, select, or_, and_
import forms.SignUpForm
from database import db
from database_models.UserDBModel import User, HelperUser, get_user_by_username, get_user_by_id, get_all_users, create_user, get_user_by_email,UserStats
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
        abort(403)
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
        if flask_login.current_user.role == 2:
            form = forms.SignUpForm.AdminCreateAccountForm()
        else:
            form = forms.SignUpForm.EmployeeCreateAccountForm()
        match request.method:
            case "GET":

                return helper_functions.helper_render("signup.html",form=form,admin_create=True)
            case "POST":
                if form.validate_on_submit():
                    try:
                        create_user(form.username.data,form.password.data,form.f_name.data,form.l_name.data,form.email.data,role=form.role.data)
                        helper_functions.flash_success("Account Created Successfully")
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

