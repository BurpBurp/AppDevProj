from flask import session, render_template, flash
import flask_login


def helper_render(template, **kwargs):
    if check_logged_in():
        user = flask_login.current_user
        if user.is_authenticated:
            return render_template(template, user=user, **kwargs)
    return render_template(template, **kwargs)


def check_logged_in():
    return flask_login.current_user.is_authenticated


def flash_error(message):
    flash(message, "error")


def flash_success(message):
    flash(message, "success")


def flash_primary(message):
    flash(message, "none")
