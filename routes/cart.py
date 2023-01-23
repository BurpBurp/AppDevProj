from flask import Blueprint, session, redirect, url_for, request, render_template
import flask_login
import helper_functions
from forms.AddToCartForm import AddToCartForm
from database_models.UserDBModel import *
from database_models.CartDBModel import *

blueprint = Blueprint("cart", __name__, template_folder="templates")

@blueprint.route("/readcart")
@flask_login.login_required
def read_cart():
    cart = flask_login.current_user.cart.cart_items
    return render_template("Checkout/readcart.html",cart=cart)

@blueprint.route("/cart/add_to_cart/<id>", methods=["GET","POST"])
@flask_login.login_required
def add_to_cart(id):
    form = AddToCartForm()
    item = Item.query.filter_by(id=id).first()
    if not item:
        helper_functions.flash_error("Item Does Not Exist")
        return redirect(url_for("index.index"))
    if request.method == "POST":
        if cart_item := Cart_Item.query.filter_by(Item_id=item.id).first():
            cart_item.quantity += form.quantity.data
            db.session.commit()
        else:
            cart_item = Cart_Item(cart=flask_login.current_user.cart,item=item,quantity=form.quantity.data)
            db.session.add(cart_item)
            db.session.commit()

        helper_functions.flash_success(f"Added {item.name} to cart")
        return redirect(url_for("cart.read_cart"))
    return render_template("Checkout/addtocart.html",item=item,form=form)
    pass

@blueprint.route("/cart/delete_item/<id>")
@flask_login.login_required
def delete_item(id):
    item = Cart_Item.query.filter_by(id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for("cart.read_cart"))
    helper_functions.flash_error("Item Does Not Exist")
    return redirect(url_for("cart.read_cart"))

@blueprint.route("/deletecart")
@flask_login.login_required
def deletecart():
    cart = flask_login.current_user.cart
    for item in cart.cart_items:
        db.session.delete(item)
        db.session.commit()
    db.session.delete(cart)
    db.session.commit()
    create_cart(flask_login.current_user)
    return redirect(url_for("cart.read_cart"))
