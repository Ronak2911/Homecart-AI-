from ..database.collections import get_properties_collection
from bson.objectid import ObjectId

def add_property(data):
    properties = get_properties_collection()
    properties.insert_one(data)


def get_properties():
    properties = get_properties_collection()
    data = list(properties.find())
    for p in data:
        p["_id"] = str(p["_id"])
    return data

def update_property(pid, data):
    properties = get_properties_collection()
    properties.update_one(
        {"_id": ObjectId(pid)},
        {"$set": data}
    )

def delete_property(pid):
    properties = get_properties_collection()
    properties.delete_one({"_id": ObjectId(pid)})
