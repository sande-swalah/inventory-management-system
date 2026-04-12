from ..models.store_repository import StoreRepository
from ..services.store_service import StoreService


class StoreController:
    def __init__(self, service):
        self.service = service

    def get_all_stores(self):
        return self.service.get_all_stores()

    def add_store(self, data):
        return self.service.add_store(data)


store_repository = StoreRepository()
store_service = StoreService(store_repository)
store_controller = StoreController(store_service)
