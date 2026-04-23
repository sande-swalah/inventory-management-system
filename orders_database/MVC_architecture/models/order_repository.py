from extensions import db
from sqlalchemy.exc import IntegrityError, StatementError
from orders_database.MVC_architecture.models.order_domain import Order_Data
from orders_database.MVC_architecture.models.order_schema import OrderSchema
from products_database.MVC_architecture.models.product_domain import Product_Data


class OrderRepository:
    def __init__(self):
        self.schema = OrderSchema()
        self.list_schema = OrderSchema(many=True)

    def fetch_all_orders(self):
        orders = Order_Data.query.order_by(Order_Data.id.asc()).all()
        return self.list_schema.dump(orders)

    def fetch_order(self, order_id):
        order = db.session.get(Order_Data, int(order_id))
        return self.schema.dump(order) if order else None

    def create_order(self, data):
        payload = {k: v for k, v in data.items() if k != "product_ids"}
        order = Order_Data(**payload)

        if isinstance(data.get("product_ids"), list):
            products = Product_Data.query.filter(Product_Data.id.in_(data["product_ids"])).all()
            order.products = products
            if products and not payload.get("product_id"):
                order.product_id = products[0].id

        db.session.add(order)
        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid order data")
        return self.schema.dump(order)

    def update_order(self, order_id, data):
        order = db.session.get(Order_Data, int(order_id))
        if not order:
            return None

        for field, value in data.items():
            if field == "product_ids":
                continue
            setattr(order, field, value)

        if isinstance(data.get("product_ids"), list):
            products = Product_Data.query.filter(Product_Data.id.in_(data["product_ids"])).all()
            order.products = products
            if products and not data.get("product_id"):
                order.product_id = products[0].id

        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid order data")
        return self.schema.dump(order)

    def delete_order(self, order_id):
        order = db.session.get(Order_Data, int(order_id))
        if not order:
            return False

        db.session.delete(order)
        db.session.commit()
        return True
