# Darwin's Stuff
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterTOTP(FlaskForm):
    secret = HiddenField()
    otp = StringField("One Time Password",validators=[DataRequired(message="Please Enter OTP")])
    submit = SubmitField("Authenticate")

class LoginTOTP(FlaskForm):
    otp = StringField("One Time Password",validators=[DataRequired(message="Please Enter OTP")])
    submit = SubmitField("Login")

class RemoveTOTP(FlaskForm):
    current_password = PasswordField("Current Password",validators=[DataRequired()])
    submit = SubmitField("Remove OTP")
