from flask import Blueprint, session, redirect, url_for, request, render_template, jsonify
import flask_login
import helper_functions

from forms.AddToCartForm import AddToCartForm
from forms.UpdateQtyForm import UpdateQtyForm

from serializer import non_timed_serializer
from itsdangerous import BadSignature
import secrets

import stripe

from database_models.UserDBModel import *
from database_models.CartDBModel import *
from database_models.OrderDBModel import *

blueprint = Blueprint("order", __name__, template_folder="templates")

@blueprint.route("/admin/orders", defaults={'status':None})
@blueprint.route("/admin/orders/<status>/")
@flask_login.login_required
@helper_functions.admin_required
def admin_orders(status):
    if status == "ALL":
        status = None
    if status:
        orders = Order.query.filter_by(status=status.upper()).all()
    else:
        orders = Order.query.all()
        status = "all"
    return render_template("orders/admin_orders_all.html", orders=orders, status=status.upper())


@blueprint.route("/admin/orders/complete-order", methods=["GET","POST"])
@flask_login.login_required
@helper_functions.admin_required
def complete_order():
    id = request.form.get("order-id")
    order = Order.query.filter_by(id=id).first()
    if not order:
        return jsonify(success=0, msg="Error! Order not found")
    for item in order.order_items:
        item.fulfilled = True
        db.session.commit()
    order.status = "COMPLETED"
    db.session.commit()
    return jsonify(success=1, msg="Success! Order completed")

@blueprint.route("/admin/orders/order/<id>")
@flask_login.login_required
@helper_functions.admin_required
def admin_order_indiv(id):
    order = Order.query.filter_by(id=id).first()
    print(order.order_items[0].fulfilled)
    return render_template("orders/admin_order_indiv.html", order=order, prev=request.args.get("prev"))

@blueprint.route("/admin/orders/order/fulfill", methods=["POST"])
@flask_login.login_required
@helper_functions.admin_required
def fulfill_item():
    id = request.form.get("item-id")
    print(id)
    item = Order_Item.query.filter_by(id=id).first()
    if not item:
        return jsonify(success=0, msg="Error! Item not found")

    item.fulfilled = bool(request.form.get("fulfilled"))
    db.session.commit()

    order = item.orders
    if all((i.fulfilled for i in order.order_items)):
        order.status = "FULFILLED"
        db.session.commit()
    elif order.status == "FULFILLED":
        order.status = "PAID"
        db.session.commit()


    return jsonify(success=1, msg="Success! Item Fulfilled", status=order.status)


@blueprint.route("/user/orders", defaults={'status':None})
@blueprint.route("/user/orders/<status>/")
@flask_login.login_required
def view_orders(status):
    if status == "ALL":
        status = None
    if status:
        orders = [order for order in flask_login.current_user.order if order.status == "COMPLETED"]
    else:
        orders = [order for order in flask_login.current_user.order if order.status != "COMPLETED"]
        status = "all"
    print(orders)
    print(status)
    return render_template("orders/user_orders_all.html", orders=orders, status=status.upper())


@blueprint.route("/user/orders/order/<id>")
@flask_login.login_required
def user_order_indiv(id):
    order = Order.query.filter_by(id=id).first()
    print(order.order_items[0].fulfilled)
    return render_template("orders/user_order_indiv.html", order=order, prev=request.args.get("prev"))
