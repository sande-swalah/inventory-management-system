from flask import Blueprint, jsonify, request

from .supplier_controllers import supplier_controller

supplier_blueprint = Blueprint("suppliers", __name__, url_prefix="/suppliers")


@supplier_blueprint.route("/<int:supplier_id>", methods=["GET"])
def get_suppliers():
    return jsonify(supplier_controller.get_all_suppliers()), 200


@supplier_blueprint.route("/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id):
    supplier = supplier_controller.get_supplier(supplier_id)
    if supplier:
        return jsonify(supplier), 200
    return jsonify({"error": "Supplier not found"}), 404


@supplier_blueprint.route("/", methods=["POST"])
def create_supplier():
    data = request.json or {}
    created = supplier_controller.add_supplier(data)
    return jsonify(created), 201


@supplier_blueprint.route("/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    data = request.json or {}
    updated = supplier_controller.update_supplier(supplier_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Supplier not found"}), 404


@supplier_blueprint.route("/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    deleted = supplier_controller.delete_supplier(supplier_id)
    if deleted:
        return jsonify({"message": "Supplier deleted"}), 200
    return jsonify({"error": "Supplier not found"}), 404
