from flask import Blueprint, session, render_template, request, redirect, url_for
from database_models.CartDBModel import *
from forms.AddItemForm import *
import flask_login
import stripe
import stripe.error
from forms.CouponForm import AddCoupon
import helper_functions

blueprint = Blueprint("coupon", __name__, template_folder="templates")

@blueprint.route("/coupon/add", methods=["POST","GET"])
@flask_login.login_required
@helper_functions.admin_required
def add_coupon():
    form = AddCoupon()
    if request.method == "GET":
        return render_template("coupon/add_coupon.html", form=form)
    if request.method == "POST":
        print(form.codes.data)
        if form.validate_on_submit():
            if form.coupon_type.data == "percentage":
                if form.coupon_discount.data > 100:
                    form.coupon_discount.errors.append("Value must be less than 100")
                    return render_template("coupon/add_coupon.html", form=form)

                coupon = stripe.Coupon.create(percent_off=form.coupon_discount.data,duration="forever",name=form.name.data)
            else:
                coupon = stripe.Coupon.create(amount_off=form.coupon_discount.data * 100,duration="forever",name=form.name.data,currency="SGD")
            codes_in_use = []

            for code in form.codes.data:
                retrived_code = stripe.PromotionCode.list(code=code,active=True)
                print(retrived_code)
                if len(retrived_code["data"]) > 0:
                    codes_in_use.append(code)

            if len(codes_in_use) > 0:
                for code in codes_in_use:
                    helper_functions.flash_error(f"Code {code} in use")
                stripe.Coupon.delete(coupon["id"])
                return render_template("coupon/add_coupon.html", form=form)
            for code in form.codes.data:
                stripe.PromotionCode.create(coupon=coupon["id"], code=code)
            return redirect(url_for("coupon.view_coupons"))
        return render_template("coupon/add_coupon.html", form=form)


@blueprint.route("/coupon", methods=["GET"])
@flask_login.login_required
@helper_functions.admin_required
def view_coupons():
    coupons = stripe.Coupon.list()["data"]
    print(coupons)
    return render_template("coupon/view_coupons.html", couponList= coupons)

@blueprint.route("/coupon/delete/<id>/", methods=["GET"])
@blueprint.route("/coupon/delete/<id>", methods=["GET"])
@flask_login.login_required
@helper_functions.admin_required
def delete_coupons(id):
    try:
        stripe.Coupon.retrieve(id)
        stripe.Coupon.delete(id)
        helper_functions.flash_success("Deleted Coupon")
    except stripe.error.StripeError:
        helper_functions.flash_error("Coupon Not FOund")
    return redirect(url_for("coupon.view_coupons"))


@blueprint.route("/coupon/edit/<id>/", methods=["GET","POST"])
@blueprint.route("/coupon/edit/<id>", methods=["GET","POST"])
@flask_login.login_required
@helper_functions.admin_required
def edit_coupon(id):
    try:
        coupon = stripe.Coupon.retrieve(id)
        print(coupon)
    except stripe.error.StripeError:
        helper_functions.flash_error("Coupon Not FOund")
        return redirect(url_for("coupon.view_coupons"))
    if request.method == "GET":
        return "FOUND COUPON"

