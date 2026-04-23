from flask import Blueprint, jsonify, request
from .product_controllers import product_controller

product_blueprint = Blueprint("products", __name__, url_prefix="/products")


@product_blueprint.route("/", methods=["GET"])
def get_products():
    return jsonify(product_controller.get_all_products()), 200


@product_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = product_controller.get_product(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


@product_blueprint.route("", methods=["POST"])
@product_blueprint.route("/", methods=["POST"])
def create_product():
    data = request.json or {}
    created = product_controller.add_product(data)
    return jsonify(created), 201


@product_blueprint.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json or {}
    updated = product_controller.update_product(product_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Product not found"}), 404


@product_blueprint.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    deleted = product_controller.delete_product(product_id)
    if deleted:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404
