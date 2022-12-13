from flask import Blueprint, session, redirect, url_for, render_template
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database import db
import flask_login
from sqlalchemy import text
from flask_mail import Message
import mail

blueprint = Blueprint("test", __name__, template_folder="templates")


@blueprint.route("/test")
def test():
    # #mail dont work on sch network
    # items = [["Dicks", 10, 5], ["Cocks", 5, 3], ["Balls", 8, 10]]
    # total = sum(i[1] * i[2] for i in items)
    # print("Received GET")
    # msg = Message(subject="Testing", recipients=[])
    # msg.attach("logo.png", 'image/png', data=open("static/Logo.png", "rb").read(), disposition="inline",
    #            headers=[['Content-ID', '<Logo>']])
    # msg.html = render_template("Order_Confirmation/Order_Confirmation.html",
    #                            items=items,total=total)
    # msg.sender = "KH-Wares"
    # mail.mail.send(msg)
    # print("msg sent")
    # return render_template("Order_Confirmation/Order_Confirmation.html",
    #                        items=[["Dicks", 10, 5], ["Cocks", 5, 3], ["Balls", 8, 10]])
    item = Item(name="Test",price=100.0,description="Test Desc",images=["Test","Test1"],category="ABC")
    db.session.add(item)
    print(Item.query.all().first())
    cart_item = Cart_Item(Item=Item.query.filter_by(id=1).first(),qty=100)
    db.session.add(cart_item)
    db.session.commit()
