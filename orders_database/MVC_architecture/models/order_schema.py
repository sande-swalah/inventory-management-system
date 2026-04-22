from extensions import ma
from orders_database.MVC_architecture.models.order_domain import Order_Data


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order_Data
        include_fk = True
        load_instance = True
