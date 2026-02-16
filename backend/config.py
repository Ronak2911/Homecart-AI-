import os
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_TLS = True
MONGO_TLS_ALLOW_INVALID_CERTIFICATES = True
APP_NAME = "Homecart AI Agent"
UPLOAD_FOLDER = os.path.join("frontend", "static", "uploads")
DEBUG = True


