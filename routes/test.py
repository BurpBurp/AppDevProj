from flask import Blueprint, session
from database_models.UserDBModel import *
from database_models.CartDBModel import *

blueprint = Blueprint("test", __name__, template_folder="templates")

@blueprint.route("/test")
def test():
    user = get_user_by_username(session["username"])
    db.session.add(Cart(User=user))
    db.session.commit()
    print(user.cart_id)
    item = db.session.execute(select(Item).where(Item.name == "Bread")).first()[0]
    db.session.add(Cart_Item(Cart=user.cart_id,Item=item))
    db.session.commit()
    print(user.cart_id.cart_items[0].Item.name)
