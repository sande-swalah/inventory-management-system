from datetime import datetime

from ..models.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_items(self):
        return self.repo.fetch_all_items()

    def get_item(self, item_id):
        return self.repo.fetch_item(item_id)

    def add_item(self, data):
        now = datetime.now().isoformat()
        item = {
            "product_id": data["product_id"],
            "store_id": data["store_id"],
            "quantity": data.get("quantity", 0),
            "threshold": data.get("threshold", 0),
            "last_updated": now,
        }
        return self.repo.create_item(item)

    def update_item(self, item_id, data):
        data = {**data, "last_updated": datetime.now().isoformat()}
        return self.repo.update_item(item_id, data)

    def remove_item(self, item_id):
        return self.repo.delete_item(item_id)
