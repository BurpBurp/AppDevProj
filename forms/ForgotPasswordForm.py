from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class ForgotPasswordForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    submit = SubmitField("Reset Password")

class ForgotPasswordResetForm(FlaskForm):
    new_password = PasswordField("New Password",validators=[DataRequired()])
    confirm_new_password = PasswordField("Re-Enter New Password",validators=[DataRequired(),EqualTo("new_password",message="Passwords Do Not Match")])
    submit = SubmitField("Reset Password")
