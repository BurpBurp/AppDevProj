from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, IntegerField, DecimalField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

class AddItemForm(FlaskForm):
    name = StringField("Item Name",validators=[DataRequired()])
    quantity = IntegerField("Quantity",validators=[DataRequired(), NumberRange(min=0, message="Quantity cannot be less than 0")])
    price = DecimalField("Price of Item",places=2, validators=[DataRequired(), NumberRange(min=0, message="Rich man FOC?")])
    image = FileField("Picture of Item")
    category = StringField("Type of Item")
    submit = SubmitField("Add Item")

class UpdateItemForm(FlaskForm):
    name = StringField("Item Name",validators=[DataRequired()])
    quantity = IntegerField("Quantity",validators=[DataRequired(), NumberRange(min=0, message="Quantity cannot be less than 0")])
    price = DecimalField("Price of Item", validators=[DataRequired(), NumberRange(min=0, message="Rich man FOC?")])
    image = FileField("Picture of Item")
    category = StringField("Type of Item")
    submit = SubmitField("Update Item")
