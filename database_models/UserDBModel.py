# Darwin's Stuff
from sqlalchemy import select, exc, func, and_
from numbers import Number
import helper_functions
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
import custom_exceptions
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, default=0)  # 0 - User, 1 - Employee, 2 - Admin
    cart = db.relationship("Cart", backref="user", uselist=False)
    order = db.relationship("Order", backref="user")
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    reset_token = db.Column(db.String)
    profile_pic = db.Column(db.String, default="default.png")
    date_created = db.Column(db.DateTime(), default=func.now())
    totp_secret = db.Column(db.String)

    def get_role_str(self):
        match self.role:
            case 0:
                return "User"
            case 1:
                return "Employee"
            case 2:
                return "Administrator"

    def update_name(self, f_name, l_name):
        self.f_name = f_name
        self.l_name = l_name
        db.session.commit()

    def update_email(self, current_password, email:str, is_admin=False):
        if check_password_hash(self.password,current_password) or is_admin:
            self.email = str(email).lower()
            db.session.commit()
        else:
            raise custom_exceptions.WrongPasswordError("Passwords Dont Match")

    def update_password(self,current_password,new_password,confirm_password):
        if check_password_hash(self.password,current_password):
            self.password = generate_password_hash(new_password)
            db.session.commit()
        else:
            raise custom_exceptions.WrongPasswordError("Passwords Dont Match")
    
    def admin_update_password(self,new_password,confirm_password):
        self.password = generate_password_hash(new_password)
        db.session.commit()

    def remove_totp(self,current_password,is_admin=False):
        if check_password_hash(self.password,current_password) or is_admin:
            self.totp_secret = None
            db.session.commit()
        else:
            raise custom_exceptions.WrongPasswordError()

    def delete_account(self, current_password,is_admin=False):
        if check_password_hash(self.password,current_password) or is_admin:
            db.session.delete(self)
            db.session.commit()
        else:
            raise custom_exceptions.WrongPasswordError("Passwords Dont Match")

    def admin_delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def admin_update_role(self,role):
        self.role = role
        db.session.commit()


# HelperUser Depreciated
# class HelperUser:
#     def __init__(self, user: User):
#         if isinstance(user, User):
#             self.__user = user
#             self.__username = user.username
#             self.__password = user.password
#             self.__email = user.email
#             self.__id = user.id
#             self.__role = user.role
#         elif user is None:
#             print(f"user not found")
#             raise ValueError(f"user not found")
#         else:
#             print(f"Expected Type User got {type(user)}")
#             raise TypeError(f"Expected Type User got {type(user)}")
#
#     def get_id(self):
#         return self.__id
#
#     def get_username(self):
#         return self.__username
#
#     def change_password(self, old_pass, new_pass, new_pass_repeat, role=0):
#         print(old_pass, new_pass, new_pass_repeat, role)
#         if role >= 2:
#             old_pass = self.__password
#         if old_pass == self.__password:
#             if new_pass == new_pass_repeat:
#                 self.__user.password = new_pass
#                 self.__password = new_pass
#                 db.session.commit()
#                 print(self.__password)
#                 return True
#             else:
#                 raise custom_exceptions.PasswordNotMatchError("Passwords Dont Match")
#         else:
#             raise custom_exceptions.WrongPasswordError("Password Is Wrong")
#
#     def change_email(self, current_pass, email, role=0):
#         if get_user_by_email(email):
#             raise custom_exceptions.RepeatedEmailError()
#
#         if role >= 2:
#             current_pass = self.__password
#         if current_pass == self.__password:
#             self.__user.email = email
#             self.__email = email
#             db.session.commit()
#             return
#         else:
#             raise custom_exceptions.WrongPasswordError()
#
#     def __change_username(self, username, password):
#         if self.__password == password:
#             self.__user.username = username
#             db.session.commit()
#         else:
#             print("Password wrong")
#
#     def delete_user(self, current_password, role=0):
#         if role >= 2:
#             current_password = self.__password
#         if current_password == self.__password:
#             db.session.delete(self.__user)
#             db.session.commit()
#         else:
#             raise custom_exceptions.WrongPasswordError()


class UserStats():
    def init(self):
        pass

    def get_num_users(self):
        return len(db.session.execute(select(User).where(User.role == 0)).all())

    def get_num_employees(self):
        return len(db.session.execute(select(User).where(User.role == 1)).all())

    def get_num_admins(self):
        return len(db.session.execute(select(User).where(User.role == 2)).all())


def get_user_by_username(name: str) -> User | None:
    user: User = db.session.execute(select(User).where(User.username == str(name))).first()
    if user:
        return user[0]
    else:
        return None


def get_user_by_id(id: Number) -> User | None:
    user = db.session.execute(select(User).where(User.id == str(id))).first()
    if user:
        return user[0]
    else:
        return None


def get_user_by_email(email: str) -> User | None:
    user = db.session.execute(select(User).where(User.email == str(email))).first()
    if user:
        return user[0]
    else:
        return None


def get_all_users():
    users = db.session.execute(select(User)).all()
    return users


def create_user(username, password, f_name, l_name, email, role=0):
    try:
        user = User(username=username, password=password, f_name=f_name, l_name=l_name, email=str(email).lower(), role=role)
        db.session.add(user)
        db.session.commit()
        return user
    except exc.IntegrityError:
        db.session.rollback()
        raise custom_exceptions.UserAlreadyExistsError


def try_login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password,password):
            return user
        else:
            return None
    else:
        return None
