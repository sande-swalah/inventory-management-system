from datetime import datetime

from extensions import db


class Inventory_Data(db.Model):
        __tablename__ = "inventory_items"

        id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
        store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
        quantity = db.Column(db.Integer, nullable=False, default=0)
        threshold = db.Column(db.Integer, nullable=False, default=0)
        last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        product = db.relationship("Product_Data", back_populates="inventory_items")
        store = db.relationship("Store_Data", back_populates="inventory_items")
