from flask import Blueprint, session, redirect,url_for,render_template
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database import db
import flask_login
from sqlalchemy import text
from flask_mail import Message
import Mail

blueprint = Blueprint("test", __name__, template_folder="templates")

@blueprint.route("/test")
def test():
    print("Received GET")
    msg = Message(subject="Testing",recipients=["dphxdarwin@gmail.com"])
    msg.attach("logo.png",'image/png',data=open("static/Logo.png","rb").read(),disposition="inline",headers=[['Content-ID','<Logo>']])
    msg.html = render_template("Order_Confirmation/Order_Confirmation.html",items=[["Dicks",10,5],["Cocks",5,3],["Balls",8,10]])
    msg.sender = "KH-Wares"
    Mail.mail.send(msg)
    print("msg sent")
    return render_template("Order_Confirmation/Order_Confirmation.html",items=[["Dicks",10,5],["Cocks",5,3],["Balls",8,10]])
