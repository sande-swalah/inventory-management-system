from flask import Flask, jsonify

from user_handling.MVC_architecture.controllers.user_routes import user_blueprint
from user_handling.user_database import init_db, init_app


def create_app():
    app = Flask(__name__)
    init_db()
    init_app(app)
    app.register_blueprint(user_blueprint, url_prefix="/api")

    @app.get("/")
    def start_up():
        return jsonify({"app is starting"}), 200

    return app


app = create_app()


if __name__ == "__main__":
    print("running")
    app.run()