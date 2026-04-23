
def register_all_blueprints(app):
    from user_handling import register_blueprints as register_user_blueprints
    from inventory_database import register_blueprints as register_inventory_blueprints
    from products_database import register_blueprints as register_product_blueprints
    from orders_database import register_blueprints as register_order_blueprints
    from manage_store_database import register_blueprints as register_store_blueprints
    from suppliers_database import register_blueprints as register_supplier_blueprints
    from reports_database import register_blueprints as register_report_blueprints

    register_user_blueprints(app)
    register_inventory_blueprints(app)
    register_product_blueprints(app)
    register_order_blueprints(app)
    register_store_blueprints(app)
    register_supplier_blueprints(app)
    register_report_blueprints(app)
