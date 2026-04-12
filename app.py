from flask import Flask, jsonify

from user_handling.MVC_architecture.controllers.user_routes import user_blueprint
from user_handling.user_database import init_db as init_user_db, init_app as init_user_app

from products_database.MVC_architecture.controllers.product_routes import product_blueprint
from products_database import init_db as init_product_db, init_app as init_product_app

from inventory_database.MVC_architecture.controllers.inventory_routes import inventory_blueprint
from inventory_database import init_db as init_inventory_db, init_app as init_inventory_app

from manage_store_database.MVC_architecture.controllers.store_routes import store_blueprint
from manage_store_database import init_db as init_store_db, init_app as init_store_app

from suppliers_database.MVC_architecture.controllers.supplier_routes import supplier_blueprint
from suppliers_database import init_db as init_supplier_db, init_app as init_supplier_app

from orders_database.MVC_architecture.controllers.order_routes import order_blueprint
from orders_database import init_db as init_order_db, init_app as init_order_app

from reports_database.MVC_architecture.controllers.report_routes import report_blueprint
from reports_database import init_db as init_report_db, init_app as init_report_app


def create_app():
    app = Flask(__name__)
    init_user_db()
    init_user_app(app)

    init_product_db()
    init_product_app(app)

    init_inventory_db()
    init_inventory_app(app)

    init_store_db()
    init_store_app(app)

    init_supplier_db()
    init_supplier_app(app)

    init_order_db()
    init_order_app(app)

    init_report_db()
    init_report_app(app)

    app.register_blueprint(user_blueprint, url_prefix="/api")
    app.register_blueprint(product_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_blueprint, url_prefix="/api")
    app.register_blueprint(store_blueprint, url_prefix="/api")
    app.register_blueprint(supplier_blueprint, url_prefix="/api")
    app.register_blueprint(order_blueprint, url_prefix="/api")
    app.register_blueprint(report_blueprint, url_prefix="/api")

    @app.get("/")
    def starting():
        return "app is starting"

    return app


app = create_app()
