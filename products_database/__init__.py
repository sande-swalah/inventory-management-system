def register_blueprints(app):
    from products_database.MVC_architecture.controllers.product_routes import product_blueprint

    app.register_blueprint(product_blueprint, url_prefix="/api/products")