# from ..database.collections import get_customers_collection, get_inquiries_collection

# def show_customers():

#     customers_col = get_customers_collection()
#     inquiries_col = get_inquiries_collection()

#     customers = list(customers_col.find())
#     inquiries = list(inquiries_col.find())

#     result = []

#     # map inquiries by customerid
#     inquiry_map = {}

#     for inquiry in inquiries:

#         customerid = inquiry.get("customerid")

#         if customerid not in inquiry_map:
#             inquiry_map[customerid] = []

#         inquiry_map[customerid].append(inquiry)

#     # merge
#     for customer in customers:

#         customer_id = customer["_id"]

#         customer_inquiries = inquiry_map.get(customer_id, [])

#         if customer_inquiries:

#             for inquiry in customer_inquiries:

#                 location = inquiry.get("location", {})
#                 requirements = inquiry.get("requirements", {})

#                 budgetmin = requirements.get("budgetmin")
#                 budgetmax = requirements.get("budgetmax")

#                 if budgetmin and budgetmax:
#                     budgetrange = f"{int(budgetmin/100000)}L-{int(budgetmax/100000)}L"
#                 else:
#                     budgetrange = None

#                 result.append({
#                     "name": customer.get("name"),
#                     "whatsappnumber": customer.get("whatsappnumber"),
#                     "city": customer.get("city"),
#                     "leadstatus": customer.get("leadstatus"),

#                     "area": location.get("area"),
#                     "budgetrange": budgetrange,
#                     "propertytype": requirements.get("propertytype"),
#                     "status": inquiry.get("inquirystatus")
#                 })

#         else:

#             result.append({
#                 "name": customer.get("name"),
#                 "whatsappnumber": customer.get("whatsappnumber"),
#                 "city": customer.get("city"),
#                 "leadstatus": customer.get("leadstatus"),

#                 "area": None,
#                 "budgetrange": None,
#                 "propertytype": None,
#                 "status": "No inquiries"
#             })

#     return result
from ..database.collections import get_customers_collection, get_inquiries_collection

def show_customers():

    customers_col = get_customers_collection()
    inquiries_col = get_inquiries_collection()

    customers = list(customers_col.find())
    inquiries = list(inquiries_col.find())

    result = []

    inquiry_map = {}

    for inquiry in inquiries:
        customerid = inquiry.get("customerid")

        if customerid not in inquiry_map:
            inquiry_map[customerid] = []

        inquiry_map[customerid].append(inquiry)

    for customer in customers:

        customer_id = customer["_id"]
        customer_inquiries = inquiry_map.get(customer_id, [])

        if customer_inquiries:

            for inquiry in customer_inquiries:

                location = inquiry.get("location", {})
                requirements = inquiry.get("requirements", {})

                budgetmin = requirements.get("budgetmin")
                budgetmax = requirements.get("budgetmax")

                if budgetmin and budgetmax:
                    budgetrange = f"{int(budgetmin/100000)}L-{int(budgetmax/100000)}L"
                else:
                    budgetrange = customer.get("Budget") or "-"

                result.append({
                    "name": customer.get("Name") or "-",
                    "whatsappnumber": customer.get("WhatsApp") or "-",
                    "city": customer.get("City") or "-",
                    "leadstatus": customer.get("Lead Status") or "-",

                    "area": location.get("area") or "-",
                    "budgetrange": budgetrange,
                    "propertytype": requirements.get("propertytype") or customer.get("Type") or "-",
                    "status": inquiry.get("inquirystatus") or customer.get("Inquiry Status") or "No inquiries"
                })

        else:

            result.append({
                "name": customer.get("Name") or "-",
                "whatsappnumber": customer.get("WhatsApp") or "-",
                "city": customer.get("City") or "-",
                "leadstatus": customer.get("Lead Status") or "-",

                "area": "-",
                "budgetrange": customer.get("Budget") or "-",
                "propertytype": customer.get("Type") or "-",
                "status": customer.get("Inquiry Status") or "No inquiries"
            })

    return result

