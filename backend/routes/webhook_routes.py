import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

webhook_bp = Blueprint("webhook", __name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
TOKEN = os.getenv("WHATSAPP_TOKEN")
# Support BOTH names (prevents bugs)
PHONE_ID = (
    os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    or os.getenv("PHONE_NUMBER_ID")
)

if not PHONE_ID:
    raise Exception("❌ PHONE NUMBER ID missing in ENV")

GRAPH_URL = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"

print("✅ VERIFY_TOKEN:", VERIFY_TOKEN)
print("✅ PHONE_ID:", PHONE_ID)
print("✅ GRAPH_URL:", GRAPH_URL)


@webhook_bp.before_app_request
def log_all_requests():
    print("\n====================")
    print("📡 Incoming Request")
    print("Method:", request.method)
    print("URL:", request.url)
    print("Headers:", dict(request.headers))
    print("====================\n")


# -----------------------------------
# Send helper
# -----------------------------------
def send_whatsapp(payload):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload["messaging_product"] = "whatsapp"

    response = requests.post(GRAPH_URL, headers=headers, json=payload)
    print("📤 WhatsApp API response:", response.json())


# -----------------------------------
# Webhook route
# -----------------------------------
# @webhook_bp.route("/webhook", methods=["GET"])
# def whatsapp_webhook():

#     # -----------------------------------
#     # Webhook Verification
#     # -----------------------------------
#     if request.method == "GET":
#         mode = request.args.get("hub.mode")
#         token = request.args.get("hub.verify_token")
#         challenge = request.args.get("hub.challenge")

#         print("🔎 Webhook verification request")

#         if mode == "subscribe" and token == VERIFY_TOKEN:
#             print("✅ Webhook verified successfully")
#             return challenge, 200

#         print("❌ Webhook verification failed")
#         return "Forbidden", 403

#     # -----------------------------------
#     # Incoming Messages
#     # -----------------------------------
#     if request.method == "POST":
#         data = request.json
#         print("📩 Incoming WhatsApp payload:", data)

#         try:
#             message = data["entry"][0]["changes"][0]["value"]["messages"][0]
#         except Exception:
#             print("⚠️ No message in payload")
#             return "EVENT_RECEIVED", 200

#         from_number = message["from"]
#         msg_type = message["type"]

#         print("👤 From:", from_number)
#         print("💬 Type:", msg_type)

#         if msg_type == "text":
#             send_main_menu(from_number)

#         elif msg_type == "interactive":
#             interactive = message["interactive"]

#             if "button_reply" in interactive:
#                 reply_id = interactive["button_reply"]["id"]
#                 print("🔘 Button clicked:", reply_id)
#                 handle_reply(from_number, reply_id)

#             elif "list_reply" in interactive:
#                 reply_id = interactive["list_reply"]["id"]
#                 print("📋 List selected:", reply_id)
#                 handle_reply(from_number, reply_id)

#         return "EVENT_RECEIVED", 200

@webhook_bp.route("/webhook", methods=["POST"])
def receive_webhook():
    # -----------------------------------
    # Incoming Messages (Meta POST)
    # -----------------------------------
    print("Request Call post",request.json)
    data = request.json
    print("📩 Incoming WhatsApp payload:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
    except Exception:
        print("⚠️ No message in payload")
        return "EVENT_RECEIVED", 200

    from_number = message["from"]
    msg_type = message["type"]

    print("👤 From:", from_number)
    print("💬 Type:", msg_type)

    if msg_type == "text":
        send_main_menu(from_number)

    elif msg_type == "interactive":
        interactive = message["interactive"]

        if "button_reply" in interactive:
            reply_id = interactive["button_reply"]["id"]
            print("🔘 Button clicked:", reply_id)
            handle_reply(from_number, reply_id)

        elif "list_reply" in interactive:
            reply_id = interactive["list_reply"]["id"]
            print("📋 List selected:", reply_id)
            handle_reply(from_number, reply_id)

    return "EVENT_RECEIVED", 200

@webhook_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    # -----------------------------------
    # Webhook Verification (Meta GET)
    # -----------------------------------
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print("🔎 Webhook verification request")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully")
        return challenge, 200

    print("❌ Webhook verification failed")
    return "Forbidden", 403



# -----------------------------------
# Bot Logic
# -----------------------------------
def send_main_menu(to):
    send_whatsapp({
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Welcome! Choose an option:"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "track_order",
                            "title": "Track Order"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "buy_product",
                            "title": "Buy Product"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "support",
                            "title": "Support"
                        }
                    }
                ]
            }
        }
    })


def handle_reply(to, reply_id):

    if reply_id == "track_order":
        send_whatsapp({
            "to": to,
            "type": "text",
            "text": {
                "body": "Please enter your Order ID"
            }
        })

    elif reply_id == "buy_product":
        send_product_list(to)

    elif reply_id == "support":
        send_whatsapp({
            "to": to,
            "type": "text",
            "text": {
                "body": "Connecting you to support..."
            }
        })

    elif reply_id.startswith("cat_"):
        send_whatsapp({
            "to": to,
            "type": "text",
            "text": {
                "body": f"You selected category: {reply_id}"
            }
        })


def send_product_list(to):
    send_whatsapp({
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": "Choose a category"
            },
            "action": {
                "button": "View Categories",
                "sections": [
                    {
                        "title": "Available Categories",
                        "rows": [
                            {"id": "cat_elec", "title": "Electronics"},
                            {"id": "cat_cloth", "title": "Clothing"},
                            {"id": "cat_home", "title": "Home Items"}
                        ]
                    }
                ]
            }
        }
    })

@webhook_bp.route("/data-deletion")
def data_deletion():
    return """
    <h2>Data Deletion Instructions</h2>
    <p>
    Users can request deletion of their data by contacting us at:
    <b>patelchit842005@Gmail.com</b>
    </p>
    <p>
    Upon request, we will delete all stored user information including
    phone number, messages, and profile data.
    </p>
    """

@webhook_bp.route("/privacy-policy")
def privacy_policy():
    return """
    <h2>Privacy Policy</h2>
    <p>
    This application provides WhatsApp chatbot services.
    </p>

    <p>
    We may collect limited user information such as:
    </p>
    <ul>
        <li>Phone number</li>
        <li>User messages</li>
        <li>Profile name (if available)</li>
    </ul>

    <p>
    This data is used solely for providing chatbot functionality
    and improving user experience.
    </p>

    <p>
    We do NOT sell, trade, or share user data with third parties.
    </p>

    <p>
    If you have any privacy-related concerns, contact us at:
    <b>patelchit842005@Gmail.com</b>
    </p>
    """

@webhook_bp.route("/terms")
def terms_conditions():
    return """
    <h2>Terms & Conditions</h2>

    <p>
    By using this WhatsApp chatbot, you agree to the following terms:
    </p>

    <ul>
        <li>The chatbot is provided for informational/demo purposes.</li>
        <li>Users must not misuse the service.</li>
        <li>We are not responsible for decisions made based on chatbot responses.</li>
        <li>Service availability is not guaranteed.</li>
    </ul>

    <p>
    We reserve the right to modify or discontinue the service at any time.
    </p>

    <p>
    For questions, contact:
    <b>patelchit842005@Gmail.com</b>
    </p>
    """
