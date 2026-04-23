from functools import wraps
from flask import jsonify, request
from user_handling.MVC_architecture.controllers.user_controllers import user_controller


def required_roles(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = request.headers.get("user_id")
            if not user_id:
                return jsonify({"error": "Authentication required"}), 401

            user = user_controller.get_user(user_id)
            # if not user:
            #     return jsonify({"error": "no user with that name"}), 401

            user_roles = user.get("roles", [])
            if isinstance(user_roles):
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