from flask import Blueprint, render_template, request, redirect, url_for, flash,make_response
from werkzeug.security import generate_password_hash, check_password_hash

from ..database.collections import get_users_collection
from ..middleware.auth_middleware import auth_required
from ..middleware.role_middleware import role_required

auth_bp = Blueprint("auth", __name__)


# ================================
# REGISTER (GET + POST)
# ================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        users_collection = get_users_collection()   # ✅ INSIDE FUNCTION

        name = request.form.get("name")
        role = request.form.get("role")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation
        if not name or not role or not email or not password:
            flash("All fields are required")
            return redirect(url_for("auth.register"))

        # Check existing user
        if users_collection.find_one({"email": email}):
            flash("Email already exists")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        users_collection.insert_one({
            "name": name,
            "role": role,
            "email": email,
            "password": hashed_password,
            "is_active": True
        })

        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ================================
# LOGIN PAGE
# ================================
from flask import session
from ..utils.jwt_helper import generate_token


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        users_collection = get_users_collection()

        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({"email": email})

        if not user:
            flash("Invalid Email or Password")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user["password"], password):
            flash("Invalid Email or Password")
            return redirect(url_for("auth.login"))

        # ======================
        # CREATE SESSION (WEB)
        # ======================
        session["user_id"] = str(user["_id"])
        session["role"] = user["role"]
        session["name"] = user["name"]

        # ======================
        # CREATE JWT (API)
        # ======================
        token = generate_token(user["_id"], user["role"])

        # Store token in session (optional)
        session["token"] = token

        flash("Login successful")
        if session["role"] == "staff":
            return redirect(url_for("dashboard.dashboard"))
        elif session["role"] == "admin":
            return redirect(url_for("dashboard.dashboard"))
        else:
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")




@auth_bp.route("/logout")
def logout():

    # Remove session data
    session.clear()

    # Also remove session cookie
    response = make_response(redirect(url_for("auth.login")))
    response.delete_cookie("session")

    flash("Logged out successfully")

    # Disable caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
