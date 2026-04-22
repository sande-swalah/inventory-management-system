from flask import Blueprint, jsonify, request

from .report_controllers import report_controller

report_blueprint = Blueprint("reports", __name__)


@report_blueprint.route("/reports", methods=["GET"])
def get_reports():
    return jsonify(report_controller.get_all_reports()), 200


@report_blueprint.route("/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):
    report = report_controller.get_report(report_id)
    if report:
        return jsonify(report), 200
    return jsonify({"error": "Report not found"}), 404


@report_blueprint.route("/reports/summary", methods=["GET"])
def get_report_summary():
    return jsonify(report_controller.get_summary()), 200


@report_blueprint.route("/reports/history", methods=["GET"])
def get_report_history():
    return jsonify(report_controller.get_history()), 200


@report_blueprint.route("/reports", methods=["POST"])
@report_blueprint.route("/reports/snapshot", methods=["POST"])
def create_report_snapshot():
    data = request.json or {}
    name = data.get("name", "Snapshot")
    created = report_controller.snapshot(name)
    return jsonify(created), 201


@report_blueprint.route("/reports/<int:report_id>", methods=["PUT"])
def update_report(report_id):
    data = request.json or {}
    updated = report_controller.update_report(report_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Report not found"}), 404


@report_blueprint.route("/reports/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):
    deleted = report_controller.delete_report(report_id)
    if deleted:
        return jsonify({"message": "Report deleted"}), 200
    return jsonify({"error": "Report not found"}), 404
