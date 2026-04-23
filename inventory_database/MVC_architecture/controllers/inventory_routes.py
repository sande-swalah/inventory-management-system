from flask import Blueprint, jsonify, request
from user_handling.utilities.role_based_access.middleware import required_roles
from .inventory_controllers import inventory_controller

inventory_blueprint = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_blueprint.route("/items", methods=["GET"])
def list_inventory():
    return jsonify(inventory_controller.get_all_items()), 200


@inventory_blueprint.route("/products", methods=["GET"])
def list_inventory_products():
    return jsonify(inventory_controller.get_inventory_products()), 200


@inventory_blueprint.route("/items/<int:item_id>", methods=["GET"])
@required_roles("manager", "staff", "admin")
def get_inventory_item(item_id):
    item = inventory_controller.get_item(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@inventory_blueprint.route("/items", methods=["POST"])
@required_roles("manager", "staff", "admin")
def create_inventory_item():
    data = request.json or {}
    try:
        created = inventory_controller.add_item(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(created), 201


@inventory_blueprint.route("/items/<int:item_id>", methods=["PUT"])
@required_roles("manager", "staff", "admin")
def update_inventory_item(item_id):
    data = request.json or {}
    try:
        updated = inventory_controller.update_item(item_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Item not found"}), 404


@inventory_blueprint.route("/items/<int:item_id>", methods=["DELETE"])
@required_roles("manager", "staff", "admin")
def delete_inventory_item(item_id):
    deleted = inventory_controller.delete_item(item_id)
    if deleted:
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404
