from extensions import ma
from manage_store_database.MVC_architecture.models.store_domain import Store_Data


class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Store_Data
        include_fk = True
        load_instance = True
