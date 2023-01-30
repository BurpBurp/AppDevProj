from sqlalchemy import select, ForeignKey, func
from database import db
from database_models.UserDBModel import User
from database_models.CartDBModel import Item

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey(User.id))
    total = db.Column(db.Float,default=0)
    token = db.Column(db.String)
    status = db.Column(db.String, default="PAID") # PAID, FULFILLED, COMPLETED
    order_items = db.relationship("Order_Item",backref="orders")
    date_created = db.Column(db.DateTime(), default=func.now())

class Order_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, ForeignKey(Order.id))
    item_id = db.Column(db.Integer,ForeignKey(Item.id))
    name = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.String)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    images = db.Column(db.PickleType,default=[])
    category = db.Column(db.String)
    fulfilled = db.Column(db.Boolean, default=False)
