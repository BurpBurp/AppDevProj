from sqlalchemy import select
from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user")
    cart_id = db.Column(db.String, nullable=True)

class HelperUser():
    def __init__(self,user : User):
        if isinstance(user,User):
            self.__user = user
            self.__username = user.username
            self.__password = user.password
            self.__id = user.id
            self.__role = user.role
        elif user is None:
            raise ValueError(f"user not found")
        else:
            raise TypeError(f"Expected Type User got {type(user)}")

    def change_username(self,username,password):
        if self.__password == password:
            self.__user.username = username
            db.session.commit()
        else:
            print("Password wrong")

def get_user_by_username(name: str) -> User | None:
    user: User = db.session.execute(select(User).where(User.username == name)).first()[0]
    if user:
        return user
    else:
        return None


def get_user_by_id(id: int) -> User | None:
    user = db.session.execute(select(User).where(User.id == str(id))).first()[0]
    if user:
        return user
    else:
        return None
