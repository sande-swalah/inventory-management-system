from flask import Flask, jsonify

from app_setup import register_models
from config.config import Config
from extensions.extensions import db, migrate, ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    
    register_models()
    with app.app_context():
        db.create_all()


    @app.get("/")
    def starting():
        return jsonify({"message": "Inventory management app is running"}), 200

    return app


app = create_app()
