from flask import Blueprint, request, redirect, url_for, session, abort

from sqlalchemy import exc, select, or_, and_
from database import db
from database_models.UserDBModel import User, HelperUser, get_user_by_username, get_user_by_id,create_user, get_user_by_email, try_login_user
import custom_exceptions
import helper_functions
import forms.SignUpForm
import forms.LoginForm
import forms.UpdateForm
import flask_login

blueprint = Blueprint("crud",__name__,template_folder="templates")

@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.SignUpForm.SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = create_user(form.username.data,form.password.data,form.f_name.data,form.l_name.data,form.email.data)
                helper_functions.flash_success("Account Created Successfully")
                flask_login.login_user(user)
                return redirect(url_for("index.index"))
            except custom_exceptions.UserAlreadyExistsError:
                helper_functions.flash_error("User Already Exists")
                if get_user_by_username(form.username.data):
                    form.username.errors.append("Username Taken")
                if get_user_by_email(form.email.data):
                    form.email.errors.append("Email Taken")
                return helper_functions.helper_render("signup.html",form=form)
        else:
            return helper_functions.helper_render("signup.html",form=form)
    else:
        if helper_functions.check_logged_in():
            helper_functions.flash_success("Already Logged in")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("signup.html",form=form)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if user := try_login_user(form.username.data,form.password.data):
                flask_login.login_user(user,remember=form.remember.data)
                helper_functions.flash_success("Logged in Successfully")
                return redirect(url_for("index.index"))
            else:
                helper_functions.flash_error("Username or Password Incorrect")
                return helper_functions.helper_render("login.html",form=form)
    else:
        if helper_functions.check_logged_in():
            helper_functions.flash_success("Already Logged in")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("login.html",form=form)

@blueprint.route("/update", methods = ["GET","POST"])
@flask_login.login_required
def update():
    match request.method:
        case "GET":
            if not (target_user := get_user_by_id(request.args.get("id"))):
                helper_functions.flash_error("Invalid user ID")
                abort(404)

            print(flask_login.current_user.id != target_user.id)
            print(flask_login.current_user.role < 2)
            if flask_login.current_user.id != target_user.id and flask_login.current_user.role < 2:
                helper_functions.flash_error("You do not have permission to do that")
                abort(403)

            update_pass_form = forms.UpdateForm.UpdatePasswordForm(target_user_id=request.args.get("id"))
            update_email_form = forms.UpdateForm.UpdateEmailForm(target_user_id=request.args.get("id"))
            update_name_form = forms.UpdateForm.UpdateNameForm(target_user_id=request.args.get("id"))
            update_delete_form = forms.UpdateForm.UpdateDeleteForm(target_user_id=request.args.get("id"))

            return helper_functions.render_template("update.html",target_user=target_user,update_pass_form=update_pass_form,
                                                    update_email_form=update_email_form,
                                                    update_name_form=update_name_form,
                                                    update_delete_form=update_delete_form)

        case "POST":
            pass
@blueprint.route("/signout", methods=["GET","POST"])
@flask_login.login_required
def signout():
    flask_login.logout_user()
    helper_functions.flash_primary("Signed Out Successfully")
    return redirect(url_for("index.index"))
