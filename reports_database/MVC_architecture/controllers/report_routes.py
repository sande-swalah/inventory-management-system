from flask import Blueprint, jsonify, request

from .report_controllers import report_controller

report_blueprint = Blueprint("reports", __name__)


@report_blueprint.route("/reports/summary", methods=["GET"])
def get_report_summary():
    return jsonify(report_controller.get_summary()), 200


@report_blueprint.route("/reports/history", methods=["GET"])
def get_report_history():
    return jsonify(report_controller.get_history()), 200


@report_blueprint.route("/reports/snapshot", methods=["POST"])
def create_report_snapshot():
    data = request.json or {}
    name = data.get("name", "Snapshot")
    created = report_controller.snapshot(name)
    return jsonify(created), 201
