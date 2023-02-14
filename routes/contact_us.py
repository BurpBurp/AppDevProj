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
import smtplib

gmail_user = 'ywps2022@gmail.com'
gmail_password = 'jpfrxrdpsctwbuxk'


def send_email(to, subject, message):

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        message = 'Subject: {}\n\n{}'.format(subject, message)
        server.sendmail(gmail_user, to, message)
    finally:
        server.quit()


blueprint = Blueprint("contact", __name__, template_folder="templates")


@blueprint.route("/contact-us-form", methods=["GET", "POST"])
def contact_us():
    form = ContactUsForm()
    if request.method == "GET":
        return render_template("contact/custform.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            print(form.errors)
            contact = ContactUs(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data,
                                message=form.message.data)
            db.session.add(contact)
            db.session.commit()
            to = form.email.data
            subject = 'KH Wares query confirmation email'
            message = f'''Dear Mr/Mrs {form.name.data}
Thank you for reaching out to our customer support team. We appreciate you taking the time to contact us and allowing us the opportunity to assist you. Your message is of upmost importance to us and we will contact you as soon as we can. 

Here is a summary of your query:
"{form.message.data}".

If you have any additional queries or support needs, do not hesitate to contact us again, we will always be here to help!

Best regards,
The KH Wares team
'''
            send_email(to, subject, message)

            support_subject = f"Query from {form.email.data}"
            support_message = f'''Customer query from Mr/Mrs {form.name.data}, {form.email.data}

Query Details:
{form.message.data}

Contact details:
Name: {form.name.data}
Email: {form.email.data}
Phone number: {form.phone_number.data}
'''
            send_email(gmail_user,support_subject, support_message)
            return redirect(url_for("contact.thank_you_page"))
        print(form.errors)
        return render_template("contact/custform.html", form=form)


@blueprint.route("/contact-us/update/<id>/", methods=["GET", "POST"])
def update_contact(id):
    if not (contact := get_contact_by_id(id)):
        return redirect(url_for("index.index"))

    form = UpdateContactForm()
    if request.method == "GET":
        return render_template("contact/custform.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            print(form.errors)
            contact.name = form.name.data
            contact.email = form.email.data
            contact.phone_number = form.phone_number.data
            contact.message = form.message.data
            db.session.commit()
            return redirect(url_for("contact.contact_list"))
        print(form.errors)
        return render_template("contact/custform.html", form=form)


@blueprint.route("/contact/list", methods=["GET"])
def contact_list():
    return render_template("contact/contactlist.html", contact_list=get_all_contact())


@blueprint.route("/contact/list/delete/<id>/", methods=["GET"])
def delete_contact(id):
    if contact := get_contact_by_id(id):
        db.session.delete(contact)
        db.session.commit()
        return render_template("contact/contactlist.html", contact_list=get_all_contact())
    return render_template("contact/contactlist.html", contact_list=get_all_contact())


@blueprint.route("/contact-us")
def contact_us_page():
    return render_template("contact/contactus.html")


@blueprint.route("/thank-you")
def thank_you_page():
    return render_template("contact/thankyoupage.html")
