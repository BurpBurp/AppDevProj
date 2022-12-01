from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    f_name = StringField("First Name", validators=[DataRequired()])
    l_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Re-Enter Password",
                                     validators=
                                     [DataRequired(),
                                      EqualTo("password")])
    submit = SubmitField("Sign Up")


class AdminCreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    f_name = StringField("First Name", validators=[DataRequired()])
    l_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Re-Enter Password",
                                     validators=
                                     [DataRequired(),
                                      EqualTo("password")])
    role = SelectField("Role", choices=[(0, "User"),(1, "Employee"),(2, "Admin")])
    submit = SubmitField("Create Account")
