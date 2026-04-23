from datetime import datetime

from ..models.supplier_repository import SupplierRepository


class SupplierService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_suppliers(self):
        return self.repo.fetch_all_suppliers()

    def get_supplier(self, supplier_id):
        return self.repo.fetch_supplier(supplier_id)

    def add_supplier(self, data):
        name = data.get("name")
        if not name:
            raise ValueError("Supplier name is required")

        payload = {
            "name": name,
            "product": data.get("product"),
            "category": data.get("category"),
            "contact_number": data.get("contact_number"),
            "email": data.get("email"),
            "supplier_type": data.get("supplier_type"),
            "created_on": datetime.utcnow(),
        }
        return self.repo.create_supplier(payload)

    def update_supplier(self, supplier_id, data):
        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "name",
            "product",
            "category",
            "contact_number",
            "email",
            "supplier_type",
            "not_taking_return",
            "taking_return",
            "created_on",
            "user_email",
        }

        payload = {}
        for field, value in data.items():
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

            if field == "name" and (value is None or str(value).strip() == ""):
                raise ValueError("Supplier name cannot be empty")

            if field == "created_on" and isinstance(value, str):
                normalized_value = value.replace("Z", "+00:00")
                try:
                    value = datetime.fromisoformat(normalized_value)
                except ValueError as exc:
                    raise ValueError("Invalid created_on format. Use ISO datetime string") from exc

            payload[field] = value

        return self.repo.update_supplier(supplier_id, payload)

    def remove_supplier(self, supplier_id):
        return self.repo.delete_supplier(supplier_id)
