from flask import Flask, jsonify

from user_handling.MVC_architecture.controllers.user_routes import user_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_blueprint, url_prefix="/api")

    @app.get("/")
    def start_up():
        return jsonify({"app is starting"}), 200

    return app


app = create_app()


if __name__ == "__main__":
    print("running")
    app.run()