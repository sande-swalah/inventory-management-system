def register_models():
    from inventory_database.MVC_architecture.models.inventory_domain import Inventory_Data
    from manage_store_database.MVC_architecture.models.store_domain import Store_Data  
    from orders_database.MVC_architecture.models.order_domain import Order_Data 
    from products_database.MVC_architecture.models.product_domain import Product_Data  
    from reports_database.MVC_architecture.models.report_domain import Report_Data  
    from suppliers_database.MVC_architecture.models.supplier_domain import Supplier_Data 
    from user_handling.MVC_architecture.models.user_domain.user_domain import User_Data
