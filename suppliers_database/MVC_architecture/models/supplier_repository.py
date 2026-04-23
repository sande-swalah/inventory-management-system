from extensions import db
from sqlalchemy.exc import IntegrityError


class SupplierRepository:
    def __init__(self):
        from suppliers_database.MVC_architecture.models.supplier_domain import Supplier_Data
        from suppliers_database.MVC_architecture.services.services_schema import SupplierSchema

        self.model = Supplier_Data
        self.schema = SupplierSchema()
        self.list_schema = SupplierSchema(many=True)

    def fetch_all_suppliers(self):
        suppliers = self.model.query.order_by(self.model.id.asc()).all()
        return self.list_schema.dump(suppliers)

    def fetch_supplier(self, supplier_id):
        supplier = db.session.get(self.model, int(supplier_id))
        return self.schema.dump(supplier) if supplier else None

    def create_supplier(self, data):
        supplier = self.model(**data)
        db.session.add(supplier)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Supplier email already exists")
        return self.schema.dump(supplier)

    def update_supplier(self, supplier_id, data):
        supplier = db.session.get(self.model, int(supplier_id))
        if not supplier:
            return None

        for field, value in data.items():
            setattr(supplier, field, value)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Supplier email already exists")
        return self.schema.dump(supplier)

    def delete_supplier(self, supplier_id):
        supplier = db.session.get(self.model, int(supplier_id))
        if not supplier:
            return False

        db.session.delete(supplier)
        db.session.commit()
        return True
