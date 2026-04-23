from datetime import datetime

from ..models.store_repository import StoreRepository


class StoreService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_stores(self):
        return self.repo.fetch_all_stores()

    def get_store(self, store_id):
        return self.repo.fetch_store(store_id)

    def add_store(self, data):
        store = {
            "name": data["name"],
            "address": data["address"],
            "contact_number": data.get("contact_number"),
            "email": data.get("email"),
            "product_ids": data.get("product_ids", []),
            "created_on": datetime.now().isoformat(),
        }
        return self.repo.create_store(store)

    def update_store(self, store_id, data):
        return self.repo.update_store(store_id, data)

    def remove_store(self, store_id):
        return self.repo.delete_store(store_id)
