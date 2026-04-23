from marshmallow import fields

from extensions import ma
from inventory_database.MVC_architecture.models.inventory_domain import Inventory_Data
from products_database.MVC_architecture.models.product_schema import ProductSchema


class InventorySchema(ma.SQLAlchemyAutoSchema):
	product = fields.Nested(ProductSchema, dump_only=True)

	class Meta:
		model = Inventory_Data
		include_fk = True
		load_instance = True
