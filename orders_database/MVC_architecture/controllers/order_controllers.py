from ..models.order_repository import OrderRepository
from ..services.order_service import OrderService


class OrderController:
    def __init__(self, service):
        self.service = service

    def get_all_orders(self):
        return self.service.get_all_orders()

    def get_order(self, order_id):
        return self.service.get_order(order_id)

    def place_order(self, data):
        return self.service.place_order(data)


order_repository = OrderRepository()
order_service = OrderService(order_repository)
order_controller = OrderController(order_service)
