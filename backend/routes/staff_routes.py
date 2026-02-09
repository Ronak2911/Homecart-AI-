from ..middleware.auth_middleware import auth_required
from ..middleware.role_middleware import role_required
from ..database.collections import get_users_collection
from flask import Blueprint, render_template
staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/staff")
@auth_required  
@role_required(["admin"])
def staff_list():
    users_collection = get_users_collection().find()
    return render_template("staff/staff_list.html",users=users_collection)

