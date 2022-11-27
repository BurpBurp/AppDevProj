from flask import Blueprint, request, redirect, url_for, session, abort
from sqlalchemy import exc, select, or_, and_
import forms.SignUpForm
from database import db
from database_models.UserDBModel import User, HelperUser, get_user_by_username, get_user_by_id, get_all_users, create_user, get_user_by_email,UserStats
import custom_exceptions
import helper_functions
from forms import SignUpForm

blueprint = Blueprint("admin", __name__, template_folder="templates")


@blueprint.route("/admin", methods=["GET", "POST"])
def admin():
    if user := get_user_by_username(session.get("username")):
        if user.role != "admin":
            helper_functions.flash_error("Permission Denied")
            return redirect("index.index")
        else:
            match request.method:
                case "GET":
                    users = get_all_users()
                    return helper_functions.helper_render("admin.html", user_list=users,stats=UserStats())

                case "POST":
                    pass

    return redirect(url_for("crud.login"))


@blueprint.route("/adminCreateAccount", methods=["GET", "POST"])
def admin_create_account():
    if user := get_user_by_username(session.get("username")):
        if user.role != "admin":
            helper_functions.flash_error("Permission Denied")
            return redirect("index.index")
        else:
            form = forms.SignUpForm.AdminCreateAccountForm()
            match request.method:
                case "GET":
                    return helper_functions.helper_render("signup.html",form=form)
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
                            return helper_functions.helper_render("signup.html",form=form)
                    else:
                        return helper_functions.helper_render("signup.html",form=form)

    return redirect(url_for("crud.login"))
