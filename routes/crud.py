from flask import Blueprint, request, redirect, render_template, url_for, session, flash, abort
from sqlalchemy import exc, select, or_, and_
from database import db
from UserDBModel import User, HelperUser, get_user_by_username, get_user_by_id
import custom_exceptions
import helper_functions

blueprint = Blueprint("crud",__name__,template_folder="templates")

@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        newUser = User(username=name,email=email,password=password)
        existingUser = db.session.execute(select(User).where(or_(User.username == name, User.email == email))).scalar()
        if not existingUser:
            try:
                db.session.add(newUser)
                db.session.commit()
                session["username"] = name
                db.session.close()
            except exc.IntegrityError:
                flash("User.User already exists")
                return helper_functions.helper_render("signup.html")
        else:
            flash("User.User already exists")
            return helper_functions.helper_render("signup.html")
        return redirect(url_for("index.index"))
    else:
        if helper_functions.check_logged_in():
            print(f"Session Cached, {session['username']}")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("signup.html")

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        existingUser = db.session.execute(select(User).where(and_(User.username == name, User.password == password))).scalar()
        if existingUser:
            session["username"] = existingUser.username
            flash("Logged in Successfully")
            return redirect(url_for("index.index"))
        else:
            flash("Username/Password Wrong")
            return helper_functions.helper_render("login.html")
    else:
        if helper_functions.check_logged_in():
            print(f"Session Cached, {session['username']}")
            flash("Logged in Successfully")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("login.html")

@blueprint.route("/update", methods = ["GET","POST"])
def update():
    if "username" not in session:
        return redirect(url_for("crud.login"))
    sessUsername = session["username"]
    currentUser = get_user_by_username(sessUsername)
    if request.method == "GET":
        args = request.args
        id = args.get("id",None)
        if id:
            target_user = get_user_by_id(id)
            if target_user:
                role_to_send = currentUser.role
                if target_user.id == currentUser.id:
                    role_to_send = "user"
                if sessUsername == target_user.username or currentUser.role == "admin":
                    return helper_functions.helper_render("update.html", role=role_to_send, target_user = target_user)
                else:
                    abort(403,"Access Denied")
            else:
                abort(400, "Invalid ID")
        else:
            return redirect(url_for("crud.update",id=currentUser.id))


    else:
        form = request.form
        try:
            userId = form["userID"]
        except KeyError:
            abort(400,"Missing form inputs")

        if not (user := get_user_by_id(userId)):
            abort(400,"User ID not valid")
            return redirect(url_for("crud.update",id=currentUser.id))
        user = HelperUser(user)

        role_to_send = currentUser.role
        if user.get_id() == currentUser.id:
            role_to_send = "user"

        if not (user.get_username() == session["username"] or currentUser.role == "admin"):
            abort(403,"Access Denied")
            return redirect(url_for("index.index"))

        match form["changeType"]:
            case "changePass":

                try:
                    old_pass = form["curPass"]
                    new_pass = form["newPass"]
                    new_pass_repeat = form["newPassRepeat"]
                except KeyError:
                    abort(400, "Missing form inputs")
                    return redirect(url_for("crud.update",id=currentUser.id))

                try:
                    user.change_password(old_pass,new_pass,new_pass_repeat,role_to_send)
                    flash("Password Change Successful")
                    return redirect(url_for("crud.update"))

                except custom_exceptions.WrongPasswordError:
                    flash("Entered Password is Wrong")
                    return redirect(url_for("crud.update"))

                except custom_exceptions.PasswordNotMatchError:
                    flash("Passwords do not match")
                    return redirect(url_for("crud.update"))


            case "changeEmail":

                try:
                    old_pass = form["curPass"]
                    email = form["email"]
                except KeyError:
                    abort(400, "Missing form inputs")
                    return redirect(url_for("crud.update",id=currentUser.id))

                try:
                    user.change_email(old_pass,email,role_to_send)
                    flash("Email Change Successful")
                    return redirect(url_for("crud.update"))

                except custom_exceptions.WrongPasswordError:
                    flash("Entered Password is Wrong")
                    return redirect(url_for("crud.update"))

            case other:
                abort(400,"Bad changeType")

@blueprint.route("/signout", methods=["GET","POST"])
def signout():
    if "username" in session:
        session.pop("username",None)
        helper_functions.helper_flash("Signed Out Successfully")
    return redirect(url_for("index.index"))
