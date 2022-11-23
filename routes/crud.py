from flask import Blueprint, request, redirect, url_for, session, abort
from sqlalchemy import exc, select, or_, and_
from database import db
from database_models.UserDBModel import User, HelperUser, get_user_by_username, get_user_by_id
import custom_exceptions
import helper_functions

blueprint = Blueprint("crud",__name__,template_folder="templates")

@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
        except KeyError:
            return redirect(url_for("crud.signup"))
        newUser = User(username=name,email=email,password=password)
        existingUser = db.session.execute(select(User).where(or_(User.username == name, User.email == email))).scalar()
        if not existingUser:
            try:
                db.session.add(newUser)
                db.session.commit()
                session["username"] = name
                db.session.close()
            except exc.IntegrityError:
                helper_functions.flash_error("User already exists")
                return helper_functions.helper_render("signup.html")
        else:
            helper_functions.flash_error("User already exists")
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
            helper_functions.flash_success("Logged in Successfully")
            return redirect(url_for("index.index"))
        else:
            helper_functions.flash_error("Username/Password Wrong")
            return helper_functions.helper_render("login.html")
    else:
        if helper_functions.check_logged_in():
            print(f"Session Cached, {session['username']}")
            helper_functions.flash_success("Already Logged in")
            return redirect(url_for("index.index"))
        return helper_functions.helper_render("login.html")

@blueprint.route("/update", methods = ["GET","POST"])
def update():
    if "username" not in session: # If not Logged in
        return redirect(url_for("crud.login"))
    if not helper_functions.check_logged_in(): # If logged in user exists, aka not deleted
        return redirect(url_for("crud.login"))
    sessUsername = session["username"] # current username to sessUsername
    currentUser = get_user_by_username(sessUsername) # get current user db object

    if request.method == "GET": # if get method
        args = request.args # grab arguments
        id = args.get("id",None) # grab id
        if id: # if ID in args
            target_user = get_user_by_id(id) # try and get user by id
            if target_user: # if grab user successful
                role_to_send = currentUser.role # set role to send as current user role.
                # role_to_send determine if password required for changes to account
                if target_user.id == currentUser.id: # if updated user is same. Override role to send as user. Forces password to be entered
                    role_to_send = "user"
                if sessUsername == target_user.username or currentUser.role == "admin": # if not logged as rurrent user or not admin
                    return helper_functions.helper_render("update.html", role=role_to_send, target_user = target_user) # send to own update page
                else:
                    abort(403,"Access Denied")
            else:
                helper_functions.flash_error(f"User with ID: {id} does not exist") #if id not valid send to own update page
                return redirect(url_for("crud.update",id=currentUser.id))
        else:
            helper_functions.flash_error("No ID Provided") # if id not provided send to own update page
            return redirect(url_for("crud.update",id=currentUser.id))


    else: # POST method
        form = request.form
        try:
            userId = form["userID"]
        except KeyError:
            abort(400,"Missing form inputs")

        if not (user := get_user_by_id(userId)):
            helper_functions.flash_error(f"User with ID: {userId} does not exist")
            return redirect(url_for("crud.update",id=currentUser.id))
        user = HelperUser(user)

        role_to_send = currentUser.role
        change_self = False
        if user.get_id() == currentUser.id:
            change_self = True
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
                    helper_functions.flash_error("Missing Form Inputs")
                    return redirect(url_for("crud.update",id=user.get_id()))

                try:
                    user.change_password(old_pass,new_pass,new_pass_repeat,role_to_send)
                    helper_functions.flash_success("Password Change Successful")
                    return redirect(url_for("crud.update",id=user.get_id()))

                except custom_exceptions.WrongPasswordError:
                    helper_functions.flash_error("Entered Password is Wrong")
                    return redirect(url_for("crud.update",id=user.get_id()))

                except custom_exceptions.PasswordNotMatchError:
                    helper_functions.flash_error("Passwords do not match")
                    return redirect(url_for("crud.update",id=user.get_id()))


            case "changeEmail":

                try:
                    old_pass = form["curPass"]
                    email = form["email"]
                except KeyError:
                    helper_functions.flash_error("Missing Form Inputs")
                    return redirect(url_for("crud.update",id=user.get_id()))

                try:
                    user.change_email(old_pass,email,role_to_send)
                    helper_functions.flash_success("Email Change Successful")
                    return redirect(url_for("crud.update",id=user.get_id()))

                except custom_exceptions.WrongPasswordError:
                    helper_functions.flash_error("Entered Password is Wrong")
                    return redirect(url_for("crud.update",id=user.get_id()))

                except custom_exceptions.RepeatedEmailError:
                    helper_functions.flash_error("Email already in use")
                    return redirect(url_for("crud.update",id=user.get_id()))

            case "deleteAccount":
                try:
                    password = form["curPass"]
                except KeyError:
                    return redirect(url_for("crud.update",id=user.get_id()))

                try:
                    user.delete_user(password,role_to_send)
                except custom_exceptions.WrongPasswordError:
                    helper_functions.flash_error("Entered Password is Wrong")
                    return redirect(url_for("crud.update",id=user.get_id()))
                helper_functions.flash_success("Account Deleted")
                if change_self:
                    session.pop("username",None)
                    return redirect(url_for("index.index"))
                return redirect(url_for("admin.admin"))


            case _:
                abort(400,"Bad changeType")

@blueprint.route("/signout", methods=["GET","POST"])
def signout():
    if "username" in session:
        session.pop("username",None)
        helper_functions.flash_primary("Signed Out Successfully")
    return redirect(url_for("index.index"))
