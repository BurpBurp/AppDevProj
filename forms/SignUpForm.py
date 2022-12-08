from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


class SignUpForm(FlaskForm):
    username = StringField("Username (Case-Sensitive)", validators=[DataRequired(),Regexp("^\S*$",message="Username cannot contain spaces")])
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
    username = StringField("Username (Case-Sensitive)", validators=[DataRequired(),Regexp("^\S*$",message="Username cannot contain spaces")])
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

class EmployeeCreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    f_name = StringField("First Name", validators=[DataRequired()])
    l_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Re-Enter Password",
                                     validators=
                                     [DataRequired(),
                                      EqualTo("password")])
    role = SelectField("Role", choices=[(0, "User")])
    submit = SubmitField("Create Account")
