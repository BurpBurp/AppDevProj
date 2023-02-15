# Darwin's Stuff
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, BooleanField, DecimalField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Regexp

class AddCoupon(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    coupon_type = SelectField("Type",choices=[('amount',"Amount Off"),("percentage","Percentage")])
    coupon_discount = DecimalField("Amount Off",validators=[DataRequired(),NumberRange(min=0.01, message="Value must be greater than 0.01")], places=2)
    codes = FieldList(StringField('Code', validators=[DataRequired(),Regexp("^[A-Za-z0-9]+$")]), min_entries=1)

class EditCoupon(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    codes = FieldList(StringField('Code', validators=[DataRequired(),Regexp("^[A-Za-z0-9]+$")]), min_entries=0)
