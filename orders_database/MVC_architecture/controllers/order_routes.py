from flask import Blueprint, jsonify, request

from .order_controllers import order_controller

order_blueprint = Blueprint("orders", __name__, url_prefix="/orders")


@order_blueprint.route("/", methods=["GET"])
def get_orders():
    return jsonify(order_controller.get_all_orders()), 200


@order_blueprint.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = order_controller.get_order(order_id)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404


@order_blueprint.route("/", methods=["POST"])
def place_order():
    data = request.json or {}
    created = order_controller.place_order(data)
    return jsonify(created), 201


@order_blueprint.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.json or {}
    updated = order_controller.update_order(order_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Order not found"}), 404


@order_blueprint.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    deleted = order_controller.delete_order(order_id)
    if deleted:
        return jsonify({"message": "Order deleted"}), 200
    return jsonify({"error": "Order not found"}), 404
