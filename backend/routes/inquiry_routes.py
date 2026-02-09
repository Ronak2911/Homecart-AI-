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
        "role": session["role"],
        "name": session["name"]
    }

    # -------- FILTER INPUT --------
    filters = {
        "city": request.args.get("city"),
        "status": request.args.get("status"),
        "type": request.args.get("type"),
        "sort": request.args.get("sort")
    }

    inquiries = get_inquiries_for_user(user)

    # -------- APPLY FILTERS (NO DB REQUERY) --------
    if filters["city"]:
        inquiries = [
            i for i in inquiries
            if i.get("requirements", {}).get("location", {}).get("city") == filters["city"]
        ]

    if filters["status"]:
        inquiries = [
            i for i in inquiries
            if i.get("inquirystatus") == filters["status"]
        ]

    if filters["type"]:
        inquiries = [
            i for i in inquiries
            if i.get("requirements", {}).get("propertytype") == filters["type"]
        ]

    # -------- SORTING --------
    if filters["sort"] == "budget_low":
        inquiries.sort(
            key=lambda x: x.get("requirements", {}).get("budgetmin", 0)
        )

    if filters["sort"] == "budget_high":
        inquiries.sort(
            key=lambda x: x.get("requirements", {}).get("budgetmax", 0),
            reverse=True
        )

    if filters["sort"] == "newest":
        inquiries.reverse()

    return render_template(
        "inquiry/inquiry_list.html",
        inquiries=inquiries,
        user=user
    )
