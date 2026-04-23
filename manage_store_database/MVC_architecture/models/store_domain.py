from datetime import datetime

from extensions import db


class Store_Data(db.Model):
        __tablename__ = "stores"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        address = db.Column(db.String(100), nullable=False)
        contact_number = db.Column(db.String(30))
        email = db.Column(db.String(100))
        created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        inventory_items = db.relationship("Inventory_Data", back_populates="store", lazy=True)
        products = db.relationship("Product_Data", secondary="store_products", back_populates="stores", lazy=True)