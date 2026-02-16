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
from .routes.webhook_routes import webhook_bp  


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correct .env path (project root)
ENV_PATH = os.path.join(BASE_DIR, ".env")


def create_app():

    # Load ENV FIRST
    load_dotenv(ENV_PATH)

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
        static_folder=os.path.join(BASE_DIR, "frontend", "static")
    )

    # Load config AFTER env
    app.config.from_object(config)

    # Enable CORS
    CORS(app)

    print("VERIFY_TOKEN loaded:", bool(os.getenv("VERIFY_TOKEN")))
   

    # Initialize MongoDB Atlas
    init_mongo(app)

    # Register blueprints AFTER mongo init
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(inquiry_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(webhook_bp)  # Register webhook blueprint
    @app.context_processor
    def inject_user():
        from flask import session
        return dict(current_user=session.get("user"))


    @app.after_request
    def disable_cache(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app
