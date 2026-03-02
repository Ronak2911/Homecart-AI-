# from flask import Blueprint, render_template, request
# from ..database.mongodb import mongo
# from ..models.customer_model import Customers

# customer_bp = Blueprint("customers", __name__)

# @customer_bp.route("/customers")
# def customers():
#     print("📢 Customers route called")

#     customers_data = Customers.get_all()

#     print("👤 From model:", customers_data)

#     search = request.args.get("search", "")
#     city = request.args.get("city", "")
#     leadstatus = request.args.get("leadstatus", "")
    

#     query = {}

#     # 🔎 Search by Name OR WhatsApp
#     if search:
#         query["$or"] = [
#             {"Name": {"$regex": search, "$options": "i"}},
#             {"WhatsApp": {"$regex": search, "$options": "i"}}
#         ]

#     # 🌆 Filter by City
#     if city:
#         query["City"] = {"$regex": city, "$options": "i"}

#     # 🔥 Filter by Lead Status
#     if leadstatus:
#         query["Lead Status"] = leadstatus

#     customers_data = list(
#         mongo.db.customers.find(query).sort("updated_at", -1)
#     )

#     # ✅ DEBUG (optional – remove later)
#     print("Customers from DB:", customers_data)

#     formatted_customers = []

#     for c in customers_data:
#         formatted_customers.append({
#             "name": c.get("Name") or "-",
#             "whatsappnumber": c.get("WhatsApp") or "-",
#             "city": c.get("City") or "-",
#             "leadstatus": c.get("Lead Status") or "Cold",
#             "budgetrange": c.get("Budget") or "-",
#             "propertytype": c.get("Type") or "-",
#             "status": c.get("Inquiry Status") or "No inquiries"
#         })

#     return render_template(
#         "customer_list.html",
#         customers=formatted_customers
#     )


from flask import Blueprint, render_template, request
from ..models.customer_model import get_customers_collection


customer_bp = Blueprint("customers", __name__)
@customer_bp.route("/customer-list")
def customers():

    customers = get_customers_collection()
    search = request.args.get("search", "").strip()
    city = request.args.get("city", "").strip()


    query = {}

    # 🔍 Search filter (Name or WhatsApp)
    if search:
        query["$or"] = [
            {"Name": {"$regex": search, "$options": "i"}},
            {"WhatsApp": {"$regex": search, "$options": "i"}}
        ]

    # 🏙 City filter
    if city:
        query["City"] = {"$regex": city, "$options": "i"}

    data = list(customers.find(query))

    result = []

    for customer in data:
        result.append({
            "name": customer.get("Name", ""),
            "whatsappnumber": customer.get("WhatsApp", ""),
            "city": customer.get("City", ""),
            "budgetrange": customer.get("Budget", ""),
            "propertytype": customer.get("Type", ""),
            "status": customer.get("Inquiry Status", "No inquiries")
        })

    return render_template("customer/customer_list.html", customers=result)