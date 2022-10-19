import sqlalchemy
from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, select, Column, text, and_, or_
from flask_wtf.csrf import CSRFProtect
import User



# Flask and DB Init
app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master.db'
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)
User.db.init_app(app)
db.init_app(app)


app.config['SESSION_SQLALCHEMY'] = db
# Session Init
Session(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        newUser = User.User(username=name,email=email,password=password)
        existingUser = db.session.execute(select(User.User).where(or_(User.User.username == name, User.User.email == email))).scalar()
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
        return redirect(url_for("index"))
    else:
        if "username" in session:
            print(f"Session Cached, {session['username']}")
            return redirect(url_for("index"))
        return render_template("signup.html")

@app.route("/signout", methods=["GET","POST"])
def signout():
    session.pop("username",None)
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        existingUser = db.session.execute(select(User.User).where(and_(User.User.username == name, User.User.password == password))).scalar()
        if existingUser:
            session["username"] = existingUser.username
            flash("Logged in Successfully")
            return redirect(url_for("index"))
        else:
            flash("Username/Password Wrong")
            return render_template("login.html")
    else:
        if "username" in session:
            print(f"Session Cached, {session['username']}")
            flash("Logged in Successfully")
            return redirect(url_for("index"))
        return render_template("login.html")



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        User.db.create_all()
    app.run(debug=True)
