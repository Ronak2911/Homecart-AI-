from .mongodb import mongo


def get_users_collection():
    return mongo.db.users

def get_properties_collection():
    return mongo.db.properties

def get_customers_collection():
    return mongo.db.customers


def get_inquiries_collection():
    return mongo.db.inquires


def get_visits_collection():
    return mongo.db.visits


def get_chatlogs_collection():
    return mongo.db.chatlogs
