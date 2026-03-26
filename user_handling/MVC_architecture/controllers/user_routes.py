from flask import Blueprint, jsonify, request

from .user_controllers import user_controller


user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(user_controller.get_all_users()), 200


@user_blueprint.route("/users/register", methods=["POST"])
def register_user():
    print("registering user")
    data = request.json
    print(f"this is user data: {data}")



    created_user = user_controller.register(data)
    return jsonify(created_user), 201


@user_blueprint.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    print(f"This is login data: {data}")
    email = data.get("email")
    password = data.get("password")

    user = user_controller.login(data)
    
    return jsonify(user), 200
