from datetime import datetime

from extensions import db


class Product_Data(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    buying_price = db.Column(db.Float, nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    threshold = db.Column(db.Integer, nullable=False, default=0)
    expiry_date = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))

    supplier = db.relationship("Supplier_Data", back_populates="products")
    inventory_items = db.relationship("Inventory_Data", back_populates="product", lazy=True)
    orders = db.relationship("Order_Data", back_populates="product", lazy=True)