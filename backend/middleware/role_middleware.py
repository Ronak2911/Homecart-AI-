from functools import wraps
from flask import request, jsonify


def role_required(allowed_roles):
    """
    Middleware to restrict access based on user role
    Example:
    @role_required(["admin"])
    @role_required(["admin", "staff"])
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # role comes from auth_middleware
            user_role = getattr(request, "user_role", None)

            if not user_role:
                return jsonify({
                    "success": False,
                    "message": "Role information missing"
                }), 403

            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Access denied: Insufficient permission"
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator
