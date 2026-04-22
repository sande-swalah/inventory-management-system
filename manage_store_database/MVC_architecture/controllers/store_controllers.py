from ..models.store_repository import StoreRepository
from ..services.store_service import StoreService


class StoreController:
    def __init__(self, service):
        self.service = service

    def get_all_stores(self):
        return self.service.get_all_stores()

    def get_store(self, store_id):
        return self.service.get_store(store_id)

    def add_store(self, data):
        return self.service.add_store(data)

    def update_store(self, store_id, data):
        return self.service.update_store(store_id, data)

    def delete_store(self, store_id):
        return self.service.remove_store(store_id)


store_repository = StoreRepository()
store_service = StoreService(store_repository)
store_controller = StoreController(store_service)
