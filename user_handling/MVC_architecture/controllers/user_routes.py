from functools import wraps
from flask import Blueprint, jsonify, request
from user_handling.utilities.role_based_access.middleware import required_roles

from .user_controllers import user_controller
from ..user_validators.user_validators import (
    validate_login_data,
    validate_registration_data,
    validate_update_data,
)

user_blueprint = Blueprint("users", __name__, url_prefix="/users")



# def require_roles(*roles):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             user_id = request.headers.get("X-User-Id") or request.headers.get("user_id")
#             if not user_id:
#                 return jsonify({"error": "Authentication required"}), 401

#             user = user_controller.get_user(user_id)
#             if not user:
#                 return jsonify({"error": "User not found"}), 404

#             user_roles = user.get("roles", [])
#             if not any(role in user_roles for role in roles):
#                 return jsonify({"error": "Unauthorized"}), 403

#             return func(*args, **kwargs)
#         return wrapper
#     return decorator


@user_blueprint.route("/")
def home():
    return jsonify("You are currently in guest mode")



@user_blueprint.route("/welcome", methods=["GET"])
def welcome_user():
    return jsonify("welcome to the app, would you like to register or login")



@user_blueprint.route("/all", methods=["GET"])
@required_roles("manager", "staff", "admin")
def get_all_users():
    return jsonify(user_controller.get_all_users()), 200


@user_blueprint.route("/register", methods=["POST"])
def register_user():
    print("registering user")
    data = request.json or {}
    print(f"this is user data: {data}")

    is_valid, errors = validate_registration_data(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    created_user = user_controller.register(data)
    return jsonify(created_user), 201


@user_blueprint.route("/login", methods=["POST"])
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

@user_blueprint.route("/<user_id>", methods=["GET"])
@required_roles("manager", "staff", "admin")
def get_user(user_id):
    user = user_controller.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "user not found"}), 404


@user_blueprint.route("/<user_id>", methods=["PUT"])
@required_roles("manager", "admin")
def update_user(user_id):
    data = request.json or {}

    is_valid, errors = validate_update_data(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    updated_user = user_controller.update(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({"error": "user not found or update failed"}), 404


@user_blueprint.route("/<user_id>", methods=["DELETE"])
@required_roles("manager", "admin")
def delete_user(user_id):
    deleted = user_controller.delete(user_id)
    if deleted:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "user not found"}), 404


@user_blueprint.route("/<user_id>/restore", methods=["PATCH"])
@required_roles("manager", "admin")
def restore_user(user_id):
    restored = user_controller.restore(user_id)
    if restored:
        return jsonify({"message": "User restored"}), 200
    return jsonify({"error": "user not found"}), 404


    


