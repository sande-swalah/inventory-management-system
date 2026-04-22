from extensions import ma
from products_database.MVC_architecture.models.product_domain import Product_Data


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product_Data
        include_fk = True
        load_instance = True
