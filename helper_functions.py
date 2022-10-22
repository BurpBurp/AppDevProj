from flask import session, render_template,flash
from UserDBModel import get_user_by_username

def helper_render(template,**kwargs):
    if check_logged_in():
        user = get_user_by_username(session["username"])
        if user:
            return render_template(template,user=user,**kwargs)
    return render_template(template,**kwargs)

def check_logged_in():
    if "username" in session:
        if user := get_user_by_username(session["username"]):
            return True
    return False

def helper_flash(message,category=None):
    session.pop("_flashes",None)
    flash(message,category)
