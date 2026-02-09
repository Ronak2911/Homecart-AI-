from flask import Blueprint, render_template, session
from bson.objectid import ObjectId
from ..middleware.auth_middleware import auth_required
from ..database.collections import (
    get_properties_collection,
    get_customers_collection,
    get_inquiries_collection,
    get_visits_collection
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@auth_required
def dashboard():

    role = session["role"]
    user_id = session["user_id"]

    properties_col = get_properties_collection()
    customers_col = get_customers_collection()
    inquiries_col = get_inquiries_collection()
    visits_col = get_visits_collection()

    data = {
        "role": role
    }

    # ===================== ADMIN DASHBOARD =====================
    if role == "admin":

        # ---- KPI COUNTS ----
        data["stats"] = {
            "properties": properties_col.count_documents({}),
            "customers": customers_col.count_documents({}),
            "inquiries": inquiries_col.count_documents({}),
            "visits": visits_col.count_documents({})
        }

        # ---- CITY WISE INQUIRIES ----
        city_counter = {}
        for i in inquiries_col.find():
            city = i.get("requirements", {}).get("location", {}).get("city")
            if city:
                city_counter[city] = city_counter.get(city, 0) + 1

        data["city_chart"] = {
            "labels": list(city_counter.keys()),
            "values": list(city_counter.values())
        }

        # ---- BUDGET WISE INQUIRIES ----
        b1 = b2 = b3 = 0
        for i in inquiries_col.find():
            maxb = i.get("requirements", {}).get("budgetmax", 0)
            if maxb <= 5_000_000:
                b1 += 1
            elif maxb <= 10_000_000:
                b2 += 1
            else:
                b3 += 1

        data["budget_chart"] = {
            "labels": ["0–50L", "50L–1Cr", "1Cr+"],
            "values": [b1, b2, b3]
        }

        # ---- CONVERSION FUNNEL ----
        confirmed_visits = visits_col.count_documents({"status": "Confirmed"})

        data["funnel_chart"] = {
            "labels": ["Inquiries", "Visits", "Confirmed"],
            "values": [
                data["stats"]["inquiries"],
                data["stats"]["visits"],
                confirmed_visits
            ]
        }

    # ===================== STAFF DASHBOARD =====================
    else:

        my_visits = list(
            visits_col.find({"usersid": ObjectId(user_id)})
        )

        total = len(my_visits)
        upcoming = len([v for v in my_visits if v.get("status") != "Confirmed"])
        completed = len([v for v in my_visits if v.get("status") == "Confirmed"])

        data["stats"] = {
            "total": total,
            "upcoming": upcoming,
            "completed": completed
        }

        # ---- DAILY VISIT TREND ----
        daily_counter = {}
        for v in my_visits:
            date = v.get("preferreddate")
            if date:
                daily_counter[date] = daily_counter.get(date, 0) + 1

        data["daily_chart"] = {
            "labels": list(daily_counter.keys()),
            "values": list(daily_counter.values())
        }

    return render_template("dashboard/dashboard.html", data=data)
