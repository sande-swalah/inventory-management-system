from marshmallow import ValidationError, fields, validate

from extensions import db
from products_database.MVC_architecture.models.product_domain import Product_Data
from products_database.MVC_architecture.models.product_schema import ProductSchema

product_schema = ProductSchema()
list_product_schema = ProductSchema(many=True)


class ProductRepository:
    def create_product(self, data):
        
        try:
            new_product = product_schema.load(data)
        except ValidationError as err:
            return {"error": err.messages}, 422
        
        db.session.add(new_product)
        db.session.commit()
        return product_schema.dump(new_product)

    def fetch_all_products(self):
        products = Product_Data.query.order_by(Product_Data.id.asc()).all()
        return list_product_schema.dump(products)

    def fetch_product(self, product_id):
        product = db.session.get(Product_Data, int(product_id))
        return product_schema.dump(product) if product else None

    def create_product(self, data):
        product = Product_Data(**data)
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product)

    def update_product(self, product_id, data):
        product = db.session.get(Product_Data, int(product_id))
        if not product:
            return None

        for field, value in data.items():
            setattr(product, field, value)

        db.session.commit()
        return product_schema.dump(product)

    def delete_product(self, product_id):
        product = db.session.get(Product_Data, int(product_id))
        if not product:
            return False

        db.session.delete(product)
        db.session.commit()
        return True
