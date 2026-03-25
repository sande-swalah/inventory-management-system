from flask import Blueprint, jsonify, request

from .user_controlers import user_controller


user_blueprint = Blueprint("users", __name__)


@user_blueprint.get("/users")
def get_all_users_route():
    return jsonify(user_controller.get_all_users()), 200


@user_blueprint.get("/users/<int:user_id>")
def get_user_route(user_id):
    user = user_controller.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@user_blueprint.post("/users/register")
def register_user_route():
    data = request.get_json(silent=True) or {}
    created_user = user_controller.register(data)
    return jsonify(created_user), 201


@user_blueprint.post("/users/login")
def login_user_route():
    data = request.get_json(silent=True) or {}
    try:
        user = user_controller.login(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify(user), 200


@user_blueprint.put("/users/<int:user_id>")
def update_user_route(user_id):
    data = request.get_json(silent=True) or {}
    updated_user = user_controller.update(user_id, data)
    if not updated_user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(updated_user), 200


@user_blueprint.delete("/users/<int:user_id>")
def delete_user_route(user_id):
    deleted = user_controller.delete(user_id)
    if not deleted:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200


@user_blueprint.post("/users/<int:user_id>/restore")
def restore_user_route(user_id):
    restored_user = user_controller.restore(user_id)
    if not restored_user:
        return jsonify({"error": "User not found in deleted users"}), 404
    return jsonify(restored_user), 200
