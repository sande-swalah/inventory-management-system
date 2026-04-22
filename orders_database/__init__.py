def register_blueprints(app):
    from orders_database.MVC_architecture.controllers.order_routes import order_blueprint

    app.register_blueprint(order_blueprint, url_prefix="/api")