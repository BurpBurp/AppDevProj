from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(message="Please Enter Username")])
    password = PasswordField("Password",validators=[DataRequired(message="Please Enter Password")])
    remember = BooleanField("Remember me?")
    submit = SubmitField("Log In")
