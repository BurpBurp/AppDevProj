from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master.db'
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String,unique = True, nullable = False)
    email = db.Column(db.String,unique = True, nullable = False)
    password = db.Column(db.String,nullable = False)
    role = db.Column(db.String,default="user")

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        existingUserByName : User = db.session.execute(db.select(User).where(User.username == name)).scalar()
        existingUserByEmail : User = db.session.execute(db.select(User).where(User.email == email)).scalar()
        newUser = User(name,email,password)
        try:
            db.session.add(newUser)
            db.session.commit()
        except exc.IntegrityError:
            return "ERROR USER/EMAIL ALREADY EXISTS"
        print(db.session.execute(db.select(User).where(User.role == "user")).scalar().role)
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/usr")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
