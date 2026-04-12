from ..models.product_repository import ProductRepository
from ..services.product_service import ProductService


class ProductController:
    def __init__(self, service):
        self.service = service

    def get_all_products(self):
        return self.service.get_all_products()

    def get_product(self, product_id):
        return self.service.get_product(product_id)

    def add_product(self, data):
        return self.service.add_product(data)

    def update_product(self, product_id, data):
        return self.service.update_product(product_id, data)

    def delete_product(self, product_id):
        return self.service.remove_product(product_id)


product_repository = ProductRepository()
product_service = ProductService(product_repository)
product_controller = ProductController(product_service)
