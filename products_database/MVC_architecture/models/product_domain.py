from datetime import datetime

from extensions import db


order_products = db.Table(
    "order_products",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)

store_products = db.Table(
    "store_products",
    db.Column("store_id", db.Integer, db.ForeignKey("stores.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)


class Product_Data(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Float, nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    threshold = db.Column(db.Integer, nullable=False, default=0)
    expiry_date = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50))
    

    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))

    supplier = db.relationship("Supplier_Data", back_populates="products")
    inventory_records = db.relationship(
        "Inventory_Data",
        back_populates="product",
        lazy=True,
        cascade="all, delete-orphan",
    )
    orders = db.relationship("Order_Data", back_populates="product", lazy=True)
    order_links = db.relationship("Order_Data", secondary="order_products", back_populates="products", lazy=True)
    stores = db.relationship("Store_Data", secondary="store_products", back_populates="products", lazy=True)

