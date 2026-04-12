from datetime import datetime

from ..models.supplier_repository import SupplierRepository


class SupplierService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_suppliers(self):
        return self.repo.fetch_all_suppliers()

    def add_supplier(self, data):
        payload = {
            "name": data["name"],
            "product": data.get("product"),
            "category": data.get("category"),
            "contact_number": data.get("contact_number"),
            "email": data.get("email"),
            "supplier_type": data.get("supplier_type"),
            "created_on": datetime.now().isoformat(),
        }
        return self.repo.create_supplier(payload)
