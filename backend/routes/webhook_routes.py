import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

webhook_bp = Blueprint("webhook", __name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")

GRAPH_URL = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"


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
    print("WhatsApp API response:", response.json())


# -----------------------------------
# Webhook route
# -----------------------------------
@webhook_bp.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():

    # -----------------------------------
    # Meta Webhook Verification
    # -----------------------------------
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Forbidden", 403

    # -----------------------------------
    # Incoming WhatsApp Messages
    # -----------------------------------
    if request.method == "POST":
        data = request.json
        print("Incoming WhatsApp message:", data)

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        except Exception:
            return "EVENT_RECEIVED", 200

        from_number = message["from"]
        msg_type = message["type"]

        if msg_type == "text":
            send_main_menu(from_number)

        elif msg_type == "interactive":
            button_id = message["interactive"]["button_reply"]["id"]
            handle_button(from_number, button_id)

        return "EVENT_RECEIVED", 200


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


def handle_button(to, btn):

    if btn == "track_order":
        send_whatsapp({
            "to": to,
            "type": "text",
            "text": {
                "body": "Please enter your Order ID"
            }
        })

    elif btn == "buy_product":
        send_product_list(to)

    elif btn == "support":
        send_whatsapp({
            "to": to,
            "type": "text",
            "text": {
                "body": "Connecting you to support..."
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
                "sections": [
                    {
                        "title": "Categories",
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
