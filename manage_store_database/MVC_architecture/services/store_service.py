from datetime import datetime

from ..models.store_repository import StoreRepository


class StoreService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_stores(self):
        return self.repo.fetch_all_stores()

    def add_store(self, data):
        store = {
            "name": data["name"],
            "address": data["address"],
            "contact_number": data.get("contact_number"),
            "email": data.get("email"),
            "created_on": datetime.now().isoformat(),
        }
        return self.repo.create_store(store)
