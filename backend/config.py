import os
import dns.resolver
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_TLS = True
MONGO_TLS_ALLOW_INVALID_CERTIFICATES = True
APP_NAME = "Homecart AI Agent"
UPLOAD_FOLDER = os.path.join("frontend", "static", "uploads")
DEBUG = True

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
