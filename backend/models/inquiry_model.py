from warnings import filters

from bson.objectid import ObjectId
from ..database.collections import (
    get_inquiries_collection,
    get_visits_collection
)

# def get_inquiries_for_user(user):
#     """
#     user = {
#         "_id": "string",
#         "role": "admin" | "staff"
#     }
#     """

#     inquiries_col = get_inquiries_collection()
#     visits_col = get_visits_collection()

#     # ---------------- ADMIN ----------------
#     if user["role"] == "admin":
#         data = list(inquiries_col.find())

#     # ---------------- STAFF ----------------
#     else:
#         visits = list(
#             visits_col.find(
#                 {"usersid": ObjectId(user["_id"])},
#                 {"inquiryid": 1}
#             )
#         )

#         inquiry_ids = [v.get("inquiryid") for v in visits if v.get("inquiryid")]

#         if not inquiry_ids:
#             return []

#         data = list(
#             inquiries_col.find({"_id": {"$in": inquiry_ids}})
#         )

#     # Convert ObjectIds → string
#     for i in data:
#         i["_id"] = str(i["_id"])
#         if "customerid" in i:
#             i["customerid"] = str(i["customerid"])

#     return data


def get_inquiries_for_user(user, filters=None):

    inquiries_col = get_inquiries_collection()
    visits_col = get_visits_collection()

    query = {}

    # ROLE FILTER
    if user["role"] != "admin":

        visits = list(
            visits_col.find(
                {"usersid": ObjectId(user["_id"])},
                {"inquiryid": 1}
            )
        )

        inquiry_ids = [v.get("inquiryid") for v in visits if v.get("inquiryid")]

        if not inquiry_ids:
            return []

        query["_id"] = {"$in": inquiry_ids}

    # APPLY FILTERS
    if filters:

        # ✅ CITY (partial + case insensitive)
        if filters.get("city"):
            query["City"] = {
                "$regex": filters["city"],
                "$options": "i"
            }

        # ✅ STATUS (only Visit / Visited)
        if filters.get("status"):
            query["Status"] = {
                "$regex": f"^{filters['status']}$",
                "$options": "i"
            }

        # ✅ TYPE LOGIC
        if filters.get("type"):

            if filters["type"].lower() == "flat":
                # match any type containing 'flat'
                query["Type"] = {
                    "$regex": "flat",
                    "$options": "i"
                }
            else:
                # for Villa exact match
                query["Type"] = {
                    "$regex": f"^{filters['type']}$",
                    "$options": "i"
                }

        data = list(inquiries_col.find(query).sort("created_at", -1))


    for i in data:
        i["_id"] = str(i["_id"])

    return data