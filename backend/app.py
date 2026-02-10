import os
from flask import Flask, url_for, redirect
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
from .routes.webhook_routes import webhook_bp   # ✅ IMPORTANT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


def create_app():
    load_dotenv(ENV_PATH)

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
        static_folder=os.path.join(BASE_DIR, "frontend", "static")
    )

    app.config.from_object(config)
    CORS(app)

    print("VERIFY_TOKEN loaded:", bool(os.getenv("VERIFY_TOKEN")))

    init_mongo(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(inquiry_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(webhook_bp)  # ✅ THIS MAKES /webhook LIVE


    @app.before_request
def allow_webhook_without_redirect():
    if request.path == "/webhook":
        return None


    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app   # ✅ MUST BE HERE
