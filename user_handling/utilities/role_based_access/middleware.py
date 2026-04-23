from functools import wraps
from flask import jsonify, request
from user_handling.MVC_architecture.controllers.user_controllers import user_controller
from user_handling.utilities.tokens.blcklist import is_token_blacklisted
from user_handling.utilities.tokens.jwt import decode_token


def _normalize_bearer_token(auth_header):
    if not auth_header:
        return ""

    token = auth_header.strip()
    if token.lower().startswith("bearer "):
        token = token.split(" ", 1)[1].strip()

    # Be tolerant of users pasting `Bearer <token>` into Postman's Bearer Token field.
    if token.lower().startswith("bearer "):
        token = token.split(" ", 1)[1].strip()

    return token.strip().strip('"').strip("'")


def _get_authenticated_user():
    auth_header = request.headers.get("Authorization", "")
    token = _normalize_bearer_token(auth_header)
    if token:
        if not token:
            return None, {"error": "Authentication required"}, 401

        try:
            payload = decode_token(token)
        except ValueError as err:
            return None, {"error": str(err)}, 401

        jti = payload.get("jti")
        if jti and is_token_blacklisted(jti):
            return None, {"error": "Token has been revoked"}, 401

        user_id = payload.get("sub")
        if not user_id:
            return None, {"error": "Invalid token payload"}, 401

        user = user_controller.get_user(user_id)
        if not user:
            return None, {"error": "Invalid user"}, 401

        return user, None, None

    user_id = request.headers.get("user_id")
    if not user_id:
        return None, {"error": "Authentication required"}, 401

    user = user_controller.get_user(user_id)
    if not user:
        return None, {"error": "Invalid user"}, 401

    return user, None, None


def required_roles(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user, error_body, status_code = _get_authenticated_user()
            if not user:
                return jsonify(error_body), status_code

            user_roles = user.get("roles", [])
            if isinstance(user_roles, str):
                user_roles = [user_roles]

            normalized_roles = set()
            for role in user_roles:
                role_text = str(role).lower()
                if "." in role_text:
                    role_text = role_text.split(".")[-1]
                normalized_roles.add(role_text)

            if not any(role.lower() in normalized_roles for role in roles):
                return jsonify({"error": "Unauthorized"}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator