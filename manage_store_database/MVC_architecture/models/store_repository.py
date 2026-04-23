from extensions import db
from sqlalchemy.exc import IntegrityError, StatementError
from manage_store_database.MVC_architecture.models.store_domain import Store_Data
from manage_store_database.MVC_architecture.models.store_schema import StoreSchema
from products_database.MVC_architecture.models.product_domain import Product_Data


class StoreRepository:
    def __init__(self):
        self.schema = StoreSchema()
        self.list_schema = StoreSchema(many=True)

    def fetch_all_stores(self):
        stores = Store_Data.query.order_by(Store_Data.id.asc()).all()
        return self.list_schema.dump(stores)

    def create_store(self, store):
        payload = {k: v for k, v in store.items() if k != "product_ids"}
        record = Store_Data(**payload)

        if isinstance(store.get("product_ids"), list):
            record.products = Product_Data.query.filter(Product_Data.id.in_(store["product_ids"])).all()

        db.session.add(record)
        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid store data")
        return self.schema.dump(record)

    def fetch_store(self, store_id):
        record = db.session.get(Store_Data, int(store_id))
        return self.schema.dump(record) if record else None

    def update_store(self, store_id, data):
        record = db.session.get(Store_Data, int(store_id))
        if not record:
            return None

        for field, value in data.items():
            if field == "product_ids":
                continue
            setattr(record, field, value)

        if isinstance(data.get("product_ids"), list):
            record.products = Product_Data.query.filter(Product_Data.id.in_(data["product_ids"])).all()

        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid store data")
        return self.schema.dump(record)

    def delete_store(self, store_id):
        record = db.session.get(Store_Data, int(store_id))
        if not record:
            return False

        db.session.delete(record)
        db.session.commit()
        return True
