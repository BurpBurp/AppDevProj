from flask import session, render_template, flash
from database_models.UserDBModel import get_user_by_username


def helper_render(template, **kwargs):
    if check_logged_in():
        user = get_user_by_username(session.get("username"))
        if user:
            return render_template(template, user=user, **kwargs)
    return render_template(template, **kwargs)


def check_logged_in():
    if "username" in session:
        if user := get_user_by_username(session["username"]):
            return True
    return False


def flash_error(message):
    flash(message, "error")


def flash_success(message):
    flash(message, "success")


def flash_primary(message):
    flash(message, "none")
