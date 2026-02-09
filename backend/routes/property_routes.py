from flask import Blueprint, render_template, request, session, redirect, url_for
from bson.objectid import ObjectId

from ..models.property_model import get_properties, delete_property
from ..models.property_model import (
    get_properties_collection,
    update_property,
    add_property
)

property_bp = Blueprint("property", __name__)


@property_bp.route("/properties")
def property_list():

    # ---------- AUTH ----------
    if "user_id" not in session:
        return "Unauthorized", 401

    role = session.get("role")   # admin | staff

    # ---------- GET DATA ----------
    properties = get_properties()

    # ---------- FILTERS ----------
    city = request.args.get("city")
    ptype = request.args.get("type")
    status = request.args.get("status")
    sort = request.args.get("sort")

    if city:
        properties = [
            p for p in properties
            if p.get("location", {}).get("city") == city
        ]

    if ptype:
        properties = [
            p for p in properties
            if p.get("propertytype") == ptype
        ]

    if status:
        properties = [
            p for p in properties
            if p.get("status") == status
        ]

    # ---------- SORT ----------
    if sort == "price_low":
        properties.sort(key=lambda x: x.get("price", 0))

    if sort == "price_high":
        properties.sort(key=lambda x: x.get("price", 0), reverse=True)

    return render_template(
        "property/property_list.html",
        properties=properties,
        role=role
    )


@property_bp.route("/property/delete/<pid>")
def property_delete(pid):

    if session.get("role") != "admin":
        return "Forbidden", 403

    delete_property(pid)
    return redirect(url_for("property.property_list"))

@property_bp.route("/property/add", methods=["GET", "POST"])
def property_add():

    # 🔒 ADMIN ONLY
    if session.get("role") != "admin":
        return "Forbidden", 403

    if request.method == "POST":

        data = {
            "title": request.form.get("title"),
            "propertytype": request.form.get("propertytype"),
            "bhk": request.form.get("bhk"),
            "sizesqft": request.form.get("sizesqft"),
            "budgetrange": request.form.get("budgetrange"),
            "price": request.form.get("price"),
            "status": request.form.get("status"),

            "location": {
                "city": request.form.get("city"),
                "area": request.form.get("area"),
                "pincode": request.form.get("pincode"),
                "address": request.form.get("address"),
                "maplink": request.form.get("maplink"),
            },

            "amenities": request.form.get("amenities"),
            "description": request.form.get("description"),

            "media": {
                "images": [],   # images handled later
                "video": ""
            },

            "createdby": ObjectId(session["user_id"])
        }

        add_property(data)
        return redirect(url_for("property.property_list"))

    return render_template("property/property_add.html")


@property_bp.route("/property/edit/<pid>", methods=["GET", "POST"])
def property_edit(pid):

    # 🔒 ADMIN ONLY
    if session.get("role") != "admin":
        return "Forbidden", 403

    properties_col = get_properties_collection()
    property_data = properties_col.find_one({"_id": ObjectId(pid)})

    if not property_data:
        return "Property not found", 404

    # ---------- SAVE ----------
    if request.method == "POST":

        data = {
            "title": request.form.get("title"),
            "propertytype": request.form.get("propertytype"),
            "bhk": request.form.get("bhk"),
            "sizesqft": request.form.get("sizesqft"),
            "price": request.form.get("price"),
            "budgetrange": request.form.get("budgetrange"),
            "status": request.form.get("status"),

            "location": {
                "city": request.form.get("city"),
                "area": request.form.get("area"),
                "pincode": request.form.get("pincode"),
                "address": request.form.get("address"),
                "maplink": request.form.get("maplink"),
            },

            "amenities": request.form.get("amenities"),
            "description": request.form.get("description"),
        }

        update_property(pid, data)
        return redirect(url_for("property.property_list"))

    # ---------- NORMALIZE FOR TEMPLATE ----------
    property_data["_id"] = str(property_data["_id"])
    property_data.setdefault("location", {})
    property_data.setdefault("media", {"images": [], "video": ""})

    return render_template(
        "property/property_edit.html",
        property=property_data
    )
# Route to View a Single Property Detail
@property_bp.route("/property/view/<pid>")
def property_detail(pid):

    # ---------- AUTH CHECK ----------
    if "user_id" not in session:
        return redirect(url_for('auth.login'))

    # ---------- GET DATA ----------
    properties_col = get_properties_collection()
    property_data = properties_col.find_one({"_id": ObjectId(pid)})

    if not property_data:
        return "Property not found", 404

    # ---------- RENDER ----------
    return render_template("property/property_detail.html", p=property_data)