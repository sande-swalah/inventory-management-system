from ..models.inventory_repository import InventoryRepository
from ..services.inventory_service import InventoryService


class InventoryController:
    def __init__(self, service):
        self.service = service

    def get_all_items(self):
        return self.service.get_all_items()

    def get_item(self, item_id):
        return self.service.get_item(item_id)

    def add_item(self, data):
        return self.service.add_item(data)

    def update_item(self, item_id, data):
        return self.service.update_item(item_id, data)

    def delete_item(self, item_id):
        return self.service.remove_item(item_id)


inventory_repository = InventoryRepository()
inventory_service = InventoryService(inventory_repository)
inventory_controller = InventoryController(inventory_service)
