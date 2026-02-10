import os
from flask import Blueprint, request

webhook_bp = Blueprint("webhook", __name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@webhook_bp.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Meta verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        print("VERIFY_TOKEN (server):", VERIFY_TOKEN)
        print("VERIFY_TOKEN (meta):", token)

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Forbidden", 403

    # Incoming WhatsApp messages
    if request.method == "POST":
        print("Incoming WhatsApp message:", request.json)
        return "EVENT_RECEIVED", 200
