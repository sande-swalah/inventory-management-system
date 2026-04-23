from flask import Blueprint, jsonify, request

from .store_controllers import store_controller

store_blueprint = Blueprint("stores", __name__, url_prefix="/stores")


@store_blueprint.route("/", methods=["GET"])
def get_stores():
    return jsonify(store_controller.get_all_stores()), 200


@store_blueprint.route("/<int:store_id>", methods=["GET"])
def get_store(store_id):
    store = store_controller.get_store(store_id)
    if store:
        return jsonify(store), 200
    return jsonify({"error": "Store not found"}), 404


@store_blueprint.route("/", methods=["POST"])
def create_store():
    data = request.json or {}
    created = store_controller.add_store(data)
    return jsonify(created), 201


@store_blueprint.route("/stores/<int:store_id>", methods=["PUT"])
def update_store(store_id):
    data = request.json or {}
    updated = store_controller.update_store(store_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Store not found"}), 404


@store_blueprint.route("/stores/<int:store_id>", methods=["DELETE"])
def delete_store(store_id):
    deleted = store_controller.delete_store(store_id)
    if deleted:
        return jsonify({"message": "Store deleted"}), 200
    return jsonify({"error": "Store not found"}), 404
