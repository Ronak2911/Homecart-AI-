from bson.objectid import ObjectId

from ..database.collections import (
    get_visits_collection,
    get_users_collection,
    get_customers_collection,
    get_properties_collection
)

# =====================================================
# GET VISITS WITH DETAILS + FILTERS ✅ FIXED
# =====================================================

def get_visits_with_filters(user, filters=None):

    visits_col = get_visits_collection()

    pipeline = []

    # =========================
    # ROLE FILTER
    # =========================
    if user.get("role") != "admin":
        try:
            pipeline.append({
                "$match": {
                    "usersid": ObjectId(user["_id"])
                }
            })
        except Exception as e:
            print("❌ Invalid session user_id:", e)

    # =========================
    # LOOKUPS
    # =========================
    pipeline.extend([

        {
            "$lookup": {
                "from": "customers",
                "localField": "customerid",
                "foreignField": "_id",
                "as": "customer"
            }
        },

        {
            "$lookup": {
                "from": "users",
                "localField": "usersid",
                "foreignField": "_id",
                "as": "staff"
            }
        },

        {
            "$lookup": {
                "from": "properties",
                "localField": "propertyid",
                "foreignField": "_id",
                "as": "property"
            }
        },

        {"$unwind": {"path": "$customer", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$staff", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$property", "preserveNullAndEmptyArrays": True}}
    ])

    # =========================
    # FILTERS
    # =========================
    match_filter = {}

    if filters:

        if filters.get("city"):
            match_filter["customer.City"] = filters["city"]

        if filters.get("staffid"):
            try:
                match_filter["usersid"] = ObjectId(filters["staffid"])
            except:
                print("❌ Invalid staffid filter")

        if filters.get("status"):
            match_filter["status"] = filters["status"]

        if filters.get("propertyid"):
            try:
                match_filter["propertyid"] = ObjectId(filters["propertyid"])
            except:
                print("❌ Invalid propertyid filter")

        if filters.get("visitdate"):
            match_filter["preferreddate"] = filters["visitdate"]

    if match_filter:
        pipeline.append({"$match": match_filter})

    # =========================
    # SORT
    # =========================
    pipeline.append({
        "$sort": {"preferreddate": -1}
    })

    data = list(visits_col.aggregate(pipeline))

    result = []

    for v in data:

        staff_doc = v.get("staff", {})
        property_doc = v.get("property", {})
        customer_doc = v.get("customer", {})

        result.append({

            "_id": str(v.get("_id")),

            # =========================
            # VISIT DETAILS
            # =========================
            "visittype": v.get("visittype"),
            "preferreddate": v.get("preferreddate"),
            "preferredtime": v.get("preferredtime"),
            "status": v.get("status", "Pending"),
            "message": v.get("message"),

            # =========================
            # CUSTOMER DETAILS ✅ SAFE
            # =========================
            "customer": {
                "name": customer_doc.get("Name"),
                "phone": customer_doc.get("WhatsApp"),
                "city": customer_doc.get("City"),
                "budget": customer_doc.get("Budget"),
            },

            # =========================
            # PROPERTY DETAILS ✅ SAFE
            # =========================
            "property": {
                "title": property_doc.get("name") or property_doc.get("title"),
                "city": property_doc.get("location", {}).get("city"),
                "area": property_doc.get("location", {}).get("area"),
                "price": property_doc.get("price"),
            },

            # =========================
            # STAFF DETAILS ✅ FIXED
            # =========================
            "staff_name": (
                staff_doc.get("name")
                if staff_doc.get("role") == "staff"
                else None
            ),

            # =========================
            # FLAT FIELDS FOR HTML ✅
            # =========================
            "customer_name": customer_doc.get("Name"),
            "property_title": property_doc.get("name") or property_doc.get("title"),
        })

    return result


# =====================================================
# GET STAFF LIST ✅
# =====================================================

def get_staff_list():

    users_col = get_users_collection()

    staff = list(users_col.find({
        "role": "staff",
        "status": "active"
    }))

    for s in staff:
        s["_id"] = str(s["_id"])

    return staff


# =====================================================
# GET PROPERTY LIST ✅
# =====================================================

def get_property_list():

    properties_col = get_properties_collection()

    properties = list(properties_col.find())

    for p in properties:
        p["_id"] = str(p["_id"])

    return properties


# =====================================================
# ASSIGN STAFF TO VISIT ✅
# =====================================================

def assign_staff_to_visit(visit_id, staff_id):

    visits_col = get_visits_collection()

    try:
        visit_obj_id = ObjectId(visit_id)
        staff_obj_id = ObjectId(staff_id)
    except Exception as e:
        print("❌ ObjectId Error:", e)
        return False

    result = visits_col.update_one(
        {"_id": visit_obj_id},
        {"$set": {"usersid": staff_obj_id}}
    )

    print("✅ Staff Assigned:", result.modified_count)

    return result.modified_count > 0


# =====================================================
# GET STAFF BY CITY ✅
# =====================================================

def get_staff_by_city(city):

    users_col = get_users_collection()

    if not city:
        return []

    # ✅ Case-insensitive exact match
    staff = list(users_col.find({
        "role": "staff",
        "status": "active",
        "city": {
            "$regex": f"^{city}$",
            "$options": "i"
        }
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