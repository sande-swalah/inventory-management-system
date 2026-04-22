from ..models.supplier_repository import SupplierRepository
from ..services.supplier_service import SupplierService


class SupplierController:
    def __init__(self, service):
        self.service = service

    def get_all_suppliers(self):
        return self.service.get_all_suppliers()

    def get_supplier(self, supplier_id):
        return self.service.get_supplier(supplier_id)

    def add_supplier(self, data):
        return self.service.add_supplier(data)

    def update_supplier(self, supplier_id, data):
        return self.service.update_supplier(supplier_id, data)

    def delete_supplier(self, supplier_id):
        return self.service.remove_supplier(supplier_id)


supplier_repository = SupplierRepository()
supplier_service = SupplierService(supplier_repository)
supplier_controller = SupplierController(supplier_service)
