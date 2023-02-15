from flask import Blueprint, session, redirect, url_for, request, render_template,jsonify
import flask_login
import helper_functions

from forms.AddToCartForm import AddToCartForm
from forms.UpdateQtyForm import UpdateQtyForm

from serializer import non_timed_serializer
from itsdangerous import BadSignature
import secrets

import stripe
import stripe.error

from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database_models.OrderDBModel import *

blueprint = Blueprint("cart", __name__, template_folder="templates")

@blueprint.route("/readcart")
@flask_login.login_required
def read_cart():
    cart = flask_login.current_user.cart.cart_items
    total = 0
    for i in cart:
        total += (i.item.price*i.quantity)
    print(total)
    return render_template("Checkout/readcart.html",cart=cart,total=total)

@blueprint.route("/cart/add_to_cart/<id>/", methods=["GET","POST"])
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


@blueprint.route("/cart/add_to_cart_ajax", methods=["GET","POST"])
def add_to_cart_ajax():
    id = request.form.get("id")
    if not flask_login.current_user.is_authenticated:
        return jsonify(success=0, redir=url_for("crud.login",next=[request.form.get("prev")], custom_flash=["Please Login To Add To Cart"],_external=True))
    form = AddToCartForm()
    item = Item.query.filter_by(id=id).first()
    if not item:
        helper_functions.flash_error("Item Does Not Exist")
        return redirect(url_for("index.index"))
    if request.method == "POST":
        if cart_item := Cart_Item.query.filter_by(Item_id=item.id,cart_id=flask_login.current_user.cart.id).first():
            cart_item.quantity += form.quantity.data
            db.session.commit()
        else:
            cart_item = Cart_Item(cart=flask_login.current_user.cart,item=item,quantity=form.quantity.data)
            print(cart_item)
            db.session.add(cart_item)
            db.session.commit()
        print(len(flask_login.current_user.cart.cart_items))
        return jsonify(success=1, msg=f"Added {item.name} to cart",cart_length=len(flask_login.current_user.cart.cart_items))


@blueprint.route("/cart/update/<id>/", methods=["GET","POST"])
@flask_login.login_required
def update_qty(id):
    form = UpdateQtyForm()
    item = Cart_Item.query.filter_by(id=id,cart=flask_login.current_user.cart).first()
    print(request.method)
    if request.method == "POST":
        item.quantity = int(form.quantity.data)
        db.session.commit()
        return redirect(url_for("cart.read_cart"))
    helper_functions.flash_error("Update Failed")
    return redirect(url_for("cart.read_cart"))


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

@blueprint.route("/cart/change_quantity", methods=["POST"])
@flask_login.login_required
def update_quantity():
    cart = flask_login.current_user.cart.cart_items
    total = 0
    id = request.form.get("cart-item-id")
    quantity = request.form.get("quantity")
    print(quantity)
    if item := Cart_Item.query.filter_by(id=id).first():
        print(item.quantity)
        item.quantity = quantity
        print(item.quantity)
        db.session.commit()
        for i in cart:
            total += (i.item.price*i.quantity)
        print(total)
        print(item.quantity * item.item.price)
        return jsonify(success=1, item_total = item.quantity * item.item.price, total=total)
    return jsonify(success=0)

@blueprint.route("/cart/checkout")
@flask_login.login_required
def checkout():
    cart = flask_login.current_user.cart.cart_items
    token = non_timed_serializer.dumps({"id":flask_login.current_user.id,"token":secrets.token_urlsafe()},salt="Checkout")
    if len(cart) <= 0:
        return redirect(url_for("cart.readcart"))

    items = []
    for item in cart:
        line_item = {'price_data': {
                    'currency':'SGD',
                    'product_data':{
                        'name': item.item.name,
                        'description':item.item.description},
                    'unit_amount': int(item.item.price*100),
                    },
                    'quantity':item.quantity
                }
        items.append(line_item)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = items,
            success_url = f"http://127.0.0.1:5000/cart/checkout/success/{token}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url = url_for('cart.read_cart',_external=True),
            mode = 'payment',
            payment_method_types = ['card', 'paynow', 'grabpay'],
            customer_email=flask_login.current_user.email,
            allow_promotion_codes=True,
            metadata={"token":token}
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url)


@blueprint.route("/cart/checkout/success/<token>")
@flask_login.login_required
def checkout_success(token):
    try:
        payload = non_timed_serializer.loads(token, salt="Checkout")
    except BadSignature:
        return "Invalid Token"



    if not (order := Order.query.filter_by(token=payload.get("token")).first()):


        user = get_user_by_id(payload.get("id"))
        if not user:
            return "BAD USER"

        cart = user.cart
        if len(cart.cart_items) <= 0:
            helper_functions.flash_error("Order has no items")
            return redirect(url_for("order.view_orders"))

        discount = 0
        if checkout_id := request.args.get("session_id"):
            checkout_session = stripe.checkout.Session.retrieve(checkout_id)
            print(checkout_session)
            print(checkout_session["total_details"]["amount_discount"])
            discount = checkout_session["total_details"]["amount_discount"]/100

        order = Order(user=user,token=payload.get("token"),discount=discount)
        db.session.add(order)
        db.session.commit()
        total = 0
        for item in cart.cart_items:
            total += item.item.price * item.quantity
            order_item = Order_Item(orders=order,item=item.item,name=item.item.name,price=item.item.price,description=item.item.description,quantity=item.quantity,
                                    images=item.item.images,category=item.item.category)
            db.session.add(order_item)
            db.session.delete(item)
            db.session.commit()

        order.total = total

        #Delete Cart
        db.session.delete(cart)
        db.session.commit()
        create_cart(flask_login.current_user)

        helper_functions.flash_success("Success! Checked Out")
    print("ORDER")
    return render_template("orders/user_order_indiv.html", order=order, new=True)
