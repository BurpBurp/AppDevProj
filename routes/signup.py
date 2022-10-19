from flask import Blueprint, request, redirect, render_template, url_for, session, flash
from sqlalchemy import exc, select, or_, and_
from database import db
from UserDBModel import User

blueprint = Blueprint("signup",__name__,template_folder="templates")

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
                return render_template("signup.html")
        else:
            flash("User.User already exists")
            return render_template("signup.html")
        return redirect(url_for("index.index"))
    else:
        if "username" in session:
            print(f"Session Cached, {session['username']}")
            return redirect(url_for("index.index"))
        return render_template("signup.html")

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
            return render_template("login.html")
    else:
        if "username" in session:
            print(f"Session Cached, {session['username']}")
            flash("Logged in Successfully")
            return redirect(url_for("index.index"))
        return render_template("login.html")

@blueprint.route("/signout", methods=["GET","POST"])
def signout():
    session.pop("username",None)
    return redirect(url_for("index.index"))
