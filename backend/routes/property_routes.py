import os
from flask import Blueprint, render_template, request, session, redirect, url_for
from bson.objectid import ObjectId

from ..models.property_model import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "frontend/static/uploads"


property_bp = Blueprint("property", __name__)


from ..models.property_model import get_properties_filtered


@property_bp.route("/properties")
def property_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))


    # GET FILTER VALUES
    city = request.args.get("city")
    ptype = request.args.get("type")
    status = request.args.get("status")
    sort = request.args.get("sort")

    page = request.args.get("page", 1, type=int)
    per_page = 10


    # GET FILTERED DATA
    properties, total = get_properties_filtered(
        city=city,
        ptype=ptype,
        status=status,
        sort=sort,
        page=page,
        per_page=per_page
    )


    total_pages = (total + per_page - 1) // per_page


    # GET DISTINCT VALUES FOR DROPDOWNS
    collection = get_properties_collection()

    cities = collection.distinct("city")
    types = collection.distinct("type")
    statuses = collection.distinct("status")


    return render_template(
        "property/property_list.html",
        properties=properties,
        cities=cities,
        types=types,
        statuses=statuses,
        page=page,
        total_pages=total_pages
    )

@property_bp.route("/property/delete/<pid>")
def property_delete(pid):

    if session.get("role") != "admin":
        return "Forbidden", 403

    delete_property(pid)
    return redirect(url_for("property.property_list"))

@property_bp.route("/property/add", methods=["GET", "POST"])
def property_add():

    if session.get("role") != "admin":
        return "Forbidden", 403


    if request.method == "POST":

        data = {

            "name": request.form.get("name"),

            "type": request.form.get("type"),

            "status": request.form.get("status"),

            "BHK": request.form.get("BHK"),

            "sqft": request.form.get("sqft"),

            "price": int(request.form.get("price", 0)),

            "city": request.form.get("city"),

            "area": request.form.get("area"),

            "pincode": request.form.get("pincode"),

            "address": request.form.get("address"),

            "maplink": request.form.get("maplink"),

            "amenities": request.form.get("amenities"),

            "description": request.form.get("description"),

            "createdby": ObjectId(session["user_id"])
        }


        # IMAGE UPLOAD
        image = request.files.get("image")

        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(image.filename)

            filepath = os.path.join(UPLOAD_FOLDER, filename)

            image.save(filepath)

            data["media"] = filename


        add_property(data)

        return redirect(url_for("property.property_list"))


    return render_template("property/property_add.html")

@property_bp.route("/property/edit/<pid>", methods=["GET", "POST"])
def property_edit(pid):

    # 🔒 ADMIN ONLY
    if session.get("role") != "admin":
        return "Forbidden", 403


    properties_col = get_properties_collection()

    property_data = properties_col.find_one({
        "_id": ObjectId(pid)
    })


    if not property_data:
        return "Property not found", 404


    # ---------- SAVE ----------
    if request.method == "POST":

        data = {

            "name": request.form.get("name"),

            "type": request.form.get("type"),

            "status": request.form.get("status"),

            "BHK": request.form.get("BHK"),

            "sqft": request.form.get("sqft"),

            "price": int(request.form.get("price", 0)),

            "city": request.form.get("city"),

            "area": request.form.get("area"),

            "pincode": request.form.get("pincode"),

            "address": request.form.get("address"),

            "maplink": request.form.get("maplink"),

            "amenities": request.form.get("amenities"),

            "description": request.form.get("description"),
        }


        # ---------- IMAGE UPLOAD ----------
        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(image.filename)

            filepath = os.path.join(UPLOAD_FOLDER, filename)

            image.save(filepath)

            data["media"] = filename


        # ---------- UPDATE ----------
        properties_col.update_one(
            {"_id": ObjectId(pid)},
            {"$set": data}
        )


        return redirect(url_for("property.property_list"))



    # ---------- NORMALIZE ----------
    property_data["_id"] = str(property_data["_id"])

    property_data.setdefault("media", "")


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