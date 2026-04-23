from flask import Blueprint, jsonify, request
from user_handling.utilities.role_based_access.middleware import required_roles
from user_handling.MVC_architecture.controllers.user_controllers import user_controller
from user_handling.utilities.tokens.jwt import decode_token
from .order_controllers import order_controller

order_blueprint = Blueprint("orders", __name__, url_prefix="/orders")


def _requester_context():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip().strip('"').strip("'")
        try:
            payload = decode_token(token)
            requester_id = payload.get("sub")
            requester = user_controller.get_user(requester_id) if requester_id else None
            if requester:
                role_text = str(requester.get("roles", "")).lower()
                if "." in role_text:
                    role_text = role_text.split(".")[-1]
                return str(requester_id), role_text
        except ValueError:
            return None, None

    requester_id = request.headers.get("user_id")
    requester = user_controller.get_user(requester_id) if requester_id else None
    if not requester:
        return None, None

    role_text = str(requester.get("roles", "")).lower()
    if "." in role_text:
        role_text = role_text.split(".")[-1]

    return requester_id, role_text


@order_blueprint.route("/", methods=["GET"])
@required_roles("manager", "staff", "admin")
def get_orders():
    requester_id, requester_role = _requester_context()
    if not requester_id:
        return jsonify({"error": "Authentication required"}), 401

    orders = order_controller.get_all_orders()
    if requester_role == "user":
        orders = [order for order in orders if str(order.get("user_id")) == str(requester_id)]

    return jsonify(orders), 200


@order_blueprint.route("/<int:order_id>", methods=["GET"])
@required_roles("manager", "staff", "admin", "user")
def get_order(order_id):
    requester_id, requester_role = _requester_context()
    if not requester_id:
        return jsonify({"error": "Authentication required"}), 401

    order = order_controller.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    if requester_role == "user" and str(order.get("user_id")) != str(requester_id):
        return jsonify({"error": "You can only access your own orders"}), 403

    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404


@order_blueprint.route("/", methods=["POST"])
@required_roles("manager", "staff", "admin", "user")
def place_order():
    data = request.json or {}
    requester_id, requester_role = _requester_context()
    if not requester_id:
        return jsonify({"error": "Authentication required"}), 401

    # A user must place orders only for themselves.
    if requester_role == "user":
        data["user_id"] = int(requester_id)

    try:
        created = order_controller.place_order(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(created), 201


@order_blueprint.route("/<int:order_id>", methods=["PUT"])
@required_roles("manager", "staff", "admin", "user")
def update_order(order_id):
    data = request.json or {}
    requester_id, requester_role = _requester_context()
    if not requester_id:
        return jsonify({"error": "Authentication required"}), 401

    if requester_role == "user":
        order = order_controller.get_order(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        if str(order.get("user_id")) != str(requester_id):
            return jsonify({"error": "You can only update your own order"}), 403

    try:
        updated = order_controller.update_order(order_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Order not found"}), 404


@order_blueprint.route("/<int:order_id>", methods=["DELETE"])
@required_roles("manager", "staff", "admin", "user")
def delete_order(order_id):
    requester_id, requester_role = _requester_context()
    if not requester_id:
        return jsonify({"error": "Authentication required"}), 401

    if requester_role == "user":
        order = order_controller.get_order(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        if str(order.get("user_id")) != str(requester_id):
            return jsonify({"error": "You can only delete your own order"}), 403

    deleted = order_controller.delete_order(order_id)
    if deleted:
        return jsonify({"message": "Order deleted"}), 200
    return jsonify({"error": "Order not found"}), 404
