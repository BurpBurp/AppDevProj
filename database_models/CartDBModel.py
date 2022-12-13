from sqlalchemy import select, ForeignKey, ARRAY
from database import db
from database_models.UserDBModel import User
import custom_exceptions


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey(User.id))
    total = db.Column(db.Float,default=0)
    cart_items = db.relationship("Cart_Item",backref="Cart")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_items = db.relationship("Cart_Item",backref="Item")
    name = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.String)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    images = db.Column(db.PickleType,default=[])
    category = db.Column(db.String)


class Cart_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer,ForeignKey(Cart.id))
    Item_id = db.Column(db.Integer,ForeignKey(Item.id))
    qty = db.Column(db.Integer,default=1)

