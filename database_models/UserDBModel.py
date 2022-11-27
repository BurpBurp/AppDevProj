from sqlalchemy import select, exc, func
from database import db
import custom_exceptions


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user")
    cart_id = db.relationship("Cart", backref="User", uselist=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime(),default=func.now())


class HelperUser:
    def __init__(self, user: User):
        if isinstance(user, User):
            self.__user = user
            self.__username = user.username
            self.__password = user.password
            self.__email = user.email
            self.__id = user.id
            self.__role = user.role
        elif user is None:
            print(f"user not found")
            raise ValueError(f"user not found")
        else:
            print(f"Expected Type User got {type(user)}")
            raise TypeError(f"Expected Type User got {type(user)}")

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def change_password(self, old_pass, new_pass, new_pass_repeat, role="user"):
        print(old_pass, new_pass, new_pass_repeat, role)
        if role == "admin":
            old_pass = self.__password
        if old_pass == self.__password:
            if new_pass == new_pass_repeat:
                self.__user.password = new_pass
                self.__password = new_pass
                db.session.commit()
                print(self.__password)
                return True
            else:
                raise custom_exceptions.PasswordNotMatchError("Passwords Dont Match")
        else:
            raise custom_exceptions.WrongPasswordError("Password Is Wrong")

    def change_email(self, current_pass, email, role="user"):
        if get_user_by_email(email):
            raise custom_exceptions.RepeatedEmailError()

        if role == "admin":
            current_pass = self.__password
        if current_pass == self.__password:
            self.__user.email = email
            self.__email = email
            db.session.commit()
            return
        else:
            raise custom_exceptions.WrongPasswordError()

    def __change_username(self, username, password):
        if self.__password == password:
            self.__user.username = username
            db.session.commit()
        else:
            print("Password wrong")

    def delete_user(self, current_password, role="user"):
        if role == "admin":
            current_password = self.__password
        if current_password == self.__password:
            db.session.delete(self.__user)
            db.session.commit()
        else:
            raise custom_exceptions.WrongPasswordError()

class UserStats():
    def init(self):
        pass

    def get_num_users(self):
        return len(db.session.execute(select(User)).all())

    def get_num_admins(self):
        return len(db.session.execute(select(User).where(User.role == "admin")).all())

def get_user_by_username(name: int) -> User | None:
    user: User = db.session.execute(select(User).where(User.username == name)).first()
    if user:
        return user[0]
    else:
        return None


def get_user_by_id(id: int) -> User | None:
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

def create_user(username,password,f_name,l_name,email,role="user"):
    try:
        user = User(username=username,password=password,f_name=f_name,l_name=l_name,email=email,role=role)
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        raise custom_exceptions.UserAlreadyExistsError
