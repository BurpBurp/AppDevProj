from flask_wtf import FlaskForm
from werkzeug.datastructures import FileStorage
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, IntegerField, DecimalField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, StopValidation
from forms.CustomValidators import MultiFileAllowed
from flask_wtf.file import FileRequired, FileAllowed

class AddItemForm(FlaskForm):
    name = StringField("Item Name",validators=[DataRequired("Please enter name of item")])
    quantity = IntegerField("Quantity",validators=[DataRequired("Please enter number of items to add"), NumberRange(min=0, message="Quantity cannot be less than 0")])
    price = DecimalField("Price of Item",places=2, validators=[DataRequired("Please enter price of item"), NumberRange(min=0, message="Rich man FOC?")])
    image = MultipleFileField("Picture of Item", validators=[MultiFileAllowed(["jpg", "png", "jpeg", "jfif"],message=".jpg, .png, .jfif or .jpeg File Required")])
    description = StringField("Description of Item", validators=[DataRequired("Please enter description of item")])
    submit = SubmitField("Add Item")

class UpdateItemForm(FlaskForm):
    name = StringField("Item Name",validators=[DataRequired()])
    quantity = IntegerField("Quantity",validators=[DataRequired(), NumberRange(min=0, message="Quantity cannot be less than 0")])
    price = DecimalField("Price of Item", validators=[DataRequired(), NumberRange(min=0, message="Rich man FOC?")])
    image = MultipleFileField("Change Image", validators=[])
    description = StringField("Description of Item", validators=[DataRequired("Please enter description of item")])
    submit = SubmitField("Update Item")


