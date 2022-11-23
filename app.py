from flask import Flask, session
from flask_session import Session
from database import db
import os
import routes.test as test
import routes.crud as crud
import routes.index as index
import routes.admin as admin
from database_models.UserDBModel import User
from database_models.CartDBModel import Cart
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///master.db"
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    csrf = CSRFProtect(app) # CSRF protect forms
    db.init_app(app) # Init DB
    app.register_blueprint(test.blueprint)
    app.register_blueprint(crud.blueprint) # Register CRUD Routes
    app.register_blueprint(index.blueprint) # Register index routes
    app.register_blueprint(admin.blueprint) # Reigster Admin Routes
    Session(app) # Start Sever Side Sessions
    return app


def setup_database(app: Flask):
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app: Flask = create_app()
    if not os.path.isfile('instance/master.db'):
        setup_database(app)
    app.run()
