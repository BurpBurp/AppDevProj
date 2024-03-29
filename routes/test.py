from flask import Blueprint, session, redirect, url_for, render_template, jsonify

import helper_functions
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database_models.OrderDBModel import *
from database import db
import flask_login
from sqlalchemy import text
import secrets
from serializer import non_timed_serializer
from itsdangerous import BadSignature
from flask_mail import Message
import mail
import stripe

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
    for i in range(5):
        item = Item(name=f"Bread_{i}",price=20,description="Bread, Bread",category="Foodstuffs")
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



@blueprint.route("/admin_required")
@helper_functions.admin_required
@flask_login.login_required
def admin_required():
    return("Hello")



@blueprint.route("/test/orders")
@flask_login.login_required
def admin_required2():
    print(flask_login.current_user.is_authenticated)
    print(flask_login.current_user.username)
    print(flask_login.current_user.order)
    print(flask_login.current_user.order[0].order_items[0].item.name)
    return "SOMETHING"









