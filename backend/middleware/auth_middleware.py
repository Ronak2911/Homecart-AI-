from functools import wraps
from flask import request, jsonify, current_app, session, redirect, url_for
import jwt


def auth_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        # ============================
        # 1️⃣ SESSION AUTH (WEB)
        # ============================
        if "user_id" in session:
            request.user_id = session.get("user_id")
            request.user_role = session.get("role")
            return func(*args, **kwargs)

        # ============================
        # 2️⃣ JWT AUTH (API)
        # ============================
        token = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:

            # Browser request → redirect
            if request.accept_mimetypes.accept_html:
                return redirect(url_for("auth.login"))

            # API request → JSON error
            return jsonify({
                "success": False,
                "message": "Authentication token missing"
            }), 401

        try:
            decoded_data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            request.user_id = decoded_data.get("user_id")
            request.user_role = decoded_data.get("role")

        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "message": "Token expired"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 401

        return func(*args, **kwargs)

    return wrapper
