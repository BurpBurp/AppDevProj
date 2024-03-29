from flask import Blueprint, session, render_template, request, redirect, url_for
from database_models.CartDBModel import *
from werkzeug.utils import secure_filename
import secrets
import os
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
        # for file in form.image.data:
        #     print(file)
        #     file_name = f"{secrets.token_urlsafe(8)}{os.path.splitext(secure_filename(file.filename))[1]}"
        #     print(file_name)
        #     path = os.path.join("static", "items", file_name)
        #     print(path)
        #     file.save(path)

        if form.validate_on_submit():
            files_filenames = []
            for file in form.image.data:
                file_name = f"{secrets.token_urlsafe(8)}{os.path.splitext(secure_filename(file.filename))[1]}"
                files_filenames.append(file_name)
                path = os.path.join("static", "items", file_name)
                file.save(path)
                print(path)


            item = Item(name=form.name.data,price=form.price.data,quantity=form.quantity.data,description=form.description.data,images=files_filenames)
            db.session.add(item)
            db.session.commit()
            print(item.images)
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
        form.description.data = item.description
        return render_template("inventory/UpdateForm.html", form=form, item=item)
    elif request.method == "POST":
        if form.validate_on_submit():

            print(request.files)
            if "image" in request.files:
                print("Dealing With Files")
                files_filenames = []
                print(form.image.data)
                for file in form.image.data:
                    if file.filename == "":
                        break

                    if os.path.splitext(secure_filename(file.filename))[1] in (".png", ".jpg", ".jpeg", ".jfif"):
                        file_name = f"{secrets.token_urlsafe(8)}{os.path.splitext(secure_filename(file.filename))[1]}"
                        files_filenames.append(file_name)
                        path = os.path.join("static", "items", file_name)
                        file.save(path)
                        print(path)
                    else:
                        helper_functions.flash_error(".jpg, .png, .jfif or .jpeg File Required")
                        return render_template("inventory/UpdateForm.html", form=form, item=item)
                else:
                    print("Editing File Names")
                    item.images = files_filenames



            item.name = request.form['name']
            item.quantity = request.form['quantity']
            item.price = request.form['price']
            item.description = request.form['description']
            db.session.commit()
            return redirect(url_for("InventoryManagement.ManageInventory"))
    print("DID NOT VALIDATE")
    print(form.errors)
    return render_template("inventory/UpdateForm.html", form=form, item=item)

@blueprint.route("/ManageInventory/DeleteItem/<id>/", methods=["GET"])
@flask_login.login_required
@helper_functions.admin_required
def DeleteInventory(id):
    item = Item.query.filter_by(id=id).first()
    if item:
        cart_items = Cart_Item.query.all()
        for cart_item in cart_items:
            if cart_item.item.id == item.id:
                db.session.delete(cart_item)
                db.session.commit()
        db.session.delete(item)
        db.session.commit()
        message = f"The item {item.name} has been deleted from the database."
        helper_functions.flash_success(message)
        return redirect(url_for("InventoryManagement.ManageInventory"))

