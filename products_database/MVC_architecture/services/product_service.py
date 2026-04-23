from datetime import datetime

from ..models.product_repository import ProductRepository


class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_products(self):
        return self.repo.fetch_all_products()

    def get_product(self, product_id):
        return self.repo.fetch_product(product_id)

    def add_product(self, data):
        name = data.get("name")
        if not name:
            raise ValueError("Product name is required")

        product = {
            "name": name,
            "buying_price": data.get("buying_price", 0),
            "quantity": data.get("quantity", 0),
            "threshold": data.get("threshold", 0),
            "expiry_date": data.get("expiry_date"),
            "supplier_id": data.get("supplier_id"),
            "category": data.get("category"),
            "store_ids": data.get("store_ids", []),
            "order_ids": data.get("order_ids", []),
            "created_on": datetime.utcnow(),
        }
        return self.repo.create_product(product)

    def update_product(self, product_id, data):
        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "name",
            "buying_price",
            "quantity",
            "threshold",
            "expiry_date",
            "supplier_id",
            "category",
            "store_ids",
            "order_ids",
            "created_on",
        }

        payload = {}
        for field, value in data.items():
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

            if field == "name" and (value is None or str(value).strip() == ""):
                raise ValueError("Product name cannot be empty")

            if field == "created_on" and isinstance(value, str):
                normalized_value = value.replace("Z", "+00:00")
                try:
                    value = datetime.fromisoformat(normalized_value)
                except ValueError as exc:
                    raise ValueError("Invalid created_on format. Use ISO datetime string") from exc

            payload[field] = value

        return self.repo.update_product(product_id, payload)

    def remove_product(self, product_id):
        return self.repo.delete_product(product_id)
