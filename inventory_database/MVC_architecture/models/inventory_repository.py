from extensions import db
from sqlalchemy.exc import IntegrityError, StatementError
from inventory_database.MVC_architecture.models.inventory_domain import Inventory_Data
from products_database.MVC_architecture.models.product_domain import Product_Data
from products_database.MVC_architecture.models.product_schema import ProductSchema
from inventory_database.MVC_architecture.schemas.inventory_schema import InventorySchema


inventory_schema = InventorySchema()
list_inventory_schema = InventorySchema(many=True)
list_product_schema = ProductSchema(many=True)

class InventoryRepository:
    def fetch_all_items(self):
        items = Inventory_Data.query.order_by(Inventory_Data.id.asc()).all()
        return list_inventory_schema.dump(items)

    def fetch_item(self, item_id):
        item = db.session.get(Inventory_Data, int(item_id))
        return inventory_schema.dump(item) if item else None

    def fetch_inventory_products(self):
        products = (
            Product_Data.query.join(Inventory_Data, Inventory_Data.product_id == Product_Data.id)
            .distinct(Product_Data.id)
            .order_by(Product_Data.id.asc())
            .all()
        )
        return list_product_schema.dump(products)

    def create_item(self, data):
        item = Inventory_Data(**data)
        db.session.add(item)
        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid inventory data")
        return inventory_schema.dump(item)

    def update_item(self, item_id, data):
        item = db.session.get(Inventory_Data, int(item_id))
        if not item:
            return None

        for field, value in data.items():
            setattr(item, field, value)

        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid inventory data")
        return inventory_schema.dump(item)

    def delete_item(self, item_id):
        item = db.session.get(Inventory_Data, int(item_id))
        if not item:
            return False

        db.session.delete(item)
        db.session.commit()
        return True

    def create_data(self, obj):
        return self.create_item(obj)
    
    def read_data(self, id):
        return self.fetch_item(id)
    
    def read_all_data(self):
        return self.fetch_all_items()
        
    def update_data(self, id, obj):
        return self.update_item(id, obj)
    
    def delete_data(self, id):
        return self.delete_item(id)
