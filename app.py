from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

# Flask and DB Init
app = Flask(__name__)

app.secret_key = 'the random string'
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master.db'
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)
db.init_app(app)

app.config['SESSION_SQLALCHEMY'] = db
# Session Init
Session(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        newUser = User(name, email, password)
        try:
            db.session.add(newUser)
            try:
                db.session.commit()
            except exc.PendingRollbackError:
                print("Rollback")
                db.session.rollback()
                raise
            finally:
                db.session.close()
        except exc.IntegrityError:
            print("Duplicate")
            return "ERROR USER/EMAIL ALREADY EXISTS"
        print(db.session.execute(db.select(User).where(User.role == "user")).scalar().role)
        session["id"] = newUser.id
        return redirect(url_for("index"))
    else:
        if "username" in session:
            print(f"Session Cached, {session['id']}")
            return redirect(url_for("index"))
        return render_template("login.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
