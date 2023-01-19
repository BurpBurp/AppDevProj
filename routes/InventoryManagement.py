from flask import Blueprint, session, render_template, request, redirect, url_for
from database_models.CartDBModel import *
from forms.AddItemForm import *
import flask_login
import helper_functions
blueprint = Blueprint("InventoryManagement", __name__, template_folder="templates")

@blueprint.route("/ManageInventory")
@flask_login.login_required
@helper_functions.admin_required
def ManageInventory():
    item = Item.query.all()
    return render_template("inventory/InventoryManagement.html", itemsList= item)

@blueprint.route("/ManageInventory/AddItem", methods = ["GET", "POST"])
@flask_login.login_required
@helper_functions.admin_required
def AddInventory():
    form = AddItemForm()
    if request.method == "POST":
        if form.validate_on_submit():
            item = Item(name=form.name.data,price=form.price.data,quantity=form.quantity.data)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for("InventoryManagement.ManageInventory"))
    return render_template("inventory/ItemForm.html", form = form)

@blueprint.route("/ManageInventory/UpdateItem/<id>/", methods = ["GET", "POST"])
@flask_login.login_required
@helper_functions.admin_required
def UpdateInventory(id):
    form = UpdateItemForm()
    item = Item.query.filter_by(id=id).first()
    if not item:
            helper_functions.flash_error(f"Item with \"{id}\" not in database")
            return redirect(url_for("InventoryManagement.ManageInventory"))
    if request.method == "GET":
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.price.data = item.price
        return render_template("inventory/UpdateForm.html", form=form, item=item)
    elif request.method == "POST":
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.price = request.form['price']
        return redirect(url_for("InventoryManagement.ManageInventory"))

@blueprint.route("/ManageInventory/DeleteItem/<id>/", methods=["GET"])
@flask_login.login_required
@helper_functions.admin_required
def DeleteInventory(id):
    item = Item.query.filter_by(id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        message = f"The item {item.name} has been deleted from the database."
        helper_functions.flash_success(message)
        return redirect(url_for("InventoryManagement.ManageInventory"))
