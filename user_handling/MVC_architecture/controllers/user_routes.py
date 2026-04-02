from functools import wraps
from flask import Blueprint, jsonify, request

from .user_controllers import user_controller


user_blueprint = Blueprint("users", __name__)


def require_roles(*roles):
    """Decorator to check if user has required roles."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get user_id from header or query param
            user_id = request.args.get("user_id")

            if not user_id:
                return jsonify({"error": "user_id missing in header or query param"}), 401

           
            return func(*args, **kwargs)
        return wrapper
    return decorator


@user_blueprint.route("/users", methods=["GET"])
@require_roles("manager", "staff", "admin")
def get_all_users():
    return jsonify(user_controller.get_all_users()), 200


@user_blueprint.route("/users/register", methods=["POST"])
def register_user():
    print("registering user")
    data = request.json
    print(f"this is user data: {data}")

    created_user = user_controller.register(data)
    return jsonify(created_user), 201


@user_blueprint.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    print(f"This is login data: {data}")
    email = data.get("email")
    password = data.get("password")

    user = user_controller.login(data)

    return jsonify(user), 200

@user_blueprint.route("/users/<int:user_id>", methods=["GET"])
@require_roles("manager", "staff", "admin")
def get_user(user_id):
    user = user_controller.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "user not found"}), 404


@user_blueprint.route("/users/<int:user_id>", methods=["PUT"])
@require_roles("manager", "admin")
def update_user(user_id):
    data = request.json
    updated_user = user_controller.update(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({"error": "user not found or update failed"}), 404


@user_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
@require_roles("manager", "admin")
def delete_user(user_id):
    success = user_controller.delete(user_id)
    if success:
        return jsonify({"message": "user deleted successfully"}), 200
    return jsonify({"error": "user not found or delete failed"}), 404


@user_blueprint.route("/users/<int:user_id>/restore", methods=["POST"])
@require_roles("manager", "admin")
def restore_user(user_id):
    success = user_controller.restore(user_id)
    if success:
        return jsonify({"message": "user restored successfully"}), 200
    return jsonify({"error": "user not found or restore failed"}), 404