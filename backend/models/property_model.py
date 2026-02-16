from ..database.collections import get_properties_collection
from bson.objectid import ObjectId
import json

def add_property(data):
    properties = get_properties_collection()
    properties.insert_one(data)


def get_properties():

    properties = get_properties_collection()
    data = list(properties.find())

    clean_data = []

    for p in data:

        # Convert ObjectId to string
        p["_id"] = str(p["_id"])

        # ---------- FIX MEDIA ----------
        media = p.get("media", {})

        if isinstance(media, str):
            try:
                media = json.loads(media)
            except:
                media = {}

        if not isinstance(media, dict):
            media = {}

        media.setdefault("images", [])
        media.setdefault("video", "")

        p["media"] = media


        # ---------- FIX LOCATION ----------
        location = p.get("location", {})

        if isinstance(location, str):
            try:
                location = json.loads(location)
            except:
                location = {}

        if not isinstance(location, dict):
            location = {}

        location.setdefault("city", "")
        location.setdefault("area", "")
        location.setdefault("pincode", "")
        location.setdefault("address", "")

        p["location"] = location


        # ---------- FIX PRICE ----------
        try:
            p["price"] = int(p.get("price", 0))
        except:
            p["price"] = 0


        clean_data.append(p)

    return clean_data


def update_property(pid, data):
    properties = get_properties_collection()
    properties.update_one(
        {"_id": ObjectId(pid)},
        {"$set": data}
    )


def delete_property(pid):
    properties = get_properties_collection()
    properties.delete_one({"_id": ObjectId(pid)})


def get_properties_filtered(city=None, ptype=None, status=None, sort=None, page=1, per_page=10):

    collection = get_properties_collection()

    query = {}

    # FILTERS
    if city:
        query["city"] = city

    if ptype:
        query["type"] = ptype

    if status:
        query["status"] = status


    # SORT
    sort_order = None

    if sort == "low":
        sort_order = ("price", 1)

    elif sort == "high":
        sort_order = ("price", -1)


    # PAGINATION
    skip = (page - 1) * per_page


    cursor = collection.find(query)

    total = collection.count_documents(query)


    if sort_order:
        cursor = cursor.sort([sort_order])


    cursor = cursor.skip(skip).limit(per_page)


    properties = list(cursor)


    # Convert ObjectId → string
    for p in properties:
        p["_id"] = str(p["_id"])


    return properties, total


