from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<Task {self.id}>"


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    return render_template()

@app.route("/usr")
def user(usr):
    return render_template(f"<h1>{usr}</h1>")

if __name__ == '__main__':
    app.run(debug=True)
