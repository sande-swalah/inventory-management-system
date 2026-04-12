from flask import Blueprint, jsonify, request

from .supplier_controllers import supplier_controller

supplier_blueprint = Blueprint("suppliers", __name__)


@supplier_blueprint.route("/suppliers", methods=["GET"])
def get_suppliers():
    return jsonify(supplier_controller.get_all_suppliers()), 200


@supplier_blueprint.route("/suppliers", methods=["POST"])
def create_supplier():
    data = request.json or {}
    created = supplier_controller.add_supplier(data)
    return jsonify(created), 201
