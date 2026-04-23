from datetime import datetime

from ..models.order_repository import OrderRepository


class OrderService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_orders(self):
        return self.repo.fetch_all_orders()

    def get_order(self, order_id):
        return self.repo.fetch_order(order_id)

    def place_order(self, data):
        order = {
            "product_id": data["product_id"],
            "user_id": data.get("user_id"),
            "product_ids": data.get("product_ids", [data["product_id"]]),
            "quantity": data["quantity"],
            "order_value": data.get("order_value", 0),
            "status": data.get("status", "pending"),
            "expected_delivery": data.get("expected_delivery"),
            "created_on": datetime.now().isoformat(),
        }
        return self.repo.create_order(order)

    def update_order(self, order_id, data):
        return self.repo.update_order(order_id, data)

    def remove_order(self, order_id):
        return self.repo.delete_order(order_id)
