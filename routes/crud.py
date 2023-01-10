import sqlalchemy.exc
from flask import Blueprint, request, redirect, url_for, abort, jsonify
import flask_login
import http
import time


import secrets
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

import forms.LoginForm
import forms.SignUpForm
import forms.UpdateForm

import custom_exceptions
import helper_functions

from database_models.UserDBModel import get_user_by_username, get_user_by_id, create_user, \
    get_user_by_email, try_login_user, User

import os

# importing db modules
from database import db

# importing mail modules
import mail
from flask_mail import Message

blueprint = Blueprint("crud", __name__, template_folder="templates")

@blueprint.route("/update_role", methods=["POST"])
@flask_login.login_required
@helper_functions.admin_required
def update_role():
    if flask_login.current_user.role < 2:
        return jsonify(success=0, msg="Error! You Do Not Have Permission To Do This")

    form = forms.UpdateForm.UpdateRoleForm()
    if not (target_user := get_user_by_id(form.target_user_id.data)):
        return jsonify(success=0, msg=f"Error! No User With ID Ff \'{form.target_user_id.data}\' Found")

    try:
        target_user.admin_update_role(form.role.data)
        return jsonify(success=1, msg="Successfully Updated User Role!",role=target_user.get_role_str())
    except sqlalchemy.exc.SQLAlchemyError:
        return jsonify(success=0, msg=f"Error! An Internal Server Has Occurred. Please Try Again")

