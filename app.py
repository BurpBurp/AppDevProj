from flask import Flask, session
from flask_session import Session
from database import db
import os
import Mail
import routes.test as test
import routes.crud as crud
import routes.index as index
import routes.admin as admin
from database_models.UserDBModel import User
from database_models.CartDBModel import Cart
import flask_login
import errors.page_not_found, errors.permission_denied
from flask_wtf import CSRFProtect

login_manager = flask_login.LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///master.db"
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'khwaresappdev@gmail.com'
    app.config['MAIL_PASSWORD'] = 'rggiwzpuikfcinpq'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    csrf = CSRFProtect(app) # CSRF protect forms
    login_manager.init_app(app) #init flask login
    login_manager.login_view = "crud.login"
    db.init_app(app) # Init DB
    app.register_blueprint(test.blueprint)
    app.register_blueprint(crud.blueprint) # Register CRUD Routes
    app.register_blueprint(index.blueprint) # Register index routes
    app.register_blueprint(admin.blueprint) # Reigster Admin Routes
    app.register_error_handler(404,errors.page_not_found.page_not_found)
    app.register_error_handler(403,errors.permission_denied.permission_denied)
    Session(app) # Start Sever Side Session
    Mail.mail.init_app(app)
    return app


def setup_database(app: Flask):
    with app.app_context():
        db.create_all()

@login_manager.user_loader
def user_loader(id):
    user = User.query.filter_by(id = id).first()
    return user

if __name__ == "__main__":
    app: Flask = create_app()
    if not os.path.isfile('instance/master.db'):
        setup_database(app)
    app.run()
