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
from ..models.customer_model import show_customers

customer_bp = Blueprint("customers", __name__)

@customer_bp.route("/customers")
def customers():

    print("📢 Customers route called")

    customers_data = show_customers()

    search = request.args.get("search", "").lower()
    city = request.args.get("city", "").lower()
    leadstatus = request.args.get("leadstatus", "").lower()

    filtered = []

    for c in customers_data:

        if search:
            if search not in (c["name"] or "").lower() and \
               search not in (c["whatsappnumber"] or "").lower():
                continue

        if city:
            if city not in (c["city"] or "").lower():
                continue

        if leadstatus:
            if leadstatus != (c["leadstatus"] or "").lower():
                continue

        filtered.append(c)

    return render_template(
        "customer_list.html",
        customers=filtered
    )