def register_blueprints(app):
    from inventory_database.MVC_architecture.controllers.inventory_routes import inventory_blueprint

    app.register_blueprint(inventory_blueprint, url_prefix="/api/inventory")