from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class UpdatePasswordForm(FlaskForm):
    target_user_id = HiddenField()
    change_type = HiddenField(default="UpdatePassword")
    current_password = PasswordField("Current Password",validators=[DataRequired()])
    new_password = PasswordField("New Password",validators=[DataRequired()])
    confirm_new_password = PasswordField("Re-Enter New Password",validators=[DataRequired(),EqualTo("new_password")])
    submit = SubmitField("Change Password")

class UpdateEmailForm(FlaskForm):
    target_user_id = HiddenField()
    change_type = HiddenField(default="UpdateEmail")
    current_password = PasswordField("Current Password",validators=[DataRequired()])
    new_email = EmailField("New Email",validators=[DataRequired(),Email()])
    submit = SubmitField("Change Email")

class UpdateNameForm(FlaskForm):
    target_user_id = HiddenField()
    change_type = HiddenField(default="UpdateName")
    new_f_name = StringField("First Name",validators=[DataRequired()])
    new_l_name = StringField("Last Name",validators=[DataRequired()])
    submit = SubmitField("Update Profile")

class UpdateDeleteForm(FlaskForm):
    target_user_id = HiddenField()
    change_type = HiddenField(default="UpdateDelete")
    current_password = PasswordField("Current Password",validators=[DataRequired()])
    submit = SubmitField("Delete Account")

class UpdateImageForm(FlaskForm):
    target_user_id = HiddenField()
    change_type = HiddenField(default="UpdateImage")
    image = FileField("Upload Image",validators=[FileRequired(),FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Change Image")

class ResetPasswordForm(FlaskForm):
    target_user_id = HiddenField()
