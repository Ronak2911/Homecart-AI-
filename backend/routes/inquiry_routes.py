from flask import Blueprint, render_template, session, request
from ..models.inquiry_model import get_inquiries_for_user

inquiry_bp = Blueprint("inquiry", __name__)

@inquiry_bp.route("/inquiries")
def inquiry_list():

    # 🔒 AUTH CHECK
    if "user_id" not in session:
        return "Unauthorized", 401

    user = {
        "_id": session["user_id"],
        "role": session.get("role"),
        "name": session.get("name")
    }

    # -------- FILTER INPUT --------
    filters = {
        "city": request.args.get("city"),
        "status": request.args.get("status"),
        "type": request.args.get("type"),
        "sort": request.args.get("sort")
    }

    # -------- FETCH INQUIRIES --------
    inquiries = get_inquiries_for_user(user)

    # ✅ Convert Mongo ObjectId → string
    for i in inquiries:
        i["_id"] = str(i["_id"])

        # ✅ Ensure requirements exists
        if "requirements" not in i or not isinstance(i["requirements"], dict):
            i["requirements"] = {}

        # ✅ Ensure location exists
        if "location" not in i["requirements"] or not isinstance(i["requirements"]["location"], dict):
            i["requirements"]["location"] = {}

        # ✅ Default values (prevents Jinja crashes)
        i["requirements"].setdefault("budgetmin", 0)
        i["requirements"].setdefault("budgetmax", 0)
        i["requirements"].setdefault("propertytype", "")
        i["requirements"]["location"].setdefault("city", "")
        i["requirements"]["location"].setdefault("area", "")
        

    # -------- APPLY FILTERS --------

    # ✅ City filter (case-insensitive)
    if filters["city"]:
        inquiries = [
            i for i in inquiries
            if i.get("requirements", {})
                 .get("location", {})
                 .get("city", "")
                 .lower() == filters["city"].lower()
        ]

    # ✅ Status filter
    if filters["status"]:
        inquiries = [
            i for i in inquiries
            if i.get("inquirystatus", "")
                 .lower() == filters["status"].lower()
        ]

    # ✅ Type filter
    if filters["type"]:
        inquiries = [
            i for i in inquiries
            if i.get("requirements", {})
                 .get("propertytype", "")
                 .lower() == filters["type"].lower()
        ]

    # -------- SORTING (SAFE) --------

    if filters["sort"] == "budget_low":
        inquiries.sort(
            key=lambda x: x.get("requirements", {}).get("budgetmin") or 0
        )

    elif filters["sort"] == "budget_high":
        inquiries.sort(
            key=lambda x: x.get("requirements", {}).get("budgetmax") or 0,
            reverse=True
        )

    elif filters["sort"] == "newest":
        inquiries.sort(
            key=lambda x: x.get("created_at") or 0,
            reverse=True
        )

    return render_template(
        "inquiry/inquiry_list.html",
        inquiries=inquiries,
        user=user
    )

