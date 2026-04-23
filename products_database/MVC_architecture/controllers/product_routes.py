from flask import Blueprint, jsonify, request
from .product_controllers import product_controller
from user_handling.utilities.role_based_access.middleware import required_roles

product_blueprint = Blueprint("products", __name__, url_prefix="/products")


@product_blueprint.route("/", methods=["GET"])

def get_products():
    return jsonify(product_controller.get_all_products()), 200


@product_blueprint.route("/<int:product_id>", methods=["GET"])
@required_roles("manager", "staff", "admin")
def get_product(product_id):
    product = product_controller.get_product(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404



@product_blueprint.route("", methods=["POST"])
@product_blueprint.route("/", methods=["POST"])
@product_blueprint.route("/create_product", methods=["POST"])
@required_roles("manager", "staff", "admin", "supplier")
def create_product():
    data = request.json or {}
    try:
        created = product_controller.add_product(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(created), 201


@product_blueprint.route("/<int:product_id>", methods=["PUT"])
@required_roles("manager", "staff", "admin", "supplier")
def update_product(product_id):
    data = request.json or {}
    try:
        updated = product_controller.update_product(product_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Product not found"}), 404


@product_blueprint.route("/<int:product_id>", methods=["DELETE"])
@required_roles("manager", "staff", "admin", "supplier")
def delete_product(product_id):
    deleted = product_controller.delete_product(product_id)
    if deleted:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404
