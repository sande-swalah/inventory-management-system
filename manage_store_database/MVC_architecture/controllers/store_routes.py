from flask import Blueprint, jsonify, request

from .store_controllers import store_controller

store_blueprint = Blueprint("stores", __name__)


@store_blueprint.route("/stores", methods=["GET"])
def get_stores():
    return jsonify(store_controller.get_all_stores()), 200


@store_blueprint.route("/stores", methods=["POST"])
def create_store():
    data = request.json
    created = store_controller.add_store(data)
    return jsonify(created), 201
