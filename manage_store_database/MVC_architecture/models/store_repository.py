from extensions import db
from manage_store_database.MVC_architecture.models.store_domain import Store_Data
from manage_store_database.MVC_architecture.models.store_schema import StoreSchema


class StoreRepository:
    def __init__(self):
        self.schema = StoreSchema()
        self.list_schema = StoreSchema(many=True)

    def fetch_all_stores(self):
        stores = Store_Data.query.order_by(Store_Data.id.asc()).all()
        return self.list_schema.dump(stores)

    def create_store(self, store):
        record = Store_Data(**store)
        db.session.add(record)
        db.session.commit()
        return self.schema.dump(record)

    def fetch_store(self, store_id):
        record = db.session.get(Store_Data, int(store_id))
        return self.schema.dump(record) if record else None

    def update_store(self, store_id, data):
        record = db.session.get(Store_Data, int(store_id))
        if not record:
            return None

        for field, value in data.items():
            setattr(record, field, value)

        db.session.commit()
        return self.schema.dump(record)

    def delete_store(self, store_id):
        record = db.session.get(Store_Data, int(store_id))
        if not record:
            return False

        db.session.delete(record)
        db.session.commit()
        return True
