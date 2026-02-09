from bson.objectid import ObjectId
from ..database.collections import (
    get_inquiries_collection,
    get_visits_collection
)

def get_inquiries_for_user(user):
    """
    user = {
        "_id": "string",
        "role": "admin" | "staff"
    }
    """

    inquiries_col = get_inquiries_collection()
    visits_col = get_visits_collection()

    # ---------------- ADMIN ----------------
    if user["role"] == "admin":
        data = list(inquiries_col.find())

    # ---------------- STAFF ----------------
    else:
        visits = list(
            visits_col.find(
                {"usersid": ObjectId(user["_id"])},
                {"inquiryid": 1}
            )
        )

        inquiry_ids = [v["inquiryid"] for v in visits]

        if not inquiry_ids:
            return []

        data = list(
            inquiries_col.find({"_id": {"$in": inquiry_ids}})
        )

    # Convert ObjectIds → string
    for i in data:
        i["_id"] = str(i["_id"])
        if "customerid" in i:
            i["customerid"] = str(i["customerid"])

    return data
