def register_blueprints(app):
    from suppliers_database.MVC_architecture.controllers.supplier_routes import supplier_blueprint

    app.register_blueprint(supplier_blueprint, url_prefix="/api/suppliers")