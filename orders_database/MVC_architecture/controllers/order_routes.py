from flask import Blueprint, jsonify, request

from .order_controllers import order_controller

order_blueprint = Blueprint("orders", __name__)


@order_blueprint.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(order_controller.get_all_orders()), 200


@order_blueprint.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = order_controller.get_order(order_id)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404


@order_blueprint.route("/orders", methods=["POST"])
def place_order():
    data = request.json or {}
    created = order_controller.place_order(data)
    return jsonify(created), 201
