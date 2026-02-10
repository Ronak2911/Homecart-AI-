from dotenv import load_dotenv
import os
from flask import request

# Load backend/.env explicitly (local only)
ENV_PATH = os.path.join(os.path.dirname(__file__), "backend", ".env")
load_dotenv(ENV_PATH)

print("RUN ENV TEST:", os.getenv("MONGO_URI"))

from backend.app import create_app

app = create_app()

# ✅ Load verify token from environment (Render)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Forbidden", 403

    if request.method == "POST":
        data = request.json
        print("Incoming WhatsApp message:", data)
        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
