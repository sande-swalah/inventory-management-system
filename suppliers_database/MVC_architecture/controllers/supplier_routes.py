from flask import Blueprint, jsonify, request
from user_handling.utilities.role_based_access.middleware import required_roles
from user_handling.MVC_architecture.controllers.user_controllers import user_controller
from user_handling.utilities.tokens.jwt import decode_token

from .supplier_controllers import supplier_controller

supplier_blueprint = Blueprint("suppliers", __name__, url_prefix="/suppliers")


def _get_requester():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip().strip('"').strip("'")
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
            requester = user_controller.get_user(user_id) if user_id else None
            if requester:
                return requester
        except ValueError:
            return None

    requester_id = request.headers.get("user_id")
    return user_controller.get_user(requester_id) if requester_id else None


@supplier_blueprint.route("", methods=["GET"])
@supplier_blueprint.route("/", methods=["GET"])
@supplier_blueprint.route("/all", methods=["GET"])
@required_roles("manager", "staff", "admin", "supplier","user")
def get_suppliers():
    return jsonify(supplier_controller.get_all_suppliers()), 200


@supplier_blueprint.route("/<int:supplier_id>", methods=["GET"])
@required_roles("manager", "staff", "admin", "supplier","user")
def get_supplier(supplier_id):
    supplier = supplier_controller.get_supplier(supplier_id)
    if supplier:
        return jsonify(supplier), 200
    return jsonify({"error": "Supplier not found"}), 404


@supplier_blueprint.route("/", methods=["POST"])
@required_roles("manager", "staff", "admin", "supplier")
def create_supplier():
    data = request.json or {}

    requester = _get_requester()
    if not requester:
        return jsonify({"error": "Authentication required"}), 401

    requester_role = str(requester.get("roles", "")).lower()
    if "." in requester_role:
        requester_role = requester_role.split(".")[-1]

    if requester_role == "supplier":
        requester_email = requester.get("email")
        if not requester_email:
            return jsonify({"error": "Supplier account has no email"}), 400

        existing = supplier_controller.get_all_suppliers()
        for supplier in existing:
            owner_email = supplier.get("user_email") or supplier.get("email")
            if owner_email == requester_email:
                return jsonify({"error": "Supplier profile already exists for this account"}), 400

        # Bind supplier profile ownership to logged-in supplier.
        data["user_email"] = requester_email

    try:
        created = supplier_controller.add_supplier(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(created), 201


@supplier_blueprint.route("/<int:supplier_id>", methods=["PUT"])
@required_roles("manager", "staff", "admin", "supplier")
def update_supplier(supplier_id):
    data = request.json or {}

    requester = _get_requester()
    if not requester:
        return jsonify({"error": "Authentication required"}), 401

    requester_role = str(requester.get("roles", "")).lower()
    if "." in requester_role:
        requester_role = requester_role.split(".")[-1]

    # Suppliers can only update their own profile. Privileged roles can update any supplier.
    if requester_role == "supplier":
        supplier = supplier_controller.get_supplier(supplier_id)
        if not supplier:
            return jsonify({"error": "Supplier not found"}), 404

        requester_email = requester.get("email")
        owner_email = supplier.get("user_email") or supplier.get("email")
        if not requester_email or requester_email != owner_email:
            return jsonify({"error": "You can only update your own supplier profile"}), 403

    try:
        updated = supplier_controller.update_supplier(supplier_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Supplier not found"}), 404


@supplier_blueprint.route("/<int:supplier_id>", methods=["DELETE"])
@required_roles("manager", "staff", "admin", "supplier")
def delete_supplier(supplier_id):
    requester = _get_requester()
    if not requester:
        return jsonify({"error": "Authentication required"}), 401

    requester_role = str(requester.get("roles", "")).lower()
    if "." in requester_role:
        requester_role = requester_role.split(".")[-1]

    if requester_role == "supplier":
        supplier = supplier_controller.get_supplier(supplier_id)
        if not supplier:
            return jsonify({"error": "Supplier not found"}), 404

        requester_email = requester.get("email")
        owner_email = supplier.get("user_email") or supplier.get("email")
        if not requester_email or requester_email != owner_email:
            return jsonify({"error": "You can only delete your own supplier profile"}), 403

    deleted = supplier_controller.delete_supplier(supplier_id)
    if deleted:
        return jsonify({"message": "Supplier deleted"}), 200
    return jsonify({"error": "Supplier not found"}), 404
