from extensions import db
from products_database.MVC_architecture.models.product_domain import Product_Data
from products_database.MVC_architecture.models.product_schema import ProductSchema
from manage_store_database.MVC_architecture.models.store_domain import Store_Data
from orders_database.MVC_architecture.models.order_domain import Order_Data

product_schema = ProductSchema()
list_product_schema = ProductSchema(many=True)


class ProductRepository:
    def _apply_links(self, product, data):
        if isinstance(data.get("store_ids"), list):
            product.stores = Store_Data.query.filter(Store_Data.id.in_(data["store_ids"])).all()

        if isinstance(data.get("order_ids"), list):
            product.order_links = Order_Data.query.filter(Order_Data.id.in_(data["order_ids"])).all()

    def fetch_all_products(self):
        products = Product_Data.query.order_by(Product_Data.id.asc()).all()
        return list_product_schema.dump(products)

    def fetch_product(self, product_id):
        product = db.session.get(Product_Data, int(product_id))
        return product_schema.dump(product) if product else None

    def create_product(self, data):
        payload = {k: v for k, v in data.items() if k not in {"store_ids", "order_ids"}}
        product = Product_Data(**payload)
        self._apply_links(product, data)
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product)

    def update_product(self, product_id, data):
        product = db.session.get(Product_Data, int(product_id))
        if not product:
            return None

        for field, value in data.items():
            if field in {"store_ids", "order_ids"}:
                continue
            setattr(product, field, value)

        self._apply_links(product, data)

        db.session.commit()
        return product_schema.dump(product)

    def delete_product(self, product_id):
        product = db.session.get(Product_Data, int(product_id))
        if not product:
            return False

        db.session.delete(product)
        db.session.commit()
        return True
