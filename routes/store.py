from flask import Blueprint, session, render_template, request, redirect, url_for
from database_models.CartDBModel import *
from forms.AddItemForm import *
import flask_login
import helper_functions

blueprint = Blueprint("Store", __name__, template_folder="templates")

@blueprint.route("/Store")
def displayitem():
    item = Item.query.all()
    return render_template("inventory/Store.html", itemsList= item)

@blueprint.route("/Store/item/<id>/")
def itempage(id):
    item = Item.query.filter_by(id=id).first()
    if item:
        return render_template("inventory/itempage.html", item=item)
    else:
        helper_functions.flash_error("Item does not exist")
        return redirect(url_for("Store.displayitem"))




