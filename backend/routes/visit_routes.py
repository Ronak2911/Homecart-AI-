from flask import Blueprint, render_template, request, redirect, url_for, session

from ..middleware.auth_middleware import auth_required
from ..middleware.role_middleware import role_required

from ..models.visit_model import (
    get_visits_with_filters,
    get_staff_list,
    get_property_list,
    get_staff_by_city,
    assign_staff_to_visit
)


visit_bp = Blueprint("visit", __name__)


# ==========================================
# VISIT LIST PAGE
# ==========================================

@visit_bp.route("/visits")
@auth_required
def visits_page():

    # Build user dict from session
    user = {
        "_id": session.get("user_id"),
        "role": session.get("role"),
        "name": session.get("name")
    }

    # Filters
    filters = {
        "city": request.args.get("city"),
        "staffid": request.args.get("staffid"),
        "status": request.args.get("status"),
        "propertyid": request.args.get("propertyid"),
        "visitdate": request.args.get("visitdate")
    }

    # Get visits
    visits = get_visits_with_filters(user, filters)

    # Get dropdown data
    staff = get_staff_list()

    properties = get_property_list()

    return render_template(
        "visits/visit_list.html",
        visits=visits,
        staff=staff,
        properties=properties,
        user=user
    )


# ==========================================
# ASSIGN STAFF PAGE + ACTION
# ==========================================

@visit_bp.route("/visit/assign/<vid>", methods=["GET", "POST"])
@auth_required
@role_required("admin")

def assign_visit(vid):

    # POST → assign staff
    if request.method == "POST":

        staff_id = request.form.get("staff_id")

        if staff_id:
            assign_staff_to_visit(vid, staff_id)

        return redirect(url_for("visit.visits_page"))


    # GET → show assign page
    city = request.args.get("city")

    staff_list = get_staff_by_city(city) if city else get_staff_list()

    return render_template(
        "visits/assign_staff.html",
        visit_id=vid,
        staff_list=staff_list
    )

from bson import ObjectId
from ..database.collections import get_visits_collection


# ==========================================
# UPDATE VISIT STATUS ✅ FIXED
# ==========================================

from bson import ObjectId
from ..database.collections import get_visits_collection, get_inquiries_collection

@visit_bp.route("/visit/update-status/<vid>", methods=["POST"])
@auth_required
def update_visit_status(vid):

    new_status = request.form.get("status")

    visits_col = get_visits_collection()
    inquiries_col = get_inquiries_collection()

    visit = visits_col.find_one({"_id": ObjectId(vid)})

    if not visit:
        return redirect(url_for("visit.visits_page"))

    # ✅ Update visit status
    visits_col.update_one(
        {"_id": ObjectId(vid)},
        {"$set": {"status": new_status}}
    )

    inquiry_id = visit.get("inquiryid")

    # ✅ If visit confirmed → inquiry becomes Visited
    if new_status == "Confirmed" and inquiry_id:
        inquiries_col.update_one(
            {"_id": inquiry_id},
            {"$set": {"Status": "Visited"}}
        )

    # ✅ If visit changed back to Pending → inquiry back to Visit
    elif new_status == "Pending" and inquiry_id:
        inquiries_col.update_one(
            {"_id": inquiry_id},
            {"$set": {"Status": "Visit"}}
        )

    return redirect(url_for("visit.visits_page"))