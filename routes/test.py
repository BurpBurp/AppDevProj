from flask import Blueprint, session, redirect, url_for, render_template, jsonify
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database import db
import flask_login
from sqlalchemy import text
from flask_mail import Message
import mail

blueprint = Blueprint("test", __name__, template_folder="templates")


@blueprint.route("/test_email")
def test_email():
    #mail dont work on sch network
    items = [["Dicks", 10, 5], ["Cocks", 5, 3], ["Balls", 8, 10]]
    total = sum(i[1] * i[2] for i in items)
    print("Received GET")
    msg = Message(subject="Testing", recipients=[])
    msg.attach("logo.png", 'image/png', data=open("static/Logo.png", "rb").read(), disposition="inline",
               headers=[['Content-ID', '<Logo>']])
    msg.html = render_template("Order_Confirmation/Order_Confirmation.html",
                               items=items,total=total)
    msg.sender = "KH-Wares"
    mail.mail.send(msg)
    print("msg sent")
    return render_template("Order_Confirmation/Order_Confirmation.html",
                           items=[["Dicks", 10, 5], ["Cocks", 5, 3], ["Balls", 8, 10]])


@blueprint.route("/test_add_cart")
def test_add_cart():
    create_user("CartTest","1234","Cart","Test","Test@email.com")
    cart = Cart(user=get_user_by_username("CartTest"))
    db.session.add(cart)
    db.session.commit()
    return("HI")

@blueprint.route("/test_add_item")
def test_add_item():
    item = Item(name="Bread",price=20,description="Bread, Bread",category="Foodstuffs")
    db.session.add(item)
    db.session.commit()
    return("HI")

@blueprint.route("/test_add_to_cart")
def test_add_to_cart():
    cart_item = Cart_Item(Cart=get_user_by_username("CartTest").cart_id,item=Item.query.filter_by(name="Bread").first())
    db.session.add(cart_item)
    db.session.commit()
    return("HI")

@blueprint.route("/get_user_cart/<user>")
def test_get_cart(user):
    for item in get_user_by_username(user).cart.cart_items:
        print(item.item.name)
        print(item.qty)
        item.qty += 1
        db.session.commit()
    print(any(item.item.name == "Food" for item in get_user_by_username(user).cart.cart_items))
    return "HI"


