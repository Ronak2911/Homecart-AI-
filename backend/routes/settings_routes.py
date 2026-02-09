from flask import Blueprint, request, jsonify, render_template, session
from ..database.collections import get_users_collection
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash
from ..middleware.auth_middleware import auth_required
from ..middleware.role_middleware import role_required
settings_bp = Blueprint("settings", __name__)
@settings_bp.route("/profile")
@auth_required
def profile():
    user_id = session.get("user_id")

    print("User Profile:", user_id)

    if not user_id:
        return "Unauthorized", 401

    user = get_users_collection().find_one({
        "_id": ObjectId(user_id)
    })

    return render_template("settings/profile.html", user=user)

@settings_bp.route("/change-password", methods=["GET", "POST"])
@auth_required
def change_password():

    user_id = session.get("user_id")

    if not user_id:
        return "Unauthorized", 401

    users = get_users_collection()

    user = users.find_one({"_id": ObjectId(user_id)})

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # ✅ Check old password
        if not check_password_hash(user["password"], old_password):
            return render_template("settings/change_password.html",
                                   error="Current password is incorrect")

        # ✅ Match new password
        if new_password != confirm_password:
            return render_template("settings/change_password.html",
                                   error="New passwords do not match")

        # ✅ Password length validation
        if len(new_password) < 6:
            return render_template("settings/change_password.html",
                                   error="Password must be at least 6 characters")

        # ✅ Hash new password
        hashed_password = generate_password_hash(new_password)

        # ✅ Update in MongoDB
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )

        return render_template("settings/change_password.html",
                               success="Password updated successfully")

    return render_template("settings/change_password.html")