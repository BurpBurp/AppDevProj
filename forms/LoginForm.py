from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username (Case-Sensitive)",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember me?")
    submit = SubmitField("Log In")
