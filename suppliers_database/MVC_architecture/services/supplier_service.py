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

    def update_supplier(self, supplier_id, data):
        return self.repo.update_supplier(supplier_id, data)

    def remove_supplier(self, supplier_id):
        return self.repo.delete_supplier(supplier_id)
