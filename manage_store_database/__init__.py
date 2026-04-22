def register_blueprints(app):
    from manage_store_database.MVC_architecture.controllers.store_routes import store_blueprint

    app.register_blueprint(store_blueprint, url_prefix="/api")