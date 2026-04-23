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
        name = data.get("name")
        address = data.get("address")
        if not name:
            raise ValueError("Store name is required")
        if not address:
            raise ValueError("Store address is required")

        store = {
            "name": name,
            "address": address,
            "contact_number": data.get("contact_number"),
            "email": data.get("email"),
            "product_ids": data.get("product_ids", []),
            "created_on": datetime.utcnow(),
        }
        return self.repo.create_store(store)

    def update_store(self, store_id, data):
        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "name",
            "address",
            "contact_number",
            "email",
            "product_ids",
            "created_on",
        }

        payload = {}
        for field, value in data.items():
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

            if field == "name" and (value is None or str(value).strip() == ""):
                raise ValueError("Store name cannot be empty")

            if field == "address" and (value is None or str(value).strip() == ""):
                raise ValueError("Store address cannot be empty")

            if field == "created_on" and isinstance(value, str):
                normalized_value = value.replace("Z", "+00:00")
                try:
                    value = datetime.fromisoformat(normalized_value)
                except ValueError as exc:
                    raise ValueError("Invalid created_on format. Use ISO datetime string") from exc

            payload[field] = value

        return self.repo.update_store(store_id, payload)

    def remove_store(self, store_id):
        return self.repo.delete_store(store_id)
