import http
import flask_login
from flask import Blueprint, request, redirect, url_for, abort
import custom_exceptions
import forms.LoginForm
import secrets
from werkzeug.utils import secure_filename
import forms.SignUpForm
import forms.UpdateForm
from PIL import Image
import helper_functions
from database_models.UserDBModel import get_user_by_username, get_user_by_id, create_user, \
    get_user_by_email, try_login_user
import os

blueprint = Blueprint("crud", __name__, template_folder="templates")


@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.SignUpForm.SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = create_user(form.username.data, form.password.data, form.f_name.data, form.l_name.data,
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
                return redirect(url_for("index.index"))
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
                abort(403)

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

                return helper_functions.render_template("update.html", target_user=target_user,
                                                        update_pass_form=update_pass_form,
                                                        update_email_form=update_email_form,
                                                        update_name_form=update_name_form,
                                                        update_delete_form=update_delete_form,
                                                        update_image_form=update_image_form,
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
                update_pass_form.current_password.data = target_user.password
                update_email_form.current_password.data = target_user.password
                update_delete_form.current_password.data = target_user.password

            match request.form.get("change_type"):
                case "UpdateName":
                    if update_name_form.validate_on_submit():
                        target_user.update_name(update_name_form.new_f_name.data, update_name_form.new_l_name.data)
                        helper_functions.flash_success("Updated Profile Successfully")

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
                            target_user.delete_account(update_delete_form.current_password.data)
                        except custom_exceptions.WrongPasswordError:
                            helper_functions.flash_error("Wrong Password")
                            return redirect(url_for("crud.update", id=target_user.id))
                        if target_user.id == flask_login.current_user.id:
                            helper_functions.flash_success("Account Deleted Successfully")
                            return redirect(url_for("index.index"))
                        else:
                            helper_functions.flash_success("Account Deleted Successfully")
                            return redirect(url_for("admin.admin"))

            return redirect(url_for("crud.update", id=target_user.id))


@blueprint.route("/signout", methods=["GET", "POST"])
@flask_login.login_required
def signout():
    flask_login.logout_user()
    helper_functions.flash_primary("Signed Out Successfully")
    return redirect(url_for("index.index"))
