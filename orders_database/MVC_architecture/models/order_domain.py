from datetime import datetime

from extensions import db


class Order_Data(db.Model):
        __tablename__ = "orders"

        id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
        quantity = db.Column(db.Integer, nullable=False)
        order_value = db.Column(db.Float, nullable=False, default=0)
        status = db.Column(db.String(50), nullable=False, default="pending")
        expected_delivery = db.Column(db.String(50))
        created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        product = db.relationship("Product_Data", back_populates="orders")
        user = db.relationship("User_Data", back_populates="orders")
        products = db.relationship("Product_Data", secondary="order_products", back_populates="order_links", lazy=True)
