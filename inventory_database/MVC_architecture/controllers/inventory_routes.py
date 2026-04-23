from flask import Blueprint, jsonify, request

from .inventory_controllers import inventory_controller

inventory_blueprint = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_blueprint.route("/items", methods=["GET"])
def list_inventory():
    return jsonify(inventory_controller.get_all_items()), 200


@inventory_blueprint.route("/products", methods=["GET"])
def list_inventory_products():
    return jsonify(inventory_controller.get_inventory_products()), 200


@inventory_blueprint.route("/items/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = inventory_controller.get_item(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@inventory_blueprint.route("/items", methods=["POST"])
def create_inventory_item():
    data = request.json or {}
    created = inventory_controller.add_item(data)
    return jsonify(created), 201


@inventory_blueprint.route("/items/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    data = request.json or {}
    updated = inventory_controller.update_item(item_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Item not found"}), 404


@inventory_blueprint.route("/items/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    deleted = inventory_controller.delete_item(item_id)
    if deleted:
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404
