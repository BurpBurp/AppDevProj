import os.path

from flask import session, render_template, flash, redirect, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import secrets
import flask_login


def helper_render(template, **kwargs):
    if check_logged_in():
        user = flask_login.current_user
        if user.is_authenticated:
            return render_template(template, user=user, **kwargs)
    return render_template(template, **kwargs)

def admin_required(function):
    def wrapper(*args,**kwargs):
        if flask_login.current_user.role < 1:
            flash_error("Permission Denied")
            return redirect(url_for("index.index"))
        else:
            return function(*args,**kwargs)
    wrapper.__name__ = function.__name__
    return wrapper

def check_logged_in():
    return flask_login.current_user.is_authenticated


def flash_error(message):
    flash(message, "error")


def flash_success(message):
    flash(message, "success")


def flash_primary(message):
    flash(message, "none")


