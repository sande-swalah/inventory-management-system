from flask import Blueprint, jsonify, request
from user_handling.utilities.role_based_access.middleware import required_roles
from .store_controllers import store_controller

store_blueprint = Blueprint("stores", __name__, url_prefix="/stores")


@store_blueprint.route("/", methods=["GET"])
def get_stores():
    return jsonify(store_controller.get_all_stores()), 200


@store_blueprint.route("/<int:store_id>", methods=["GET"])
@required_roles("manager", "staff", "admin")
def get_store(store_id):
    store = store_controller.get_store(store_id)
    if store:
        return jsonify(store), 200
    return jsonify({"error": "Store not found"}), 404


@store_blueprint.route("/", methods=["POST"])
@required_roles("manager", "staff", "admin")
def create_store():
    data = request.json or {}
    try:
        created = store_controller.add_store(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(created), 201


@store_blueprint.route("/<int:store_id>", methods=["PUT"])
@required_roles("manager", "staff", "admin")
def update_store(store_id):
    data = request.json or {}
    try:
        updated = store_controller.update_store(store_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Store not found"}), 404


@store_blueprint.route("/<int:store_id>", methods=["DELETE"])
@required_roles("manager", "staff", "admin")
def delete_store(store_id):
    deleted = store_controller.delete_store(store_id)
    if deleted:
        return jsonify({"message": "Store deleted"}), 200
    return jsonify({"error": "Store not found"}), 404
