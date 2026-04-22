from extensions import ma
from inventory_database.MVC_architecture.models.inventory_domain import Inventory_Data


class InventorySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Inventory_Data
		include_fk = True
		load_instance = True
