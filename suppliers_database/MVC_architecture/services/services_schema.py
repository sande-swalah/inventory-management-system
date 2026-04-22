from extensions import ma
from suppliers_database.MVC_architecture.models.supplier_domain import Supplier_Data


class SupplierSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Supplier_Data
        load_instance = True
