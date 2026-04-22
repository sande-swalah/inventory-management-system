from extensions import db
from orders_database.MVC_architecture.models.order_domain import Order_Data
from orders_database.MVC_architecture.models.order_schema import OrderSchema


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
        order = Order_Data(**data)
        db.session.add(order)
        db.session.commit()
        return self.schema.dump(order)

    def update_order(self, order_id, data):
        order = db.session.get(Order_Data, int(order_id))
        if not order:
            return None

        for field, value in data.items():
            setattr(order, field, value)

        db.session.commit()
        return self.schema.dump(order)

    def delete_order(self, order_id):
        order = db.session.get(Order_Data, int(order_id))
        if not order:
            return False

        db.session.delete(order)
        db.session.commit()
        return True
