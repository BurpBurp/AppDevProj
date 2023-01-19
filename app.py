from flask import Flask, session
from flask_session import Session
from database import db
import os
import mail
import routes.test as test
import routes.crud as crud
import routes.index as index
import routes.admin as admin
import routes.InventoryManagement as inventory
import routes.store as store
import routes.cart as cart
from database_models.UserDBModel import User
from database_models.CartDBModel import Cart
import flask_login
import errors.page_not_found, errors.permission_denied
from flask_wtf import CSRFProtect

login_manager = flask_login.LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['UPLOAD_FOLDER'] = "/temp/uploads"
    init_mail_service(app)
    init_database_service(app)
    init_flask_login_service(app)
    register_errors(app)
    register_blueprints(app)
    Session(app)  # Start Sever Side Session
    return app


def init_mail_service(app: Flask):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'khwaresappdev@gmail.com'
    app.config['MAIL_PASSWORD'] = 'akfxhtnsjvdokqez'
    app.config['MAIL_USE_TLS'] = True
    mail.mail.init_app(app)


def init_flask_login_service(app: Flask):
    login_manager.init_app(app)
    login_manager.login_view = "crud.login"


def init_database_service(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///master.db"
    app.config['SESSION_SQLALCHEMY'] = db
    db.init_app(app)


def register_errors(app: Flask):
    app.register_error_handler(404, errors.page_not_found.page_not_found)
    app.register_error_handler(403, errors.permission_denied.permission_denied)


def register_blueprints(app: Flask):
    app.register_blueprint(test.blueprint)  # Register Test Route
    app.register_blueprint(crud.blueprint)  # Register CRUD Routes
    app.register_blueprint(index.blueprint)  # Register index routes
    app.register_blueprint(admin.blueprint)  # Register Admin Routes
    app.register_blueprint(inventory.blueprint)  # Register Inventory Route
    app.register_blueprint(cart.blueprint)
    app.register_blueprint(store.blueprint)

def setup_database(app: Flask):
    with app.app_context():
        db.create_all()


@login_manager.user_loader
def user_loader(id):
    user = User.query.filter_by(id=id).first()
    return user


if __name__ == "__main__":
    app: Flask = create_app()
    if not os.path.isfile('instance/master.db'):
        setup_database(app)
    app.run()
