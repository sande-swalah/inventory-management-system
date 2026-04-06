from functools import wraps
from flask import Blueprint, jsonify, request

from .user_controllers import user_controller
from ..user_validators.user_validators import (
    validate_login_data,
    validate_registration_data,
    validate_update_data,
)


user_blueprint = Blueprint("users", __name__)


# def require_roles(*roles):
#     """Decorator to check if user has required roles."""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             role = request.args.get("role")
#             print(f"Required roles: {roles}")
#             if role not in roles:
#                 return jsonify({"error": "Unauthorized"}), 403
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator


@user_blueprint.route("/users", methods=["GET"])
# @require_roles("manager", "staff", "admin")
def get_all_users():
    return jsonify(user_controller.get_all_users()), 200


@user_blueprint.route("/users/register", methods=["POST"])
def register_user():
    print("registering user")
    data = request.json or {}
    print(f"this is user data: {data}")

    is_valid, errors = validate_registration_data(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    created_user = user_controller.register(data)
    return jsonify(created_user), 201


@user_blueprint.route("/users/login", methods=["POST"])
def login_user():
    data = request.json or {}
    print(f"This is login data: {data}")

    is_valid, errors = validate_login_data(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    user = user_controller.login(data)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify(user), 200

@user_blueprint.route("/users/<user_id>", methods=["GET"])
# @require_roles("manager", "staff", "admin")
def get_user(user_id):
    user = user_controller.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "user not found"}), 404


@user_blueprint.route("/users/<user_id>", methods=["PUT"])
# @require_roles("manager", "admin")
def update_user(user_id):
    print(f"Updating user with id: {user_id}")
    data = request.json or {}
    print(f"Update data: {data}")

    is_valid, errors = validate_update_data(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    updated_user = user_controller.update(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({"error": "user not found or update failed"}), 404


