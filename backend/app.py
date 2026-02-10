import os
from flask import Flask, url_for, redirect, request
from dotenv import load_dotenv
from flask_cors import CORS

from . import config
from .database.mongodb import init_mongo

from .routes.auth_routes import auth_bp
from .routes.admin_routes import admin_bp
from .routes.property_routes import property_bp
from .routes.staff_routes import staff_bp
from .routes.inquiry_routes import inquiry_bp
from .routes.settings_routes import settings_bp
from .routes.visit_routes import visit_bp
from .routes.dashboard_routes import dashboard_bp

# ==========================
# Paths
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


def create_app():

    # ==========================
    # Load ENV
    # ==========================
    load_dotenv(ENV_PATH)

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
        static_folder=os.path.join(BASE_DIR, "frontend", "static")
    )

    # ==========================
    # Config & CORS
    # ==========================
    app.config.from_object(config)
    CORS(app)

    # Debug (safe)
    print("Mongo URI Loaded:", bool(os.getenv("MONGO_URI")))

    # ==========================
    # MongoDB Init
    # ==========================
    init_mongo(app)

    # ==========================
    # Register Blueprints
    # ==========================
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(inquiry_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(dashboard_bp)

    # ==========================
    # Context Processor
    # ==========================
    @app.context_processor
    def inject_user():
        from flask import session
        return dict(current_user=session.get("user"))

    # ==========================
    # Disable Cache
    # ==========================
    @app.after_request
    def disable_cache(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    # ==========================
    # Home Route
    # ==========================
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    # ==========================
    # WhatsApp Webhook ✅
    # ==========================
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

    @app.route("/webhook", methods=["GET", "POST"])
    def whatsapp_webhook():

        # Meta verification
        if request.method == "GET":
            mode = request.args.get("hub.mode")
            token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")

            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            return "Forbidden", 403

        # Incoming WhatsApp messages
        if request.method == "POST":
            print("Incoming WhatsApp message:", request.json)
            return "EVENT_RECEIVED", 200

    return app
