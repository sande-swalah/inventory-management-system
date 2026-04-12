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
        product = {
            "name": data["name"],
            "category": data.get("category"),
            "buying_price": data.get("buying_price", 0),
            "quantity": data.get("quantity", 0),
            "threshold": data.get("threshold", 0),
            "expiry_date": data.get("expiry_date"),
            "supplier_id": data.get("supplier_id"),
            "created_on": datetime.now().isoformat(),
        }
        return self.repo.create_product(product)

    def update_product(self, product_id, data):
        return self.repo.update_product(product_id, data)

    def remove_product(self, product_id):
        return self.repo.delete_product(product_id)
