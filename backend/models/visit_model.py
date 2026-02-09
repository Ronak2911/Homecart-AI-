from bson.objectid import ObjectId

from ..database.collections import (
    get_visits_collection,
    get_users_collection,
    get_customers_collection,
 git    get_properties_collection
)


# =====================================================
# GET VISITS WITH DETAILS + FILTERS
# =====================================================

def get_visits_with_filters(user, filters=None):

    visits_col = get_visits_collection()

    pipeline = []

    # ROLE FILTER
    if user.get("role") != "admin":

        pipeline.append({
            "$match": {
                "usersid": ObjectId(user["_id"])
            }
        })

    # LOOKUPS
    pipeline.extend([

        # CUSTOMER JOIN
        {
            "$lookup": {
                "from": "customers",
                "localField": "customerid",
                "foreignField": "_id",
                "as": "customer"
            }
        },

        # STAFF JOIN
        {
            "$lookup": {
                "from": "users",
                "localField": "usersid",
                "foreignField": "_id",
                "as": "staff"
            }
        },

        # PROPERTY JOIN  ✅ FIXED HERE
        {
            "$lookup": {
                "from": "property",   # ✅ CORRECT COLLECTION NAME
                "localField": "propertyid",
                "foreignField": "_id",
                "as": "property"
            }
        },

        # UNWIND
        {
            "$unwind": {
                "path": "$customer",
                "preserveNullAndEmptyArrays": True
            }
        },

        {
            "$unwind": {
                "path": "$staff",
                "preserveNullAndEmptyArrays": True
            }
        },

        {
            "$unwind": {
                "path": "$property",
                "preserveNullAndEmptyArrays": True
            }
        }

    ])

    # FILTERS
    match_filter = {}

    if filters:

        if filters.get("city"):
            match_filter["customer.city"] = filters["city"]

        if filters.get("staffid"):
            match_filter["usersid"] = ObjectId(filters["staffid"])

        if filters.get("status"):
            match_filter["status"] = filters["status"]

        if filters.get("propertyid"):
            match_filter["propertyid"] = ObjectId(filters["propertyid"])

        if filters.get("visitdate"):
            match_filter["preferreddate"] = filters["visitdate"]

    if match_filter:
        pipeline.append({"$match": match_filter})

    # SORT
    pipeline.append({
        "$sort": {
            "preferreddate": -1
        }
    })

    # EXECUTE
    data = list(visits_col.aggregate(pipeline))

    result = []

    for v in data:

        result.append({

            "_id": str(v["_id"]),

            # CUSTOMER
            "customer_name": v.get("customer", {}).get("name"),
            "property_city": v.get("property", {}).get("location", {}).get("city"),


            # PROPERTY
            "property_title": v.get("property", {}).get("title"),
            "property_city": v.get("property", {}).get("location", {}).get("city"),


            # STAFF
            "staff_name": v.get("staff", {}).get("name"),

            # VISIT INFO
            "visittype": v.get("visittype"),
            "preferreddate": v.get("preferreddate"),
            "preferredtime": v.get("preferredtime"),

            "status": v.get("status", "scheduled")

        })

    return result


# =====================================================
# GET STAFF LIST
# =====================================================

def get_staff_list():

    users_col = get_users_collection()

    staff = list(users_col.find({
        "role": "staff",
        "isactive": True
    }))

    for s in staff:
        s["_id"] = str(s["_id"])

    return staff


# =====================================================
# GET PROPERTY LIST
# =====================================================

def get_property_list():

    properties_col = get_properties_collection()

    properties = list(properties_col.find())

    for p in properties:
        p["_id"] = str(p["_id"])

    return properties


# =====================================================
# ASSIGN STAFF
# =====================================================

def assign_staff_to_visit(visit_id, staff_id):

    visits_col = get_visits_collection()

    result = visits_col.update_one(
        {"_id": ObjectId(visit_id)},
        {"$set": {"usersid": ObjectId(staff_id)}}
    )

    return result.modified_count > 0


# =====================================================
# GET STAFF BY CITY
# =====================================================

def get_staff_by_city(city):

    users_col = get_users_collection()

    staff = list(users_col.find({
        "role": "staff",
        "city": city,
        "isactive": True
    }))

    result = []

    for s in staff:

        result.append({

            "_id": str(s["_id"]),
            "name": s.get("name"),
            "city": s.get("city"),
            "email": s.get("email"),
            "phone": s.get("phone")

        })

    return result
