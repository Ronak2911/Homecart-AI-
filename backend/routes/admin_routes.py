from flask import Blueprint, render_template
from ..models.customer_model import *
from ..middleware.auth_middleware import auth_required
from ..middleware.role_middleware import role_required

admin_bp = Blueprint("admin", __name__)





@admin_bp.route("/customers")
@auth_required
@role_required(["admin", "staff"])
def customers():
    customers = show_customers()
    return render_template("customer/customer_list.html", customers=customers)





@admin_bp.route("/users")
@auth_required
@role_required(["admin", "staff"])
def users():
    return render_template("users/user_list.html")




