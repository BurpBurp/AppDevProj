from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please Enter Username"),Regexp("^\S*$",message="Username cannot contain spaces")])
    f_name = StringField("First Name", validators=[DataRequired(message="Please Enter First Name")])
    l_name = StringField("Last Name", validators=[DataRequired(message="Please Enter Last Name")])
    email = EmailField("Email", validators=[DataRequired(message="Please Enter Email"), Email()])
    password = PasswordField("Password", validators=[DataRequired(message="Please Enter Password")])
    confirm_password = PasswordField("Re-Enter Password",
                                     validators=
                                     [DataRequired(message="Please Re-Enter Password"),
                                      EqualTo("password",message="Passwords Do Not Match")])
    submit = SubmitField("Sign Up")


class AdminCreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please Enter Username"),Regexp("^\S*$",message="Username cannot contain spaces")])
    f_name = StringField("First Name", validators=[DataRequired(message="Please Enter First Name")])
    l_name = StringField("Last Name", validators=[DataRequired(message="Please Enter Last Name")])
    email = EmailField("Email", validators=[DataRequired(message="Please Enter Email"), Email()])
    password = PasswordField("Password", validators=[DataRequired(message="Please Enter Password")])
    confirm_password = PasswordField("Re-Enter Password",
                                     validators=
                                     [DataRequired(message="Please Re-Enter Password"),
                                      EqualTo("password",message="Passwords Do Not Match")])
    role = SelectField("Role", choices=[(0, "User"),(1, "Employee"),(2, "Admin")])
    submit = SubmitField("Create Account")

class EmployeeCreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please Enter Username"),Regexp("^\S*$",message="Username cannot contain spaces")])
    f_name = StringField("First Name", validators=[DataRequired(message="Please Enter First Name")])
    l_name = StringField("Last Name", validators=[DataRequired(message="Please Enter Last Name")])
    email = EmailField("Email", validators=[DataRequired(message="Please Enter Email"), Email()])
    password = PasswordField("Password", validators=[DataRequired(message="Please Enter Password")])
    confirm_password = PasswordField("Re-Enter Password",
                                     validators=
                                     [DataRequired(message="Please Re-Enter Password"),
                                      EqualTo("password",message="Passwords Do Not Match")])
    role = SelectField("Role", choices=[(0, "User")])
    submit = SubmitField("Create Account")
