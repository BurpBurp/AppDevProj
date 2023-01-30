# Darwin's Stuff
from flask import Blueprint, session, request, redirect, url_for, render_template, jsonify
import pyotp
import flask_login
from forms.TOTPForms import *
from itsdangerous import BadSignature
from serializer import non_timed_serializer, serializer
import custom_exceptions
import sqlalchemy.exc

import helper_functions
from database_models.UserDBModel import *
from database_models.CartDBModel import *

blueprint = Blueprint("totp", __name__, template_folder="templates")


@blueprint.route("/totp/register", methods=["GET", "POST"])
@flask_login.login_required
def register_totp():
    if flask_login.current_user.totp_secret:
        helper_functions.flash_primary("OTP Already Registered")
        return redirect(url_for("crud.update", id=[flask_login.current_user.id]))
    if request.method == "GET":
        secret = pyotp.random_base32()
        print(secret)
        totp = pyotp.TOTP(secret)
        print(totp.now())
        uri = totp.provisioning_uri(name=flask_login.current_user.username, issuer_name="KHWares")
        print(uri)
        form = RegisterTOTP()
        form.secret.data = secret
        return render_template("TOTP/totp_register.html", secret=secret, totp_uri=uri, form=form)

    elif request.method == "POST":
        form = RegisterTOTP()
        secret = form.secret.data
        totp = pyotp.TOTP(secret)
        print(totp.now())
        if form.validate_on_submit():
            if totp.verify(form.otp.data):
                flask_login.current_user.totp_secret = secret
                db.session.commit()
                helper_functions.flash_success("Success! One Time Password Set Up")
                return redirect(url_for("crud.update",id=[flask_login.current_user.id]))
        helper_functions.flash_error("Error! One Time Password Is Invalid")
        form.otp.errors.append("One Time Password Is Invalid")
        form.otp.data = ""
        uri = totp.provisioning_uri(name=flask_login.current_user.username, issuer_name="KHWares")
        return render_template("TOTP/totp_register.html", secret=secret, totp_uri=uri, form=form)

@blueprint.route("/update/remove_totp/<id>", methods=["POST"])
@flask_login.login_required
def ajax_remove_totp(id):
    form = RemoveTOTP()
    target_user = get_user_by_id(id)
    if not target_user:
        return jsonify(success=0, msg=f"Error! User with ID {id} Does Not Exist!")

    if not helper_functions.self_or_admin(target_user):
        return jsonify(success=0, msg="Error! You Do Not Have Permission To Do This")

    is_admin = False
    if helper_functions.is_admin_not_self(target_user):
        form.current_password.data = "PLACEHOLDER"
        is_admin = True

    if form.validate_on_submit():
        try:
            target_user.remove_totp(form.current_password.data,is_admin=is_admin)
        except custom_exceptions.WrongPasswordError:
            form.current_password.errors.append("Incorrect Password")

    if len(form.errors) > 0:
        err_list = {} #key: field_id, value: list of errors
        for field,v in form.data.items():
            error_list = []
            field_obj = getattr(form,field)
            for error in field_obj.errors:
                error_list.append(error)
            err_list[field] = error_list
        print(err_list)
        return jsonify(success=0, msg="Error!", err_list = err_list)
    else:
        fields = list(form.data.keys())
        return jsonify(success=1, msg="Success! Removed One Time Password",fields=fields)





@blueprint.route("/totp/login/<token>",methods=["GET","POST"])
def totp_login(token):
    form = LoginTOTP()
    try:
        user = serializer.loads(token,salt="TOTPLogin",max_age=180)

    except BadSignature:
        helper_functions.flash_error("Error! Invalid TOTP Redirect Token")
        return redirect(url_for("crud.login"))

    if not (user := get_user_by_id(user[0])):
        helper_functions.flash_error("Error! Invalid TOTP Redirect User")
        return redirect(url_for("crud.login"))

    if form.validate_on_submit():
        if request.method == "GET":
            return render_template("TOTP/totp_login.html",form=form, user=user)
        elif request.method == "POST":
            secret = user.totp_secret
            totp = pyotp.TOTP(secret)
            print(totp.now())
            if not (remember := request.args.get("remember")):
                remember = False
            if totp.verify(form.otp.data):
                print("VALID OTP")
                flask_login.login_user(user,remember=remember)
                helper_functions.flash_success(f"Success! Logged in as {user.username}")
                next_url = request.args.get("next")
                print(next_url)
                return redirect(next_url or url_for("index.index"))
            else:
                helper_functions.flash_error("Error! One Time Password Is Invalid")
                form.otp.errors.append("One Time Password Is Invalid")
                form.otp.data = ""

    return render_template("TOTP/totp_login.html",form=form, user=user)
