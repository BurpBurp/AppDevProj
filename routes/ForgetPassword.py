# Darwin's Stuff
import sqlalchemy.exc
from flask import Blueprint, session, url_for, redirect, request, abort, render_template
import flask_login
import http
from database import db
from sqlalchemy import exc
import custom_exceptions

import helper_functions
from database_models.UserDBModel import get_user_by_email, User
from forms.ForgotPasswordForm import ForgotPasswordForm, ForgotPasswordResetForm



# Token Imports
from serializer import serializer
from itsdangerous import SignatureExpired, BadSignature
import secrets

# Mail Imports
from flask_mail import Message
import mail

blueprint = Blueprint("forgot_password", __name__, template_folder="templates")

@blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == "GET":
        return render_template("forgot_password/forgot_password.html", form=form, title="Forgot Password")
    elif request.method == "POST":
        if form.validate_on_submit():
            user = get_user_by_email(form.email.data.lower())
            if not user:
                form.email.errors.append("User with this email does not exist")
                helper_functions.flash_error("Invalid Email")
                return render_template("forgot_password/forgot_password.html", form=form, title="Forgot Password")

            token = secrets.token_urlsafe(16)
            user.reset_token = token
            serialized = serializer.dumps({"id": user.id, "token": token}, salt="PasswordReset")
            url = url_for("forgot_password.forgot_password_reset", token=serialized, _external=True)
            print(f"<a href='{url}'>"
                  f"{url}"
                  f"</a>")
            msg = Message(subject="Reset Password Request", recipients=[user.email],
                          sender=("KHWares", "khwaresappdev@gmail.com"))
            msg.body = f"""You have requested a password reset for your KH Wares account
        Click Here: {url} to reset your password. This link will expire in 10 minutes.
        If you did not request this, Ignore this message. No changes will be made."""
            try:
                mail.mail.send(msg)
                helper_functions.flash_success("Reset Password Email has been sent")
                return redirect(url_for("index.index"))
            except Exception as e:
                print(e)
                abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
            return "Test"

    return render_template("forgot_password/forgot_password.html", form=form, title="Forgot Password")


@blueprint.route("/forgot/reset_password/<token>",methods=["GET","POST"])
def forgot_password_reset(token):
    try:
        token = serializer.loads(token,salt="PasswordReset",max_age=600)
        user = User.query.filter_by(reset_token=token.get("token"),id=token.get("id")).first()
        if not user:
            helper_functions.flash_error("Token Is Invalid")
            return redirect(url_for("index.index"))
    except SignatureExpired:
        helper_functions.flash_error("Token Has Expired")
        return redirect(url_for("index.index"))
    except BadSignature:
        helper_functions.flash_error("Token Is Invalid")
        return redirect(url_for("index.index"))


    if user.reset_token == token.get("token"):
        match request.method:
            case "GET":
                if user:
                    form = ForgotPasswordResetForm()
                    return helper_functions.helper_render("forgot_password/forgot_password_reset.html",form=form,target_user=user)
                else:
                    helper_functions.flash_error("BAD REQUEST")
                    return redirect(url_for("index.index"))
            case "POST":
                form = ForgotPasswordResetForm()
                user = User.query.filter_by(reset_token=token.get("token"),id=token.get("id")).first()
                if user:
                    if form.validate_on_submit():
                        try:
                            user.admin_update_password(form.new_password.data,form.confirm_new_password.data)
                            try:
                                user.reset_token = None
                                db.session.commit()
                                helper_functions.flash_success("Changed Password Successfully")
                                return redirect(url_for("crud.login"))
                            except sqlalchemy.exc.SQLAlchemyError:
                                helper_functions.flash_error("Error! Internal Server Error (SQLAlchemyError)")
                                pass
                        except custom_exceptions.PasswordNotMatchError:
                            form.new_password.errors.append("Passwords do not match")
                            form.confirm_new_password.errors.append("Passwords do not match")
                            helper_functions.flash_error("Passwords do not match")
                    return helper_functions.helper_render("forgot_password/forgot_password_reset.html",form=form,target_user=user)
                else:
                    helper_functions.flash_error("BAD REQUEST")
                    return redirect(url_for("index.index"))
    else:
        helper_functions.flash_error("Invalid Token")
        return redirect(url_for("index.index"))
