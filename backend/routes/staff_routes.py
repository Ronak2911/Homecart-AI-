
from datetime import datetime
from ..middleware.auth_middleware import auth_required
from ..middleware.role_middleware import role_required
from ..database.collections import get_users_collection

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from bson import ObjectId
staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/staff")
@auth_required  
@role_required(["admin"])
def staff_list():
    users_collection = get_users_collection().find()
    return render_template("staff/staff_list.html",users=users_collection)

@staff_bp.route("/staff/add", methods=['GET', 'POST'])
@auth_required  
@role_required(["admin"])
def add_staff():


    if request.method == 'POST':
          

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        city = request.form['city']
        password = request.form['password']

        users = get_users_collection()

        # check email exists
        if users.find_one({"email": email}):
            flash("Email already exists", "danger")
            return redirect(url_for('staff.add_staff'))

        staff_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "role": role,
            "city": city,
            "password": generate_password_hash(password),
            "created_at": datetime.now(),
            "status": "active"
        }

        users.insert_one(staff_data)

        flash("Staff added successfully", "success")
        return redirect(url_for('staff.staff_list'))
    return render_template("staff/add_staff.html")

@staff_bp.route("/staff/edit/<user_id>", methods=['GET', 'POST'])
@auth_required
@role_required(["admin"])
def edit_staff(user_id):

    users = get_users_collection()

    try:
        user_obj_id = ObjectId(user_id)
    except:
        flash("Invalid staff ID", "danger")
        return redirect(url_for('staff.staff_list'))

    user = users.find_one({"_id": user_obj_id})

    if not user:
        flash("Staff not found", "danger")
        return redirect(url_for('staff.staff_list'))

    if request.method == 'POST':

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()
        role = request.form.get("role", "").strip()
        status = request.form.get("status", "").strip()

        # Basic validation
        if not name or not email:
            flash("Name and Email are required", "danger")
            return redirect(request.url)

        update_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "city": city,
            "role": role,
            "status": status
        }

        users.update_one(
            {"_id": user_obj_id},
            {"$set": update_data}
        )

        flash("Staff updated successfully", "success")
        return redirect(url_for('staff.staff_list'))

    # Convert ObjectId for template
    user["_id"] = str(user["_id"])

    return render_template("staff/edit_staff.html", user=user)

@staff_bp.route("/staff/delete/<staff_id>")
def delete_staff(staff_id):
    users = get_users_collection()
    
    # Delete staff
    users.delete_one({"_id": ObjectId(staff_id)})

    return redirect(url_for("staff.staff_list"))