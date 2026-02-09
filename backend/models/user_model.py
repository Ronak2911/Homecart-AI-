from bson.objectid import ObjectId
from ..database.collections import (
    get_inquiries_collection,
    get_visits_collection
)

def get_inquiries_for_user(user):
    """
    user = {
      "_id": "...",
      "role": "admin" | "staff"
    }
    """

    inquiries_col = get_inquiries_collection()
    visits_col = get_visits_collection()

    # ---------------- ADMIN ----------------
    if user["role"] == "admin":
        inquiries = list(inquiries_col.find())

    # ---------------- STAFF ----------------
    else:
        # find inquiry ids assigned to staff via visits
        visits = visits_col.find({"usersid": ObjectId(user["_id"])})
        inquiry_ids = {v["inquiryid"] for v in visits}

        inquiries = list(
            inquiries_col.find({"_id": {"$in": list(inquiry_ids)}})
        )

    # convert ids
    for i in inquiries:
        i["_id"] = str(i["_id"])
        i["customerid"] = str(i["customerid"])

    return inquiries


def filter_and_sort_inquiries(inquiries, filters):
    """
    filters = {
      city, status, type, sort
    }
    """

    # -------- FILTERS --------
    if filters.get("city"):
        inquiries = [
            i for i in inquiries
            if i["requirements"]["location"]["city"] == filters["city"]
        ]

    if filters.get("status"):
        inquiries = [
            i for i in inquiries
            if i["inquirystatus"] == filters["status"]
        ]

    if filters.get("type"):
        inquiries = [
            i for i in inquiries
            if i["requirements"]["propertytype"] == filters["type"]
        ]

    # -------- SORTING --------
    if filters.get("sort") == "budget_low":
        inquiries.sort(
            key=lambda x: x["requirements"]["budgetmin"]
        )

    if filters.get("sort") == "budget_high":
        inquiries.sort(
            key=lambda x: x["requirements"]["budgetmax"],
            reverse=True
        )

    if filters.get("sort") == "newest":
        inquiries.reverse()

    return inquiries
