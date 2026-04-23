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
        product_id = data.get("product_id")
        if product_id is None:
            raise ValueError("product_id is required")

        quantity = data.get("quantity")
        if quantity is None:
            raise ValueError("quantity is required")

        order = {
            "product_id": product_id,
            "user_id": data.get("user_id"),
            "product_ids": data.get("product_ids", [product_id]),
            "quantity": quantity,
            "order_value": data.get("order_value", 0),
            "status": data.get("status", "pending"),
            "expected_delivery": data.get("expected_delivery"),
            "created_on": datetime.utcnow(),
        }
        return self.repo.create_order(order)

    def update_order(self, order_id, data):
        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "product_id",
            "user_id",
            "product_ids",
            "quantity",
            "order_value",
            "status",
            "expected_delivery",
            "created_on",
        }

        payload = {}
        for field, value in data.items():
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

            if field == "created_on" and isinstance(value, str):
                normalized_value = value.replace("Z", "+00:00")
                try:
                    value = datetime.fromisoformat(normalized_value)
                except ValueError as exc:
                    raise ValueError("Invalid created_on format. Use ISO datetime string") from exc

            payload[field] = value

        return self.repo.update_order(order_id, payload)

    def remove_order(self, order_id):
        return self.repo.delete_order(order_id)
