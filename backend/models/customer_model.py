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
from unicodedata import name

from ..database.collections import get_customers_collection, get_inquiries_collection

def show_customers():

    customers_col = get_customers_collection()
    # inquiries_col = get_inquiries_collection()

    customers = list(customers_col.find())
    # inquiries = list(inquiries_col.find())

    result = []
    # inquiry_map = {}

    # for inquiry in inquiries:
    #     customerid = inquiry.get("customerid")

    #     if customerid not in inquiry_map:
    #         inquiry_map[customerid] = []

    #     inquiry_map[customerid].append(inquiry)

    for customer in customers:

            # customer_id = customer["_id"]
            # customer_inquiries = inquiry_map.get(customer_id, [])

            # if customer_inquiries:

            #     for inquiry in customer_inquiries:

            #         location = inquiry.get("location", {})
            #         requirements = inquiry.get("requirements", {})

            #         budgetmin = requirements.get("budgetmin")
            #         budgetmax = requirements.get("budgetmax")

            #         if budgetmin and budgetmax:
            #             budgetrange = f"{int(budgetmin/100000)}L-{int(budgetmax/100000)}L"
            #         else:
            #             budgetrange = customer.get("Budget", "")

                # result.append({
                #     "name": customer.get("Name", ""),
                #     "whatsappnumber": customer.get("WhatsApp", ""),
                #     "city": customer.get("City", ""),
                #     # "area": location.get("area", ""),
                #     # "budgetrange": budgetrange,
                #     # "propertytype": requirements.get("propertytype") or customer.get("Type", ""),
                #     "budgetrange": str(customer.get("Budget", "")).strip(),
                #     "propertytype": str(customer.get("Type", "")).strip(),
                #     "status": inquiry.get("inquirystatus") or customer.get("Inquiry Status", "No inquiries")
                # })
        result.append({
            "name": str(customer.get("Name", "")).strip(),
            "whatsappnumber": str(customer.get("WhatsApp", "")).strip(),
            "city": str(customer.get("City", "")).strip(),
            "budgetrange": str(customer.get("Budget", "")).strip(),
            "propertytype": str(customer.get("Type", "")).strip(),
            "status": str(customer.get("Inquiry Status", "No inquiries")).strip()
        }) 

        # else:

        #     result.append({
        #         "name": customer.get("Name", ""),
        #         "whatsappnumber": customer.get("WhatsApp", ""),
        #         "city": customer.get("City", ""),
        #         "area": "",
        #         "budgetrange": customer.get("Budget", ""),
        #         "propertytype": customer.get("Type", ""),
        #         "status": customer.get("Inquiry Status", "No inquiries")
        #     })

    return result