from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class AddToCartForm(FlaskForm):
    quantity = IntegerField("Quantity",validators=[DataRequired(),NumberRange(min=1)],default=1)
    submit = SubmitField("Log In")
