from datetime import datetime

from ..models.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_items(self):
        return self.repo.fetch_all_items()

    def get_inventory_products(self):
        return self.repo.fetch_inventory_products()

    def get_item(self, item_id):
        return self.repo.fetch_item(item_id)

    def add_item(self, data):
        product_id = data.get("product_id")
        store_id = data.get("store_id")
        if product_id is None:
            raise ValueError("product_id is required")
        if store_id is None:
            raise ValueError("store_id is required")

        now = datetime.utcnow()
        item = {
            "product_id": product_id,
            "store_id": store_id,
            "quantity": data.get("quantity", 0),
            "threshold": data.get("threshold", 0),
            "last_updated": now,
        }
        return self.repo.create_item(item)

    def update_item(self, item_id, data):
        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "product_id",
            "store_id",
            "supplier_id",
            "quantity",
            "threshold",
            "last_updated",
        }

        payload = {}
        for field, value in data.items():
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

            if field == "last_updated" and isinstance(value, str):
                normalized_value = value.replace("Z", "+00:00")
                try:
                    value = datetime.fromisoformat(normalized_value)
                except ValueError as exc:
                    raise ValueError("Invalid last_updated format. Use ISO datetime string") from exc

            payload[field] = value

        payload["last_updated"] = datetime.utcnow()
        return self.repo.update_item(item_id, payload)

    def remove_item(self, item_id):
        return self.repo.delete_item(item_id)
