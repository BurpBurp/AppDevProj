from flask import Blueprint, session, redirect, url_for, render_template, jsonify, request

import helper_functions
from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database_models.ContactDBModel import *
from forms.ContactUsForm import ContactUsForm, UpdateContactForm
from database import db
import flask_login
from sqlalchemy import text
from flask_mail import Message
import mail

blueprint = Blueprint("contact", __name__, template_folder="templates")

@blueprint.route("/contact-us",methods=["GET","POST"])
def contact_us():
    form = ContactUsForm()
    if request.method == "GET":
        return render_template("contact/custform.html",form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            print(form.errors)
            contact = ContactUs(name=form.name.data,email=form.email.data,phone_number=form.phone_number.data,message=form.message.data)
            db.session.add(contact)
            db.session.commit()
            return redirect(url_for("index.index"))
        print(form.errors)
        return render_template("contact/custform.html",form=form)

@blueprint.route("/contact-us/update/<id>/",methods=["GET","POST"])
def update_contact(id):
    if not (contact := get_contact_by_id(id)):
        return redirect(url_for("index.index"))

    form = UpdateContactForm()
    if request.method == "GET":
        return render_template("contact/custform.html",form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            print(form.errors)
            contact.name = form.name.data
            contact.email = form.email.data
            contact.phone_number = form.phone_number.data
            contact.message = form.message.data
            db.session.commit()
            return redirect(url_for("index.index"))
        print(form.errors)
        return render_template("contact/custform.html",form=form)

@blueprint.route("/contact/list",methods=["GET"])
def contact_list():
    return render_template("contact/contactlist.html", contact_list=get_all_contact())

@blueprint.route("/contact/list/delete/<id>/",methods=["GET"])
def delete_contact(id):
    if contact := get_contact_by_id(id):
        db.session.delete(contact)
        db.session.commit()
        return render_template("contact/contactlist.html", contact_list=get_all_contact())
    return render_template("contact/contactlist.html", contact_list=get_all_contact())
