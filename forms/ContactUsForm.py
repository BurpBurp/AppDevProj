from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, length, NumberRange


class ContactUsForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), length(1, 100)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone_number = IntegerField("Phone Number", validators=[DataRequired(), NumberRange(30000000, 99999999)])
    message = TextAreaField("Message", validators=[DataRequired(), length(1, 5000)])
    submit = SubmitField("Submit Request")


class UpdateContactForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), length(1, 100)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone_number = IntegerField("Phone Number", validators=[DataRequired(), NumberRange(30000000, 99999999)])
    message = TextAreaField("Message", validators=[])
    submit = SubmitField("Submit Request")