@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.SignUpForm.SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = create_user(form.username.data, generate_password_hash(form.password.data), form.f_name.data, form.l_name.data,
                                   form.email.data)
                helper_functions.flash_success("Account Created Successfully")
                flask_login.login_user(user)
                return redirect(url_for("index.index"))
            except custom_exceptions.UserAlreadyExistsError:
                helper_functions.flash_error("User Already Exists")
                if get_user_by_username(form.username.data):
                    form.username.errors.append("Username Taken")
                if get_user_by_email(form.email.data):
                    form.email.errors.append("Email Taken")
                return helper_functions.helper_render("signup.html", form=form)
        else:
            return helper_functions.helper_render("signup.html", form=form)
    else:
        if helper_functions.check_logged_in():
            helper_functions.flash_success("Already Logged in")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("signup.html", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if user := try_login_user(form.username.data, form.password.data):
                flask_login.login_user(user, remember=form.remember.data)
                helper_functions.flash_success("Logged in Successfully")
                next_url = request.args.get("next")
                return redirect(next_url or url_for("index.index"))
            else:
                helper_functions.flash_error("Username or Password Incorrect")
                return helper_functions.helper_render("login.html", form=form)
        else:
            return helper_functions.helper_render("login.html", form=form)
    else:
        if helper_functions.check_logged_in():
            helper_functions.flash_success("Already Logged in")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("login.html", form=form)


@blueprint.route("/update", methods=["GET", "POST"])
@flask_login.login_required
def update():
    match request.method:
        case "GET":
            if not (target_user := get_user_by_id(request.args.get("id"))):
                helper_functions.flash_error("Invalid user ID")
                return abort(http.HTTPStatus.BAD_REQUEST)

            if not (
                    target_user.id == flask_login.current_user.id or flask_login.current_user.role > target_user.role or flask_login.current_user.role >= 2):
                helper_functions.flash_error("You do not have permission to do that")
                return abort(http.HTTPStatus.FORBIDDEN)

            if flask_login.current_user.id != target_user.id and flask_login.current_user.role < target_user.role:
                helper_functions.flash_error("You do not have permission to do that")
                return abort(403)

            if target_user.id == flask_login.current_user.id:
                update_pass_form = forms.UpdateForm.UpdatePasswordForm(target_user_id=request.args.get("id"))
                update_name_form = forms.UpdateForm.UpdateNameForm(target_user_id=request.args.get("id"))
                update_email_form = forms.UpdateForm.UpdateEmailForm(target_user_id=request.args.get("id"))
                update_delete_form = forms.UpdateForm.UpdateDeleteForm(target_user_id=request.args.get("id"))
                update_image_form = forms.UpdateForm.UpdateImageForm(target_user_id=request.args.get("id"))
                update_name_form.new_f_name.data = target_user.f_name
                update_name_form.new_l_name.data = target_user.l_name
                return helper_functions.render_template("update.html", target_user=target_user,
                                                        update_pass_form=update_pass_form,
                                                        update_email_form=update_email_form,
                                                        update_name_form=update_name_form,
                                                        update_delete_form=update_delete_form,
                                                        update_image_form=update_image_form,
                                                        update_self=True)

            elif flask_login.current_user.role > target_user.role or flask_login.current_user.role >= 2:
                update_pass_form = forms.UpdateForm.UpdatePasswordForm(target_user_id=request.args.get("id"),
                                                                       current_password="PlaceHolder")
                update_name_form = forms.UpdateForm.UpdateNameForm(target_user_id=request.args.get("id"))
                update_image_form = forms.UpdateForm.UpdateImageForm(target_user_id=request.args.get("id"))
                update_email_form = forms.UpdateForm.UpdateEmailForm(target_user_id=request.args.get("id"),
                                                                     current_password="PlaceHolder")
                update_delete_form = forms.UpdateForm.UpdateDeleteForm(target_user_id=request.args.get("id"),
                                                                       current_password="PlaceHolder")

                update_name_form.new_f_name.data = target_user.f_name
                update_name_form.new_l_name.data = target_user.l_name
                update_role_form = forms.UpdateForm.UpdateRoleForm(target_user_id=request.args.get("id"),role=target_user.role)
                return helper_functions.render_template("update.html", target_user=target_user,
                                                        update_pass_form=update_pass_form,
                                                        update_email_form=update_email_form,
                                                        update_name_form=update_name_form,
                                                        update_delete_form=update_delete_form,
                                                        update_image_form=update_image_form,
                                                        update_role_form=update_role_form,
                                                        update_self=False)

        case "POST":
            update_pass_form = forms.UpdateForm.UpdatePasswordForm()
            update_name_form = forms.UpdateForm.UpdateNameForm()
            update_email_form = forms.UpdateForm.UpdateEmailForm()
            update_delete_form = forms.UpdateForm.UpdateDeleteForm()
            update_image_form = forms.UpdateForm.UpdateImageForm()
            if (not (target_user := get_user_by_id(request.form.get("target_user_id")))) and request.method == "POST":
                helper_functions.flash_error("Invalid user ID")
                return abort(http.HTTPStatus.BAD_REQUEST)

            if not (
                    target_user.id == flask_login.current_user.id or flask_login.current_user.role > target_user.role or flask_login.current_user.role == 2):
                helper_functions.flash_error("You do not have permission to do that")
                return abort(http.HTTPStatus.FORBIDDEN)

            if flask_login.current_user.role > target_user.role or (
                    flask_login.current_user.role >= 2 and target_user.id != flask_login.current_user.id):
                is_admin = True
                update_pass_form.current_password.data = target_user.password
                update_email_form.current_password.data = target_user.password
                update_delete_form.current_password.data = target_user.password

            match request.form.get("change_type"):
                case "UpdateName":
                    if update_name_form.validate_on_submit():
                        target_user.update_name(update_name_form.new_f_name.data, update_name_form.new_l_name.data)
                        helper_functions.flash_success("Updated Profile Successfully")
                    else:
                        for field in update_name_form.errors:
                            field = getattr(update_name_form,field)
                            for error in field.errors:
                                helper_functions.flash_error(f"Field: {field.label.text} Error: {error}")

                case "UpdateEmail":
                    if update_email_form.validate_on_submit():
                        try:
                            target_user.update_email(update_email_form.current_password.data,update_email_form.new_email.data,is_admin)
                            helper_functions.flash_success("Changed Email Successfully")
                        except custom_exceptions.WrongPasswordError:
                            helper_functions.flash_error("Wrong Password")
                            return redirect(url_for("crud.update", id=target_user.id))
                        except sqlalchemy.exc.IntegrityError:
                            db.session.rollback()
                            helper_functions.flash_error("Email already in use!")
                            return redirect(url_for("crud.update", id=target_user.id))
                    else:
                        for field in update_email_form.errors:
                            field = getattr(update_email_form,field)
                            for error in field.errors:
                                helper_functions.flash_error(f"Field: {field.label.text} Error: {error}")

                case "UpdatePassword":
                    if not (target_user.id == flask_login.current_user.id or flask_login.current_user.role > target_user.role or flask_login.current_user.role == 2):
                        helper_functions.flash_error("You do not have permission to do that")
                        return redirect(url_for("crud.update", id=target_user.id))
                    else:
                        if update_pass_form.validate_on_submit():
                            try:
                                target_user.admin_update_password(update_pass_form.new_password.data,update_pass_form.confirm_new_password.data)
                                helper_functions.flash_success("Changed Password Successfully")
                            except custom_exceptions.WrongPasswordError:
                                helper_functions.flash_error("Wrong Password")
                                return redirect(url_for("crud.update", id=target_user.id))
                        
                        else:
                            for field in update_pass_form.errors:
                                field = getattr(update_pass_form,field)
                                for error in field.errors:
                                    helper_functions.flash_error(f"Field: {field.label.text} Error: {error}")

                case "UpdateImage":
                    if request.form.get("RemoveImage"):
                        try:
                            if target_user.profile_pic != "default.png":
                                os.remove(f"static/profiles/{target_user.profile_pic}")
                                target_user.profile_pic = "default.png"
                                print("Stuff")
                                helper_functions.flash_success("Changed Profile Picture Successfully")
                                return redirect(url_for("crud.update", id=target_user.id))
                        except IOError:
                            pass
                    else:
                        for field in update_pass_form.errors:
                            field = getattr(update_pass_form,field)
                            for error in field.errors:
                                helper_functions.flash_error(f"Field: {field.label.text} Error: {error}")



                    if update_image_form.validate_on_submit():
                        if update_image_form.image.data:
                            file_name = f"{secrets.token_urlsafe(8)}{os.path.splitext(secure_filename(update_image_form.image.data.filename))[1]}"
                            path = os.path.join("static", "profiles", file_name)
                            update_image_form.image.data.save(path)
                            try:
                                if target_user.profile_pic != "default.png":
                                    os.remove(os.path.join("static", "profiles", target_user.profile_pic))
                            except IOError:
                                pass
                            target_user.profile_pic = file_name
                            helper_functions.flash_success("Changed Profile Picture Successfully")
                    else:
                        helper_functions.flash_error("Image in JPEG, JPG or PNG format is required.")

                case "UpdateDelete":
                    if update_delete_form.validate_on_submit():
                        try:
                            target_user.delete_account(update_delete_form.current_password.data,is_admin)
                        except custom_exceptions.WrongPasswordError:
                            helper_functions.flash_error("Wrong Password")
                            return redirect(url_for("crud.update", id=target_user.id))

                        if target_user.id == flask_login.current_user.id:
                            helper_functions.flash_success("Account Deleted Successfully")
                            return redirect(url_for("index.index"))
                        else:
                            helper_functions.flash_success("Account Deleted Successfully")
                            return redirect(url_for("admin.admin"))
                    else:
                        for field in update_delete_form.errors:
                            field = getattr(update_delete_form,field)
                            for error in field.errors:
                                helper_functions.flash_error(f"Field: {field.label.text} Error: {error}")

            return redirect(url_for("crud.update", id=target_user.id))


@blueprint.route("/request_password_reset",methods=["POST"])
@flask_login.login_required
def request_password_reset():
    token = secrets.token_urlsafe(16)
    flask_login.current_user.reset_token = token
    url = "http://localhost:5000" + url_for("crud.reset_password",token=token)
    print(f"<a href='{url}'>"
          f"{url}"
          f"</a>")
    msg = Message(subject="Reset Password Request",recipients=[flask_login.current_user.email],sender=("KHWares","khwaresappdev@gmail.com"))
    msg.body = f"""You have requested a password reset for your KH Wares account
Click Here: {url} to reset your password
If you did not request this, Ignore this message. No changes will be made."""
    try:
        mail.mail.send(msg)
    except Exception as e:
        print(e)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
    return "Test"


@blueprint.route("/reset_password/<token>",methods=["GET","POST"])
@flask_login.login_required
def reset_password(token):
    if flask_login.current_user.reset_token == token:
        match request.method:
            case "GET":
                user = User.query.filter_by(reset_token=token).first()
                if user:
                    form = forms.UpdateForm.UpdatePasswordForm()
                    return helper_functions.helper_render("reset_password.html",form=form)
                else:
                    helper_functions.flash_error("BAD REQUEST")
                    return redirect(url_for("index.index"))
            case "POST":
                form = forms.UpdateForm.UpdatePasswordForm()
                user = User.query.filter_by(reset_token=token).first()
                if user:
                    if form.validate_on_submit():
                        try:
                            user.update_password(form.current_password.data,form.new_password.data,form.confirm_new_password.data)
                            try:
                                user.reset_token = ""
                                db.session.commit()
                            except sqlalchemy.exc.SQLAlchemyError:
                                pass
                            helper_functions.flash_success("Changed Password Successfully")
                            return redirect(url_for("index.index"))
                        except custom_exceptions.WrongPasswordError:
                            form.current_password.errors.append("Incorrect Password")
                            helper_functions.flash_error("Wrong Password")
                        except custom_exceptions.PasswordNotMatchError:
                            form.new_password.errors.append("Passwords do not match")
                            form.confirm_new_password.errors.append("Passwords do not match")
                            helper_functions.flash_error("Passwords do not match")
                    form = forms.UpdateForm.UpdatePasswordForm()
                    return helper_functions.helper_render("reset_password.html",form=form)
                else:
                    helper_functions.flash_error("BAD REQUEST")
                    return redirect(url_for("index.index"))
    else:
        helper_functions.flash_error("Invalid Token")
        return redirect(url_for("index.index"))






@blueprint.route("/signout", methods=["GET", "POST"])
@flask_login.login_required
def signout():
    flask_login.logout_user()
    helper_functions.flash_primary("Signed Out Successfully")
    return redirect(url_for("index.index"))
